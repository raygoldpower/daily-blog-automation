import os
import requests
import random
from datetime import datetime
import time
import json
import re

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
FACEBOOK_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "")
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN", "")
NAVER_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET", "")
BLOG_ID = "8468892944117983817"

TODAY = datetime.now().strftime("%Y년 %m월 %d일")
TODAY_EN = datetime.now().strftime("%Y-%m-%d")

CATEGORY_EMOJI = {
    "사회이슈": "🔥",
    "경제": "💰",
    "연예": "🎭",
    "스포츠": "⚽",
    "IT과학": "💻",
}

USED_TITLES_FILE = "used_titles2.json"

# 네이버 뉴스 섹션ID 정확한 매핑
# 101=경제, 102=사회, 104=세계, 105=IT/과학, 106=연예, 107=스포츠
NAVER_SECTION_MAP = {
    "사회이슈": "102",
    "경제": "101",
    "연예": "106",
    "스포츠": "107",
    "IT과학": "105",
}

CATEGORY_IMAGE_KEYWORDS = {
    "사회이슈": [
        "city street Korea", "bridge river sunset",
        "crowd walking street blur", "newspaper coffee table", "urban night lights",
    ],
    "경제": [
        "city buildings skyline dusk", "office desk morning coffee",
        "graph chart paper desk", "coins stack blurred background", "busy street people walking",
    ],
    "연예": [
        "stage spotlight empty", "microphone stand concert hall",
        "dark auditorium lights", "music notes blur background", "curtain stage theater",
    ],
    "스포츠": [
        "stadium lights empty seats", "running track morning",
        "sports field grass sunlight", "finish line ribbon", "crowd cheering blur",
    ],
    "IT과학": [
        "computer screen code dark", "server room lights",
        "smartphone technology abstract", "digital circuit board", "laptop coffee workspace",
    ],
}


def load_used_titles():
    try:
        with open(USED_TITLES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_used_title(title):
    used = load_used_titles()
    used.append(title)
    if len(used) > 30:
        used = used[-30:]
    try:
        with open(USED_TITLES_FILE, "w") as f:
            json.dump(used, f, ensure_ascii=False)
    except Exception as e:
        print("[중복방지] 저장 실패: " + str(e))


def is_duplicate(title):
    used = load_used_titles()
    for t in used:
        if title[:10] in t or t[:10] in title:
            return True
    return False


def get_naver_top_news():
    """네이버 분야별 많이 본 뉴스 수집 — 정확한 섹션ID 사용"""
    print("[네이버 많이 본 뉴스] 수집 시작...")

    today_str = datetime.now().strftime("%Y%m%d")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9",
    }

    all_results = []

    for category, section_id in NAVER_SECTION_MAP.items():
        url = (
            "https://news.naver.com/main/ranking/popularDay.naver"
            "?rankingType=popular_day&sectionId=" + section_id + "&date=" + today_str
        )
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                html = response.text

                # 여러 패턴으로 제목 추출 시도
                titles = re.findall(
                    r'class="[^"]*rankingnews[^"]*tit[^"]*"[^>]*>[^<]*<a[^>]*>([^<]+)<', html
                )
                if not titles:
                    titles = re.findall(
                        r'<a[^>]+href="https://n\.news\.naver\.com[^"]*"[^>]*>\s*([^<]{8,80})\s*<', html
                    )
                if not titles:
                    # data-rank 속성 기반 패턴
                    titles = re.findall(
                        r'data-rank="\d+"[^>]*>[^<]*<a[^>]*>([^<]{8,80})<', html
                    )

                # 중복/짧은 제목 제거
                seen = set()
                for title in titles:
                    title = title.strip()
                    if len(title) > 7 and title not in seen:
                        seen.add(title)
                        all_results.append({"category": category, "title": title})
                        print("[" + category + "(" + section_id + ")] " + title[:50])
                        if len([r for r in all_results if r["category"] == category]) >= 5:
                            break

        except Exception as e:
            print("[랭킹 오류] " + category + "(" + section_id + "): " + str(e))

    print("[네이버 많이 본 뉴스] 총 " + str(len(all_results)) + "개 수집")
    return all_results


def get_naver_news_detail(keyword, category):
    """특정 키워드 상세 뉴스 수집"""
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        return []
    try:
        response = requests.get(
            "https://openapi.naver.com/v1/search/news.json",
            headers={
                "X-Naver-Client-Id": NAVER_CLIENT_ID,
                "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
            },
            params={"query": keyword, "display": 5, "sort": "date"},
            timeout=10
        )
        if response.status_code == 200:
            items = response.json().get("items", [])
            results = []
            for item in items:
                title = (item.get("title", "")
                         .replace("<b>", "").replace("</b>", "")
                         .replace("&amp;", "&").replace("&quot;", '"'))
                desc = (item.get("description", "")
                        .replace("<b>", "").replace("</b>", "")
                        .replace("&amp;", "&"))
                if title:
                    results.append(title + ": " + desc)
            print("[네이버 상세] " + str(len(results)) + "개")
            return results
    except Exception as e:
        print("[네이버 상세 오류] " + str(e))
    return []


def get_google_trends():
    """구글 실시간 트렌드 수집"""
    print("[구글 트렌드] 수집 시도...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(
            "https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            titles = re.findall(r'<title><!\[CDATA\[([^\]]+)\]\]></title>', response.text)
            titles = [t for t in titles if t != "Google Trends" and len(t) > 1]
            print("[구글 트렌드] " + str(len(titles)) + "개: " + str(titles[:5]))
            return titles[:10]
    except Exception as e:
        print("[구글 트렌드 오류] " + str(e))
    return []


def select_best_topic(ranking_news, trending_keywords):
    """가장 핫한 이슈 1개 선택"""
    used = load_used_titles()

    # 중복 제거
    filtered = []
    for item in ranking_news:
        title = item["title"]
        is_dup = any(title[:8] in u or u[:8] in title for u in used)
        if not is_dup:
            filtered.append(item)

    if not filtered:
        print("[경고] 모든 랭킹 뉴스 중복 — 초기화")
        filtered = ranking_news

    # 트렌드 키워드와 겹치는 뉴스 우선
    if trending_keywords:
        for item in filtered:
            for keyword in trending_keywords:
                if len(keyword) >= 3 and keyword[:3] in item["title"]:
                    print("[선택] 트렌드 매칭: " + item["title"][:40])
                    return item

    # 상위 5개 중 랜덤 선택
    top = filtered[:5] if len(filtered) >= 5 else filtered
    selected = random.choice(top)
    print("[선택] 랭킹 뉴스 선택: " + selected["title"][:40])
    return selected


def call_gemini(prompt, max_tokens=8000):
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY 없음")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash:generateContent?key=" + GEMINI_API_KEY
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.85,
            "topP": 0.95,
        }
    }

    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, timeout=120)
            print("[Gemini] 응답 상태코드: " + str(response.status_code))

            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    result = "".join(part.get("text", "") for part in parts)
                    return result
                else:
                    raise Exception("Gemini 응답에 candidates 없음: " + str(data))

            elif response.status_code == 429:
                wait = 60 * (attempt + 1)
                print("[429] " + str(wait) + "초 대기 후 재시도...")
                time.sleep(wait)

            elif response.status_code == 503:
                wait = 30 * (attempt + 1)
                print("[503] " + str(wait) + "초 대기 후 재시도...")
                time.sleep(wait)

            else:
                raise Exception("Gemini 오류: " + str(response.status_code) + " " + response.text[:200])

        except Exception as e:
            print("[Gemini 오류] attempt " + str(attempt + 1) + ": " + str(e))
            if attempt < 2:
                time.sleep(20)
            else:
                raise

    raise Exception("Gemini 오류: 최대 재시도 횟수 초과")


def generate_post():
    print("\n[1단계] 네이버 많이 본 뉴스 수집...")
    ranking_news = get_naver_top_news()

    print("\n[2단계] 구글 트렌드 수집...")
    trending_keywords = get_google_trends()

    if not ranking_news:
        print("[경고] 랭킹 뉴스 수집 실패 — 기본값으로 진행")
        selected = {"category": "사회이슈", "title": "오늘의 핫이슈"}
    else:
        selected = select_best_topic(ranking_news, trending_keywords)

    category = selected["category"]
    hot_title = selected["title"]

    print("\n[선택된 이슈] " + hot_title + " (" + category + ")")

    detail_news = get_naver_news_detail(hot_title[:15], category)
    news_context = "=== 오늘(" + TODAY + ") 네이버 많이 본 뉴스 ===\n"
    news_context += "핵심 이슈: " + hot_title + "\n\n"
    if detail_news:
        news_context += "=== 관련 상세 뉴스 ===\n"
        for i, news in enumerate(detail_news[:5]):
            news_context += str(i + 1) + ". " + news + "\n"

    prompt = (
        "당신은 날카로운 시각을 가진 시사 해설 칼럼니스트입니다.\n"
        "사건을 '전달'하는 것이 아니라, 사건의 이면과 의미를 독자에게 '해석'해주는 사람입니다.\n"
        "오늘 네이버에서 실제로 가장 많이 본 뉴스를 기반으로 글을 씁니다.\n"
        "한국어만 사용하세요. 외국 문자 절대 금지.\n\n"

        "오늘 네이버 많이 본 뉴스:\n"
        + news_context + "\n\n"

        "✅ 글쓰기 핵심 원칙:\n"
        "1. 첫 문장은 독자에게 던지는 날카로운 질문 또는 역설적 사실로 시작.\n"
        "2. 팩트는 3줄 이내로 압축. 나머지는 해석과 의미로 채우세요.\n"
        "3. '대부분 언론이 다루지 않는 이면'을 반드시 한 섹션 포함.\n"
        "4. 독자의 일상과 연결되는 지점을 반드시 한 섹션 포함.\n"
        "5. 마지막은 독자에게 생각거리를 던지는 질문으로 마무리.\n"
        "6. 절대 금지: '알아보겠습니다', '살펴보겠습니다', AI 나열식 표현.\n"
        "7. 반드시 존댓말 사용.\n\n"

        "글 구조 (반드시 이 순서로):\n\n"
        "1. 훅 (2~3줄) — 독자를 멈추는 날카로운 질문 또는 역설적 사실\n\n"
        "2. ##핵심키워드## — 이슈의 본질을 한 단어나 짧은 구로 던지고 3~4문장 압축 설명\n\n"
        "3. 소제목 구조 (4개 필수)\n"
        "   [📌 핵심 팩트 — 수치·날짜 포함]\n"
        "   [🔍 왜 지금 이 이슈가 터졌는가]\n"
        "   [💡 대부분이 모르는 이면]\n"
        "   [🙋 나와 무슨 상관인가 — 독자 일상 연결]\n\n"
        "4. 마무리 질문 (2~3줄) — 생각거리 던지며 끝\n\n"
        "5. 핵심 요약\n"
        "[SUMMARY_START]\n"
        "핵심1 (구체적 수치나 팩트)\n"
        "핵심2 (이면 또는 구조적 원인)\n"
        "핵심3 (독자 삶과의 연결)\n"
        "[SUMMARY_END]\n\n"

        "분량: 3000자 이상 4000자 이하. 반드시 완성된 글 출력.\n\n"
        "카테고리: " + category + "\n\n"
        "출력 형식:\n"
        "제목: (실제 이슈의 핵심 팩트 + 해석적 시각 포함. 날짜·카테고리명 금지)\n"
        "---\n"
        "(본문)"
    )

    print("[AI] Gemini 칼럼 작성 중...")
    full_text = call_gemini(prompt, max_tokens=8000)

    lines = full_text.strip().split("\n")
    title = ""
    body_lines = []
    separator_found = False

    for line in lines:
        if line.startswith("제목:"):
            title = line.replace("제목:", "").strip()
        elif not title and "제목" in line and ":" in line:
            title = line.split(":", 1)[-1].strip()
        elif line.strip() == "---":
            separator_found = True
        elif separator_found:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()

    if not title and body_lines:
        for bl in body_lines[:5]:
            if bl.strip() and len(bl.strip()) > 5 and not bl.startswith("["):
                title = bl.strip()[:60]
                break

    if not title:
        title = hot_title[:40] + "... 지금 이슈"

    if not body:
        body = full_text

    if is_duplicate(title):
        print("[중복 감지] 발행 건너뜀: " + title)
        return None

    save_used_title(title)
    print("[완료] 제목: " + title)
    print("[완료] 글자수: " + str(len(body)) + "자")
    return {"title": title, "body": body, "category": category}


def get_images_unsplash(keyword, count=3):
    if not UNSPLASH_ACCESS_KEY:
        return []
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query": keyword,
                "per_page": 10,
                "page": random.randint(1, 5),
                "orientation": "landscape",
                "client_id": UNSPLASH_ACCESS_KEY
            },
            timeout=10
        )
        if response.status_code == 200:
            images = []
            for photo in response.json().get("results", []):
                images.append({
                    "url": photo["urls"]["regular"],
                    "alt": photo.get("alt_description", keyword) or keyword,
                    "author": photo["user"]["name"],
                    "author_url": photo["user"]["links"]["html"],
                    "source": "Unsplash"
                })
            random.shuffle(images)
            return images[:count]
    except Exception as e:
        print("[Unsplash 오류] " + str(e))
    return []


def get_images_pexels(keyword, count=3):
    pexels_key = os.environ.get("PEXELS_API_KEY", "")
    if not pexels_key:
        return []
    try:
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": pexels_key},
            params={"query": keyword, "per_page": count, "orientation": "landscape"},
            timeout=10
        )
        if response.status_code == 200:
            images = []
            for photo in response.json().get("photos", []):
                images.append({
                    "url": photo["src"]["large"],
                    "alt": photo.get("alt", keyword) or keyword,
                    "author": photo["photographer"],
                    "author_url": photo["photographer_url"],
                    "source": "Pexels"
                })
            return images
    except Exception as e:
        print("[Pexels 오류] " + str(e))
    return []


def get_images(category, count=3):
    keywords = CATEGORY_IMAGE_KEYWORDS.get(category, ["city street morning"])
    keyword = random.choice(keywords)
    print("[이미지 검색] 키워드: " + keyword)

    images = get_images_unsplash(keyword, count)
    if images:
        print("[이미지] Unsplash " + str(len(images)) + "장")
        return images

    images = get_images_pexels(keyword, count)
    if images:
        print("[이미지] Pexels " + str(len(images)) + "장")
        return images

    print("[이미지] 모든 소스 실패")
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
    source = img.get("source", "Unsplash")
    html = '<div style="text-align:center;margin:30px 0;margin-top:' + margin_top + ';">'
    html += '<img src="' + img["url"] + '" alt="' + img["alt"] + '" style="max-width:100%;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.12);"/>'
    html += '<p style="font-size:12px;color:#999;margin-top:8px;">Photo by <a href="' + img["author_url"] + '" style="color:#999;">' + img["author"] + '</a> on ' + source + '</p>'
    html += "</div>\n"
    return html


def body_to_html(body, images, category):
    emoji = CATEGORY_EMOJI.get(category, "📰")

    html = (
        '<div style="display:inline-block;background:#e65100;color:#fff;'
        'font-size:13px;padding:5px 14px;border-radius:20px;margin-bottom:8px;font-weight:600;">'
        + emoji + " " + category + "</div>\n"
        '<div style="font-size:13px;color:#888;margin-bottom:20px;">📅 ' + TODAY + "</div>\n"
    )

    if len(images) >= 1:
        html += make_image_html(images[0])

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
    para_count = 0

    for i, para in enumerate(paragraphs):
        if not para.strip():
            html += '<div style="margin:10px 0;"></div>\n'
            continue

        if para.strip() == "[SUMMARY_PLACEHOLDER]":
            html += summary_html
            continue

        if para.startswith("[") and "]" in para:
            heading = para.strip("[]").strip()
            html += (
                '<h2 style="margin-top:48px;margin-bottom:16px;font-size:21px;font-weight:700;'
                'background:linear-gradient(90deg,#e65100,#ef6c00);'
                'color:#fff;padding:12px 20px;border-radius:8px;">'
                + heading + "</h2>\n"
            )
            continue

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

    if len(images) >= 2:
        html += make_image_html(images[1], margin_top="20px")

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
    message = emoji + " " + title + "\n\n자세히 읽기 👉 " + post_url
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
    message = emoji + " " + title + "\n\n자세히 읽기 👉 " + post_url
    try:
        requests.post(
            "https://graph.facebook.com/v19.0/" + FACEBOOK_PAGE_ID + "/feed",
            data={
                "message": message,
                "link": post_url,
                "access_token": FACEBOOK_ACCESS_TOKEN
            },
            timeout=10
        )
        print("[페이스북] 공유 성공!")
    except Exception as e:
        print("[페이스북 오류] " + str(e))


def post_to_blogger(post_data, images, retry=2):
    print("\n[Blogger] insaplayer 포스팅 시작...")
    category = post_data["category"]
    labels = [category, "시사칼럼", "이슈해설", "많이본뉴스"]

    for attempt in range(1, retry + 2):
        try:
            access_token = get_access_token()
            body_html = body_to_html(post_data["body"], images, category)
            url = "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts?isDraft=false"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-Type": "application/json"
            }
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
    print("insaplayer - 네이버 많이 본 뉴스 기반 시사칼럼 v9")
    print("실행 시각: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)

    if not GEMINI_API_KEY:
        print("[오류] GEMINI_API_KEY 없음")
        exit(1)

    try:
        post = generate_post()
        if post is None:
            print("[종료] 중복 감지로 발행 건너뜀")
            exit(0)
        images = get_images(post["category"], count=3)
        post_to_blogger(post, images)
        print("\n모든 작업 완료!")
    except Exception as e:
        print("\n오류 발생: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
