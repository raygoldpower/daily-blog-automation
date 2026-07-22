import os
import requests
import json
import re
import time

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
BLOG_ID = "8468892944117983817"

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

def is_date_label(label):
    # "2026년 05월 01일" 패턴 감지
    return bool(re.match(r'^\d{4}년\s\d{2}월\s\d{2}일$', label.strip()))

def get_all_posts(token):
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
            "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts",
            headers={"Authorization": "Bearer " + token},
            params=params,
            timeout=30
        )
        if r.status_code != 200:
            print("글 목록 오류: " + r.text[:200])
            break
        data = r.json()
        items = data.get("items", [])
        posts.extend(items)
        page_token = data.get("nextPageToken")
        print("수집: " + str(len(posts)) + "개...")
        if not page_token:
            break
    return posts

def remove_date_labels(token, post_id, labels):
    clean_labels = [l for l in labels if not is_date_label(l)]
    if len(clean_labels) == len(labels):
        return False  # 변경 없음

    r = requests.patch(
        "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts/" + post_id,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
        json={"labels": clean_labels},
        timeout=15
    )
    return r.status_code == 200

if __name__ == "__main__":
    print("토큰 발급 중...")
    token = get_access_token()
    print("글 목록 수집 중...")
    posts = get_all_posts(token)
    print("총 " + str(len(posts)) + "개 글 수집 완료")

    fixed = 0
    skipped = 0
    for post in posts:
        labels = post.get("labels", [])
        date_labels = [l for l in labels if is_date_label(l)]
        if not date_labels:
            skipped += 1
            continue
        print("수정: " + post["id"] + " | 제거 태그: " + str(date_labels))
        ok = remove_date_labels(token, post["id"], labels)
        if ok:
            fixed += 1
        else:
            print("  실패!")
        time.sleep(0.5)

    print("\n완료! 수정: " + str(fixed) + "개 / 건너뜀: " + str(skipped) + "개")
