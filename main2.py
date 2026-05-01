import os
import requests
import random
from datetime import datetime
import time

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

CATEGORIES = ["스포츠이슈", "경제뉴스", "전국이슈", "연예이슈"]


def call_claude(messages, max_tokens=4000, use_search=False):
    for attempt in range(3):
        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": max_tokens,
            "messages": messages
        }
        if use_search:
            payload["tools"] = [{"type": "web_search_20250305", "name": "web_search"}]

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json=payload,
            timeout=120
        )
        if response.status_code == 200:
            content = response.json().get("content", [])
            result = ""
            for block in content:
                if block.get("type") == "text":
                    result += block.get("text", "")
            return result
        elif response.status_code == 429:
            wait = 60 * (attempt + 1)
            print("[429] " + str(wait) + "초 대기 후 재시도...")
            time.sleep(wait)
        else:
            raise Exception("Claude 오류: " + str(response.status_code))
    raise Exception("Claude 오류: 최대 재시도 횟수 초과")


def get_hot_topic(category):
    print("[핫이슈 탐색] 카테고리: " + category)

    category_map = {
        "스포츠이슈": "스포츠 (축구, 농구, 야구, 선수 이슈, 구단 뉴스)",
        "경제뉴스": "경제 (주식, 부동산, 금리, 환율, 기업 뉴스)",
        "전국이슈": "사회 (정치, 사건사고, 정책, 사회 이슈)",
        "연예이슈": "연예 (드라마, 영화, K팝, 연예인 공식 발표)"
    }

    prompt = (
        "오늘(" + TODAY + ") 한국에서 가장 뜨거운 " + category_map[category] + " 분야 핫이슈를 웹에서 검색해줘.\n\n"
        "반드시 아래 형식으로만 출력해:\n"
        "주제: (오늘 가장 핫한 이슈 제목)\n"
        "키워드: (검색 키워드 영문)\n"
        "핵심팩트: (확인된 팩트 3줄 이내)\n\n"
        "조건:\n"
        "- 공식 확인된 뉴스만\n"
        "- 루머나 추측 금지\n"
        "- 오늘 날짜 기준 가장 화제인 것\n"
        "- 명예훼손 내용 금지"
    )

    result = call_claude(
        [{"role": "user", "content": prompt}],
        max_tokens=500,
        use_search=True
    )
    print("[핫이슈] " + result[:100])
    return result


def generate_post():
    category = random.choice(CATEGORIES)
    print("[카테고리] " + category)

    hot_topic = get_hot_topic(category)
    time.sleep(5)

    prompt = (
        "당신은 20년 경력의 베테랑 시니어 기자입니다.\n"
        "TV 뉴스 앵커처럼 명확하고 신뢰감 있으며, 독자를 끌어당기는 문장력을 갖고 있습니다.\n"
        "한국어만 사용하세요. 외국 문자 절대 금지.\n\n"
        "오늘(" + TODAY + ") 가장 핫한 이슈:\n"
        + hot_topic + "\n\n"
        "절대 지켜야 할 원칙:\n"
        "1. 공식 확인된 팩트만 작성하세요. 루머, 추측 절대 금지.\n"
        "2. 명예훼손 내용 절대 금지.\n"
        "3. 반드시 존댓말을 사용하세요.\n"
        "4. 중립적이고 객관적인 시각을 유지하세요.\n"
        "5. 제목과 내용이 일치해야 합니다. 낚시성 제목 금지.\n\n"
        "글 구조 (반드시 이 순서로):\n\n"
        "1. 리드문 (2~3줄)\n"
        "핵심 팩트를 강렬하게 전달하세요. 독자가 첫 문장에 멈추게 만드세요.\n\n"
        "2. ##핵심키워드##\n"
        "이 이슈의 핵심을 한 단어나 짧은 구로 크게 던지세요.\n"
        "그 아래 2~3문장으로 쉽게 풀어쓰세요.\n\n"
        "3. 소제목 구조 (3~4개)\n"
        "소제목: [이모지 소제목내용 이모지] 형식. 앞뒤 이모지 필수.\n"
        "예: [📌 사건의 전말 📌], [💬 각계 반응 💬]\n"
        "각 소제목 아래: 배경 → 팩트 → 반응 순으로 깊어지게\n"
        "단락 3~4줄 이내. 빈 줄 필수.\n"
        "수치, 날짜, 출처 명확히 표기.\n\n"
        "4. 추천 운동 표 없음 (뉴스 기사이므로 생략)\n\n"
        "5. 전망 + 독자 관점\n"
        "앞으로 어떻게 될지 + 독자에게 의미하는 것\n"
        "반드시 존댓말로 끝내세요. 격언 금지.\n\n"
        "6. 핵심 요약\n"
        "[SUMMARY_START]\n"
        "핵심1\n"
        "핵심2\n"
        "핵심3\n"
        "[SUMMARY_END]\n\n"
        "글쓰기 원칙:\n"
        "반드시 존댓말. '~이다', '~한다' 반말 종결 절대 금지.\n"
        "AI 티 나는 나열식 표현 금지.\n"
        "2500자에서 3500자.\n\n"
        "카테고리: " + category + "\n\n"
        "출력 형식:\n"
        "제목: (팩트 기반 강렬한 제목)\n"
        "---\n"
        "(본문)"
    )

    print("[AI] 기사 작성 중...")
    full_text = call_claude(
        [{"role": "user", "content": prompt}],
        max_tokens=4000,
        use_search=False
    )

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
        title = TODAY + " " + category + " 핫이슈"
    if not body:
        body = full_text

    print("[완료] 제목: " + title)
    print("[완료] 글자수: " + str(len(body)) + "자")
    return {"title": title, "body": body, "category": category}


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
        print("[이미지] " + str(len(images)) + "장 수집")
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


def body_to_html(body, images, category):
    import re

    emoji = CATEGORY_EMOJI.get(category, "📰")

    # 배지 + 날짜
    html = (
        '<div style="display:inline-block;background:#e65100;color:#fff;'
        'font-size:13px;padding:5px 14px;border-radius:20px;margin-bottom:8px;font-weight:600;">'
        + emoji + " " + category + "</div>\n"
        '<div style="font-size:13px;color:#888;margin-bottom:20px;">📅 ' + TODAY + "</div>\n"
    )

    # 상단 이미지
    if len(images) >= 1:
        html += make_image_html(images[0])

    # 목차 자동 생성
    summary_pattern = re.compile(r'\[SUMMARY_START\](.*?)\[SUMMARY_END\]', re.DOTALL)
    keyword_pattern = re.compile(r'##(.+?)##')

    summary_match = summary_pattern.search(body)
    summary_html = make_summary_html(summary_match.group(1)) if summary_match else ""
    clean_body = summary_pattern.sub("[SUMMARY_PLACEHOLDER]", body)

    headings = re.findall(r'\[([^\]]+)\]', clean_body)
    headings = [h for h in headings if h not in ["SUMMARY_PLACEHOLDER"]]
    if headings:
        toc = '<div style="background:#f8f9ff;border:1px solid #e0e0e0;border-radius:10px;padding:20px 24px;margin:24px 0;">'
        toc += '<p style="font-weight:700;font-size:15px;color:#e65100;margin-bottom:12px;">📋 목차</p>'
        toc += '<ol style="margin:0;padding-left:20px;">'
        for h in headings:
            clean_h = re.sub(r'^[^\w가-힣]+', '', h).strip()
            clean_h = re.sub(r'[^\w가-힣\s]+$', '', clean_h).strip()
            if clean_h:
                toc += '<li style="margin:6px 0;font-size:15px;color:#444;line-height:1.6;">' + clean_h + '</li>'
        toc += '</ol></div>\n'
        html += toc

    def replace_keyword(m):
        return (
            '<div style="margin:28px 0 12px 0;">'
            '<span style="display:inline-block;font-size:30px;font-weight:900;'
            'color:#e65100;letter-spacing:-0.5px;'
            'border-bottom:3px solid #e65100;padding-bottom:4px;">'
            + m.group(1) + '</span></div>\n'
        )

    paragraphs = clean_body.split("\n")
    mid = len(paragraphs) // 2
    image2_inserted = False
    para_count = 0

    for i, para in enumerate(paragraphs):
        if not para.strip():
            html += '<div style="margin:10px 0;"></div>\n'
            continue

        if para.strip() == "[SUMMARY_PLACEHOLDER]":
            html += summary_html
            continue

        # 소제목
        if para.startswith("[") and "]" in para:
            heading = para.strip("[]").strip()
            html += (
                '<h2 style="margin-top:48px;margin-bottom:16px;font-size:21px;font-weight:700;'
                'background:linear-gradient(90deg,#e65100,#ef6c00);'
                'color:#fff;padding:12px 20px;border-radius:8px;">'
                + heading + "</h2>\n"
            )
            continue

        # 번호 리스트
        if len(para.strip()) > 1 and para.strip()[0].isdigit() and para.strip()[1] in [".", ")"]:
            html += (
                '<div style="display:flex;align-items:flex-start;margin:10px 0;padding:12px 16px;'
                'background:#fff3e0;border-radius:8px;">'
                '<span style="color:#e65100;font-weight:700;margin-right:12px;font-size:16px;">'
                + para.strip()[0] + '.</span>'
                '<span style="color:#333;font-size:16px;line-height:1.8;">'
                + para.strip()[2:].strip() + '</span></div>\n'
            )
            continue

        # 키워드 처리
        para_count += 1
        processed = keyword_pattern.sub(replace_keyword, para.strip())

        if processed != para.strip():
            html += processed
        elif para_count % 4 == 0 and len(para.strip()) > 30:
            html += (
                '<div style="border-left:4px solid #e65100;padding:14px 20px;margin:20px 0;'
                'background:#fff3e0;border-radius:0 8px 8px 0;">'
                '<p style="margin:0;font-size:16px;line-height:1.9;color:#1a1a1a;font-weight:500;">'
                + para.strip() + '</p></div>\n'
            )
        else:
            html += (
                '<p style="margin:14px 0;line-height:1.9;font-size:16px;color:#333;">'
                + para.strip() + '</p>\n'
            )

        if i >= mid and not image2_inserted and len(images) >= 2:
            html += make_image_html(images[1], margin_top="20px")
            image2_inserted = True

    if len(images) >= 3:
        html += make_image_html(images[2], margin_top="20px")

    return html


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
        raise Exception("토큰 발급 실패: " + response.text)
    return response.json()["access_token"]


def send_telegram(title, post_url, category):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    emoji = CATEGORY_EMOJI.get(category, "📰")
    message = emoji + " 새 포스팅\n\n📌 " + title + "\n\n🔗 " + post_url
    try:
        requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
            timeout=10
        )
        print("[텔레그램] 공유 성공!")
    except Exception as e:
        print("[텔레그램 오류] " + str(e))


def send_facebook(title, post_url, category):
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        return
    emoji = CATEGORY_EMOJI.get(category, "📰")
    message = emoji + " 새 포스팅\n\n" + title + "\n\n자세히 읽기 👉 " + post_url
    try:
        requests.post(
            "https://graph.facebook.com/v19.0/" + FACEBOOK_PAGE_ID + "/feed",
            data={"message": message, "link": post_url, "access_token": FACEBOOK_ACCESS_TOKEN},
            timeout=10
        )
        print("[페이스북] 공유 성공!")
    except Exception as e:
        print("[페이스북 오류] " + str(e))


def post_to_blogger(post_data, images, retry=2):
    print("\n[Blogger] insaplayer 포스팅 시작...")
    category = post_data["category"]
    labels = [category, TODAY]

    for attempt in range(1, retry + 2):
        try:
            access_token = get_access_token()
            body_html = body_to_html(post_data["body"], images, category)
            url = "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts?isDraft=false"
            headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
            payload = {
                "kind": "blogger#post",
                "title": post_data["title"],
                "content": body_html,
                "labels": labels,
                "status": "LIVE"
            }
            print("[시도 " + str(attempt) + "] " + post_data["title"])
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                post_url = response.json().get("url", "")
                print("발행 완료! " + post_url)
                send_telegram(post_data["title"], post_url, category)
                send_facebook(post_data["title"], post_url, category)
                return True
            else:
                print("실패: " + response.text[:200])
                if attempt <= retry:
                    time.sleep(10)
        except Exception as e:
            print("[오류] " + str(e))
            if attempt <= retry:
                time.sleep(10)
    return False


if __name__ == "__main__":
    print("=" * 50)
    print("insaplayer - 오늘의 핫이슈 블로그")
    print("실행 시각: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)
    try:
        post = generate_post()
        keyword_map = {
            "스포츠이슈": "sports korea news",
            "경제뉴스": "economy finance korea",
            "전국이슈": "korea news society",
            "연예이슈": "kpop entertainment korea"
        }
        images = get_images(keyword_map.get(post["category"], "news korea"), count=3)
        post_to_blogger(post, images)
        print("\n모든 작업 완료!")
    except Exception as e:
        print("\n오류 발생: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
