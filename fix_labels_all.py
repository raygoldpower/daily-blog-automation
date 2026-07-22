import os
import requests
import json
import re
import time

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")

# 블로그 설정
BLOGS = {
    "blog1": {
        "id": "4393162034375416055",
        "name": "curiousmantor",
        "keep_labels": {
            "Soccer", "Basketball", "Baseball", "Muscle Science", "Rehab",
            "Nutrition", "Sports Psychology", "Conditioning", "Mobility",
            "Physiology", "Physical Therapy", "Biomechanics", "Anatomy",
            "Body Balance", "Sports Medicine", "General"
        }
    },
    "blog2": {
        "id": "8468892944117983817",
        "name": "insaplayer",
        "keep_labels": {
            "사회이슈", "경제", "연예", "스포츠", "IT과학",
            "시사칼럼", "이슈해설", "많이본뉴스", "생활정보"
        }
    }
}

def get_access_token():
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "refresh_token": GOOGLE_REFRESH_TOKEN,
            "grant_type": "refresh_token"
        },
        timeout=10
    )
    if response.status_code != 200:
        raise Exception("토큰 실패: " + response.text)
    return response.json()["access_token"]

def get_all_posts(token, blog_id):
    posts = []
    page_token = None
    while True:
        params = {
            "maxResults": 500,
            "fields": "items(id,labels),nextPageToken",
            "status": "live"
        }
        if page_token:
            params["pageToken"] = page_token
        r = requests.get(
            "https://www.googleapis.com/blogger/v3/blogs/" + blog_id + "/posts",
            headers={"Authorization": "Bearer " + token},
            params=params,
            timeout=30
        )
        if r.status_code != 200:
            print("오류: " + r.text[:200])
            break
        data = r.json()
        posts.extend(data.get("items", []))
        page_token = data.get("nextPageToken")
        print("  수집: " + str(len(posts)) + "개...")
        if not page_token:
            break
    return posts

def fix_post_labels(token, blog_id, post_id, labels, keep_labels):
    clean_labels = [l for l in labels if l in keep_labels]
    if len(clean_labels) == len(labels):
        return False  # 변경 없음
    r = requests.patch(
        "https://www.googleapis.com/blogger/v3/blogs/" + blog_id + "/posts/" + post_id,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
        json={"labels": clean_labels},
        timeout=15
    )
    return r.status_code == 200

if __name__ == "__main__":
    print("토큰 발급 중...")
    token = get_access_token()

    for key, blog in BLOGS.items():
        print("\n" + "="*50)
        print("[" + blog["name"] + "] 태그 정리 시작")
        print("유지할 태그: " + str(blog["keep_labels"]))
        print("="*50)

        posts = get_all_posts(token, blog["id"])
        print("총 " + str(len(posts)) + "개 글")

        fixed = 0
        skipped = 0
        for post in posts:
            labels = post.get("labels", [])
            if not labels:
                skipped += 1
                continue

            removable = [l for l in labels if l not in blog["keep_labels"]]
            if not removable:
                skipped += 1
                continue

            print("수정: " + post["id"] + " | 제거: " + str(removable))
            ok = fix_post_labels(token, blog["id"], post["id"], labels, blog["keep_labels"])
            if ok:
                fixed += 1
            else:
                print("  실패!")
            time.sleep(0.5)

        print("\n[" + blog["name"] + "] 완료 — 수정: " + str(fixed) + "개 / 건너뜀: " + str(skipped) + "개")

    print("\n전체 완료!")
