import os
import requests
import random
from datetime import datetime

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
FACEBOOK_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "")
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN", "")
BLOG_ID = "8468892944117983817"

TODAY = datetime.now().strftime("%Y년 %m월 %d일")

CATEGORY_EMOJI = {
    "스포츠이슈": "⚽",
    "경제뉴스": "💰",
    "전국이슈": "🌍",
    "연예이슈": "🎭"
}

# 카테고리별 검색 쿼리
SEARCH_TOPICS = [
    # 스포츠 이슈
    {
        "category": "스포츠이슈",
        "keyword": "sports news korea",
        "queries": [
            "오늘 스포츠 뉴스 이슈 " + datetime.now().strftime("%Y년 %m월 %d일"),
            "축구 농구 야구 오늘 핫이슈",
            "스포츠 선수 공식 발표 오늘",
            "스포츠조선 오늘 뉴스",
            "해외 스포츠 이슈 오늘 한국",
        ]
    },
    # 경제 뉴스
    {
        "category": "경제뉴스",
        "keyword": "economy finance korea",
        "queries": [
            "오늘 경제 뉴스 핫이슈 " + datetime.now().strftime("%Y년 %m월 %d일"),
            "코스피 코스닥 오늘 시장 동향",
            "부동산 금리 환율 오늘 뉴스",
            "주식 투자 오늘 핫종목 이슈",
            "경제 정책 기업 오늘 발표",
        ]
    },
    # 전국 이슈
    {
        "category": "전국이슈",
        "keyword": "korea news issue today",
        "queries": [
            "오늘 전국 사회 핫이슈 " + datetime.now().strftime("%Y년 %m월 %d일"),
            "오늘 사건사고 뉴스 한국",
            "정치 사회 오늘 핫이슈",
            "오늘 화제 뉴스 한국 실시간",
            "오늘 논란 이슈 사회 뉴스",
        ]
    },
    # 연예 이슈
    {
        "category": "연예이슈",
        "keyword": "kpop entertainment news",
        "queries": [
            "오늘 연예 뉴스 핫이슈 " + datetime.now().strftime("%Y년 %m월 %d일"),
            "오늘 드라마 영화 음악 화제",
            "연예인 공식 발표 오늘 뉴스",
            "K팝 아이돌 오늘 이슈",
            "오늘 연예계 논란 공식 발표",
        ]
    },
]


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


def search_news(query):
    print("[웹검색] 검색 중: " + query)
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 2000,
            "tools": [{"type": "web_search_20250305", "name": "web_search"}],
            "messages": [{
                "role": "user",
                "content": (
                    "오늘(" + TODAY + ") 기준으로 다음 키워드를 검색해서 "
                    "실제 뉴스 기사에서 확인된 핵심 팩트만 3~5가지 요약해줘. "
                    "루머나 추측은 절대 포함하지 마. "
                    "각 팩트에 출처 언론사명을 표기해줘.\n\n"
                    "검색 키워드: " + query
                )
            }]
        },
        timeout=60
    )
    if response.status_code != 200:
        print("[웹검색 실패] " + str(response.status_code))
        return ""
    content = response.json().get("content", [])
    result = ""
    for block in content:
        if block.get("type") == "text":
            result += block.get("text", "")
    return result


def generate_with_claude(prompt):
    print("[AI] Claude 글 생성 중...")
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 8000,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=300
    )
    if response.status_code != 200:
        raise Exception("Claude 오류: " + str(response.status_code))
    return response.json()["content"][0]["text"]


def generate_post():
    topic = random.choice(SEARCH_TOPICS)
    query = random.choice(topic["queries"])

    print("[카테고리] " + topic["category"])
    print("[검색어] " + query)

    news_context = search_news(query)

    if not news_context or len(news_context) < 100:
        print("[경고] 검색 결과 부족, 다른 쿼리로 재시도")
        query = random.choice(topic["queries"])
        news_context = search_news(query)

    prompt = (
        "당신은 20년 경력의 베테랑 시니어 기자입니다.\n"
        "TV 뉴스 앵커처럼 명확하고 신뢰감 있으며, 독자를 끌어당기는 문장력을 갖고 있습니다.\n"
        "한자, 일본어, 중국어 등 한국어가 아닌 문자는 절대 사용하지 마세요.\n\n"
        "오늘(" + TODAY + ") 수집한 뉴스 정보:\n"
        + news_context + "\n\n"
        "절대 지켜야 할 원칙:\n"
        "1. 공식 확인된 팩트만 작성하세요. 루머, 찌라시, 추측 절대 금지.\n"
        "2. 명예훼손이 될 수 있는 내용 절대 금지.\n"
        "3. 확인되지 않은 사생활 침해 내용 절대 금지.\n"
        "4. 법원 판결, 공식 발표, 공식 보도된 내용만 다루세요.\n"
        "5. 반드시 존댓말을 사용하세요.\n"
        "6. 중립적이고 객관적인 시각을 유지하세요.\n"
        "7. 수치, 날짜, 출처를 명확히 표기하세요.\n"
        "8. 제목과 내용이 일치해야 합니다. 낚시성 제목 금지.\n\n"
        "글쓰기 스타일:\n"
        "첫 문장부터 핵심 팩트를 강렬하게 전달하세요.\n"
        "독자가 이 글 하나로 이슈의 전말을 완전히 이해할 수 있게 작성하세요.\n"
        "전문 용어는 괄호 안에 쉬운 설명을 추가하세요.\n"
        "소제목은 [소제목] 형식으로 표시하고 이모지를 붙이세요.\n\n"
        "반드시 아래 구조로 작성하세요:\n"
        "1. 리드문: 핵심 팩트를 2~3줄로 강렬하게 전달\n"
        "2. 배경 설명: 이 이슈가 왜 중요한지\n"
        "3. 팩트 분석: 확인된 사실만 수치/날짜와 함께\n"
        "4. 현장/전문가 시각: 업계 반응\n"
        "5. 독자 관점: 이 이슈의 의미\n"
        "6. 전망: 앞으로 어떻게 될 것인가\n\n"
        "핵심 요약: [SUMMARY_START]와 [SUMMARY_END] 사이에 3가지 핵심만 작성\n\n"
        "카테고리: " + topic["category"] + "\n"
        "목표 분량: 2500자에서 4000자\n\n"
        "반드시 아래 형식으로 출력하세요:\n"
        "제목: (팩트 기반의 강렬하고 정확한 제목)\n"
        "---\n"
        "(본문 내용)"
    )

    full_text = generate_with_claude(prompt)

    lines = full_text.strip().split("\n")
    title = ""
    body_lines = []
    separator_found = False

    for line in lines:
        if line.startswith("제목:"):
            title = line.replace("제목:", "").strip()
        elif line.strip() == "---":
            separator_found = True
        elif separator_found:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    if not title:
        title = TODAY + " " + topic["category"] + " 핫이슈"
    if not body:
        body = full_text

    print("[완료] 제목: " + title)
    print("[완료] 글자수: " + str(len(body)) + "자")
    return {"title": title, "body": body, "topic": topic}


def get_images(keyword, count=3):
    if not UNSPLASH_ACCESS_KEY:
        return []
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query": keyword,
                "per_page": count,
                "orientation": "landscape",
                "client_id": UNSPLASH_ACCESS_KEY
            },
            timeout=10
        )
        images = []
        for photo in response.json().get("results", []):
            images.append({
                "url": photo["urls"]["regular"],
                "alt": photo.get("alt_description", keyword) or keyword,
                "author": photo["user"]["name"],
                "author_url": photo["user"]["links"]["html"]
            })
        print("[이미지] " + str(len(images)) + "장 수집 완료")
        return images
    except Exception as e:
        print("[이미지 오류] " + str(e))
        return []


def make_summary_html(summary_text):
    lines = [l.strip() for l in summary_text.strip().split("\n") if l.strip()]
    html = '<div style="background:#fff8e1;border-left:5px solid #f57f17;border-radius:8px;padding:20px 24px;margin:28px 0;">'
    html += '<p style="font-weight:700;font-size:17px;color:#f57f17;margin-bottom:12px;">📌 핵심 요약</p>'
    for line in lines:
        html += '<p style="margin:6px 0;font-size:15px;color:#333;">✅ ' + line + "</p>"
    html += "</div>\n"
    return html


def make_image_html(img, margin_top="0"):
    html = '<div style="text-align:center;margin:30px 0;margin-top:' + margin_top + ';">'
    html += '<img src="' + img["url"] + '" alt="' + img["alt"] + '" style="max-width:100%;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.12);"/>'
    html += '<p style="font-size:12px;color:#999;margin-top:8px;">Photo by <a href="' + img["author_url"] + '" style="color:#999;">' + img["author"] + '</a> on Unsplash</p>'
    html += "</div>\n"
    return html


def body_to_html(body, images, topic):
    import re

    category = topic.get("category", "이슈")
    emoji = CATEGORY_EMOJI.get(category, "📰")

    category_badge = (
        '<div style="display:inline-block;background:#e65100;color:#fff;'
        'font-size:13px;padding:4px 12px;border-radius:20px;margin-bottom:8px;">'
        + emoji + " " + category + "</div>\n"
    )
    date_badge = (
        '<div style="font-size:13px;color:#888;margin-bottom:16px;">'
        + TODAY + "</div>\n"
    )

    html = category_badge + date_badge

    if len(images) >= 1:
        html += make_image_html(images[0])

    summary_pattern = re.compile(r'\[SUMMARY_START\](.*?)\[SUMMARY_END\]', re.DOTALL)
    summary_match = summary_pattern.search(body)
    summary_html = make_summary_html(summary_match.group(1)) if summary_match else ""
    clean_body = summary_pattern.sub("[SUMMARY_PLACEHOLDER]", body)

    paragraphs = clean_body.split("\n")
    mid = len(paragraphs) // 2
    image2_inserted = False

    for i, para in enumerate(paragraphs):
        if not para.strip():
            html += '<p style="margin:14px 0;">&nbsp;</p>\n'
            continue
        if para.strip() == "[SUMMARY_PLACEHOLDER]":
            html += summary_html
            continue
        if para.startswith("[") and "]" in para:
            heading = para.strip("[]").strip()
            html += '<h2 style="margin-top:40px;margin-bottom:14px;font-size:22px;border-left:4px solid #e65100;padding-left:14px;color:#1a1a1a;">' + heading + "</h2>\n"
        elif len(para.strip()) > 1 and para.strip()[0].isdigit() and para.strip()[1] in [".", ")"]:
            html += '<p style="margin:8px 0 8px 24px;line-height:2.0;color:#333;">' + para + "</p>\n"
        else:
            html += '<p style="margin:12px 0;line-height:2.0;font-size:16px;color:#222;">' + para + "</p>\n"

        if i >= mid and not image2_inserted and len(images) >= 2:
            html += make_image_html(images[1], margin_top="20px")
            image2_inserted = True

    if len(images) >= 3:
        html += make_image_html(images[2], margin_top="20px")

    return html


def send_telegram(title, post_url, topic):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[텔레그램] 설정값 없음 - 건너뜀")
        return
    category = topic.get("category", "이슈")
    emoji = CATEGORY_EMOJI.get(category, "📰")
    message = (
        emoji + " 새 포스팅\n\n"
        + "📌 " + title + "\n\n"
        + "🔗 " + post_url
    )
    try:
        response = requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
            timeout=10
        )
        if response.status_code == 200:
            print("[텔레그램] 공유 성공!")
        else:
            print("[텔레그램] 실패: " + response.text[:200])
    except Exception as e:
        print("[텔레그램 오류] " + str(e))


def send_facebook(title, post_url, topic):
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        print("[페이스북] 설정값 없음 - 건너뜀")
        return
    category = topic.get("category", "이슈")
    emoji = CATEGORY_EMOJI.get(category, "📰")
    message = (
        emoji + " 새 포스팅\n\n"
        + title + "\n\n"
        + "자세히 읽기 👉 " + post_url
    )
    try:
        response = requests.post(
            "https://graph.facebook.com/v19.0/" + FACEBOOK_PAGE_ID + "/feed",
            data={
                "message": message,
                "link": post_url,
                "access_token": FACEBOOK_ACCESS_TOKEN
            },
            timeout=10
        )
        if response.status_code == 200:
            print("[페이스북] 공유 성공!")
        else:
            print("[페이스북] 실패: " + response.text[:200])
    except Exception as e:
        print("[페이스북 오류] " + str(e))


def post_to_blogger(post_data, images):
    print("\n[Blogger] insaplayer 포스팅 시작...")
    access_token = get_access_token()
    body_html = body_to_html(post_data["body"], images, post_data["topic"])
    url = "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts?isDraft=false"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    payload = {
        "kind": "blogger#post",
        "title": post_data["title"],
        "content": body_html,
        "status": "LIVE"
    }
    print("[제목] " + post_data["title"])
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print("[응답] 상태코드: " + str(response.status_code))
    if response.status_code == 200:
        result = response.json()
        post_url = result.get("url", "")
        print("\n발행 완료!")
        print("   링크: " + post_url)
        send_telegram(post_data["title"], post_url, post_data["topic"])
        send_facebook(post_data["title"], post_url, post_data["topic"])
        return True
    else:
        print("실패: " + response.text[:300])
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("insaplayer - 실시간 이슈 블로그 - Claude Edition")
    print("실행 시각: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)
    try:
        post = generate_post()
        images = get_images(post["topic"]["keyword"], count=3)
        post_to_blogger(post, images)
        print("\n모든 작업 완료!")
    except Exception as e:
        print("\n오류 발생: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
