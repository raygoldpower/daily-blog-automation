import os
import requests
import time
import json

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
BLOG_ID = "4393162034375416055"
SITE_URL = "https://curiousmantor.blogspot.com"


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


def get_all_post_urls(access_token):
    """블로그 전체 글 URL 수집"""
    urls = []
    page_token = None
    url = "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts"

    while True:
        params = {
            "maxResults": 500,
            "fields": "items(url),nextPageToken",
            "status": "live"
        }
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
        for item in items:
            post_url = item.get("url", "")
            if post_url:
                urls.append(post_url)

        print("[수집] 총 " + str(len(urls)) + "개 URL 수집됨...")

        page_token = data.get("nextPageToken")
        if not page_token:
            break
        time.sleep(0.5)

    return urls


def request_indexing_via_search_console(access_token, post_url):
    """Search Console Inspection API로 색인 요청"""
    response = requests.post(
        "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
        headers={
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        },
        json={
            "inspectionUrl": post_url,
            "siteUrl": SITE_URL + "/"
        },
        timeout=15
    )
    return response.status_code, response.json() if response.content else {}


def load_done_urls():
    """이미 요청한 URL 목록 로드"""
    try:
        with open("indexed_urls.json", "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_done_urls(urls):
    """요청 완료 URL 저장"""
    try:
        with open("indexed_urls.json", "w") as f:
            json.dump(urls, f, ensure_ascii=False)
    except Exception as e:
        print("[저장 오류] " + str(e))


def main():
    print("=" * 50)
    print("Search Console 색인 자동 요청 스크립트")
    print("블로그1: curiousmantor.blogspot.com")
    print("=" * 50)

    access_token = get_access_token()

    print("\n[1단계] 전체 글 URL 수집 중...")
    all_urls = get_all_post_urls(access_token)
    print("[완료] 총 " + str(len(all_urls)) + "개 URL 발견\n")

    # 이미 요청한 URL 제외
    done_urls = load_done_urls()
    pending_urls = [u for u in all_urls if u not in done_urls]
    print("[대기] 색인 요청 대기 중: " + str(len(pending_urls)) + "개")
    print("[완료] 이미 요청됨: " + str(len(done_urls)) + "개\n")

    if not pending_urls:
        print("모든 글 색인 요청 완료! 더 이상 요청할 URL이 없어요.")
        return

    # 하루 최대 200개 제한
    batch = pending_urls[:200]
    print("[시작] 이번 실행: " + str(len(batch)) + "개 요청\n")

    success = 0
    fail = 0
    newly_done = list(done_urls)

    for i, url in enumerate(batch):
        # 50개마다 토큰 갱신
        if i > 0 and i % 50 == 0:
            print("\n[토큰 갱신] 재발급 중...")
            access_token = get_access_token()

        status_code, result = request_indexing_via_search_console(access_token, url)

        if status_code == 200:
            verdict = result.get("inspectionResult", {}).get("indexStatusResult", {}).get("verdict", "")
            coverage = result.get("inspectionResult", {}).get("indexStatusResult", {}).get("coverageState", "")
            success += 1
            newly_done.append(url)
            print("[성공] " + str(i+1) + "/" + str(len(batch)) + " | " + verdict + " | " + url[-60:])
        else:
            fail += 1
            error_msg = str(result)[:80] if result else str(status_code)
            print("[실패] " + str(i+1) + "/" + str(len(batch)) + " | " + error_msg)

        save_done_urls(newly_done)
        time.sleep(1)  # API 한도 초과 방지

    print("\n" + "=" * 50)
    print("완료! 성공: " + str(success) + "개 / 실패: " + str(fail) + "개")
    print("남은 URL: " + str(len(pending_urls) - len(batch)) + "개 (내일 실행 시 자동 처리)")
    print("=" * 50)


if __name__ == "__main__":
    main()
