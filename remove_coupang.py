import os
import requests
import re
import time

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
BLOG_ID = "4393162034375416055"


def get_access_token():
    print("[인증] Google Access Token 발급 중...")
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
        raise Exception("토큰 발급 실패: " + response.text)
    print("[인증] 완료!")
    return response.json()["access_token"]


def remove_coupang_from_html(html):
    """HTML에서 쿠팡 박스 제거"""
    # 쿠팡 div 블록 제거 (fff8e1 배경색 기준)
    pattern = re.compile(
        r'<div style="background:#fff8e1;border:2px solid #f57f17.*?</div>\s*',
        re.DOTALL
    )
    cleaned = pattern.sub('', html)

    # 혹시 다른 형태의 쿠팡 박스도 제거
    pattern2 = re.compile(
        r'<div style="background:#fff8e1.*?쿠팡에서 검색하기.*?</div>\s*',
        re.DOTALL
    )
    cleaned = pattern2.sub('', cleaned)

    # 쿠팡 링크 단독 제거 (혹시 남은 경우)
    pattern3 = re.compile(
        r'<a href="https://(?:www\.coupang\.com|link\.coupang\.com).*?</a>',
        re.DOTALL
    )
    cleaned = pattern3.sub('', cleaned)

    return cleaned


def get_all_posts(access_token):
    """블로그 전체 글 목록 가져오기"""
    posts = []
    page_token = None
    url = "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts"

    while True:
        params = {"maxResults": 500, "fields": "items(id,title,content),nextPageToken"}
        if page_token:
            params["pageToken"] = page_token

        response = requests.get(
            url,
            headers={"Authorization": "Bearer " + access_token},
            params=params,
            timeout=30
        )

        if response.status_code != 200:
            print("[오류] 글 목록 가져오기 실패: " + response.text[:200])
            break

        data = response.json()
        items = data.get("items", [])
        posts.extend(items)
        print("[수집] 총 " + str(len(posts)) + "개 수집됨...")

        page_token = data.get("nextPageToken")
        if not page_token:
            break
        time.sleep(1)

    return posts


def update_post(access_token, post_id, title, new_content):
    """글 내용 업데이트"""
    url = "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts/" + post_id
    response = requests.patch(
        url,
        headers={
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        },
        json={"content": new_content},
        timeout=30
    )
    return response.status_code == 200


def main():
    print("=" * 50)
    print("쿠팡 링크 일괄 삭제 스크립트")
    print("=" * 50)

    access_token = get_access_token()

    print("\n[1단계] 전체 글 목록 가져오는 중...")
    posts = get_all_posts(access_token)
    print("[완료] 총 " + str(len(posts)) + "개 글 발견\n")

    target_posts = []
    for post in posts:
        content = post.get("content", "")
        if "쿠팡" in content or "coupang" in content.lower():
            target_posts.append(post)

    print("[분석] 쿠팡 링크 포함 글: " + str(len(target_posts)) + "개\n")

    if not target_posts:
        print("쿠팡 링크가 없습니다. 완료!")
        return

    success = 0
    fail = 0

    for i, post in enumerate(target_posts):
        post_id = post["id"]
        title = post["title"]
        content = post["content"]

        new_content = remove_coupang_from_html(content)

        if new_content == content:
            print("[스킵] " + str(i+1) + "/" + str(len(target_posts)) + " 변경 없음: " + title[:30])
            continue

        # 토큰 갱신 (50개마다)
        if i > 0 and i % 50 == 0:
            print("\n[토큰 갱신] 재발급 중...")
            access_token = get_access_token()

        ok = update_post(access_token, post_id, title, new_content)

        if ok:
            success += 1
            print("[성공] " + str(i+1) + "/" + str(len(target_posts)) + " : " + title[:40])
        else:
            fail += 1
            print("[실패] " + str(i+1) + "/" + str(len(target_posts)) + " : " + title[:40])

        time.sleep(0.5)  # API 한도 초과 방지

    print("\n" + "=" * 50)
    print("완료! 성공: " + str(success) + "개 / 실패: " + str(fail) + "개")
    print("=" * 50)


if __name__ == "__main__":
    main()
