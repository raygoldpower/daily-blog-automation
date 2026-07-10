import os
import requests
import random
from datetime import datetime
import time
import json
import re

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
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
USED_IMAGES_FILE = "used_images2.json"

# 네이버 뉴스 섹션ID 정확한 매핑
NAVER_SECTION_MAP = {
    "사회이슈": "102",
    "경제": "101",
    "연예": "106",
    "스포츠": "107",
    "IT과학": "105",
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
    return any(title[:10] in t or t[:10] in title for t in used)


def load_used_images():
    try:
        with open(USED_IMAGES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_used_image(url):
    used = load_used_images()
    if url not in used:
        used.append(url)
    if len(used) > 100:
        used = used[-100:]
    try:
        with open(USED_IMAGES_FILE, "w") as f:
            json.dump(used, f, ensure_ascii=False)
    except Exception:
        pass


# ──────────────────────────────────────────────
# ✅ 핵심 1: 네이버 뉴스 기사 원문 크롤링
#    → 실제 내용 + 대표 이미지 추출
# ──────────────────────────────────────────────
def crawl_naver_article(article_url):
    """네이버 뉴스 기사 원문 크롤링 — 본문 + 대표 이미지"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://news.naver.com",
        "Accept-Language": "ko-KR,ko;q=0.9",
    }
    result = {"image_url": "", "image_source": "", "body": "", "publisher": ""}
    try:
        response = requests.get(article_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return result
        html = response.text

        # 대표 이미지 추출 (og:image 우선)
        og_image = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
        if not og_image:
            og_image = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html)
        if og_image:
            img_url = og_image.group(1).strip()
            if img_url and img_url.startswith("http"):
                result["image_url"] = img_url

        # 언론사명 추출
        publisher = re.search(r'<meta[^>]+property=["\']og:site_name["\'][^>]+content=["\']([^"\']+)["\']', html)
        if not publisher:
            publisher = re.search(r'class="[^"]*press[^"]*"[^>]*>([^<]+)<', html)
        if publisher:
            result["publisher"] = publisher.group(1).strip()

        # 기사 본문 추출 (네이버 뉴스 구조)
        body_patterns = [
            r'<article[^>]*class="[^"]*go_trans[^"]*"[^>]*>(.*?)</article>',
            r'<div[^>]*id="dic_area"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*article_body[^"]*"[^>]*>(.*?)</div>',
        ]
        for pattern in body_patterns:
            body_match = re.search(pattern, html, re.DOTALL)
            if body_match:
                body_html = body_match.group(1)
                # HTML 태그 제거, 이미지 태그만 남기기
                body_text = re.sub(r'<(?!img)[^>]+>', ' ', body_html)
                body_text = re.sub(r'\s+', ' ', body_text).strip()
                body_text = body_text[:2000]  # 최대 2000자
                result["body"] = body_text
                break

        print("[크롤링] 이미지: " + (result["image_url"][:60] if result["image_url"] else "없음"))
        print("[크롤링] 본문: " + str(len(result["body"])) + "자")
        return result

    except Exception as e:
        print("[크롤링 오류] " + str(e))
        return result


def get_naver_top_news():
    """네이버 분야별 많이 본 뉴스 수집 + 기사 URL 함께 수집"""
    print("[네이버 많이 본 뉴스] 수집 시작...")
    today_str = datetime.now().strftime("%Y%m%d")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
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

                # 제목 + URL 동시 추출
                links = re.findall(
                    r'<a[^>]+href="(https://n\.news\.naver\.com/[^"]+)"[^>]*>\s*([^<]{8,80})\s*</a>',
                    html
                )

                seen_titles = set()
                for link_url, title in links:
                    title = title.strip()
                    if len(title) > 7 and title not in seen_titles:
                        seen_titles.add(title)
                        all_results.append({
                            "category": category,
                            "title": title,
                            "url": link_url
                        })
                        print("[" + category + "] " + title[:45])
                        if len([r for r in all_results if r["category"] == category]) >= 5:
                            break

        except Exception as e:
            print("[랭킹 오류] " + category + ": " + str(e))

    print("[수집 완료] 총 " + str(len(all_results)) + "개")
    return all_results


def get_naver_news_with_url(keyword, category):
    """네이버 검색 API로 관련 기사 URL 포함 수집"""
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
                original_url = item.get("originallink", "") or item.get("link", "")
                naver_url = item.get("link", "")
                results.append({
                    "title": title,
                    "desc": desc,
                    "url": naver_url if "news.naver.com" in naver_url else original_url,
                    "original_url": original_url
                })
            return results
    except Exception as e:
        print("[네이버 검색 오류] " + str(e))
    return []


def get_google_trends():
    """구글 실시간 트렌드 수집"""
    try:
        response = requests.get(
            "https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        if response.status_code == 200:
            titles = re.findall(r'<title><!\[CDATA\[([^\]]+)\]\]></title>', response.text)
            titles = [t for t in titles if t != "Google Trends" and len(t) > 1]
            return titles[:10]
    except Exception as e:
        print("[구글 트렌드 오류] " + str(e))
    return []


def select_best_topic(ranking_news, trending_keywords):
    used = load_used_titles()
    filtered = [
        item for item in ranking_news
        if not any(item["title"][:8] in u or u[:8] in item["title"] for u in used)
    ]
    if not filtered:
        filtered = ranking_news

    if trending_keywords:
        for item in filtered:
            for keyword in trending_keywords:
                if len(keyword) >= 3 and keyword[:3] in item["title"]:
                    print("[선택] 트렌드 매칭: " + item["title"][:40])
                    return item

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
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.85, "topP": 0.95}
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
                    return "".join(part.get("text", "") for part in parts)
                raise Exception("candidates 없음")
            elif response.status_code in [429, 503]:
                wait = 30 * (attempt + 1)
                print("[" + str(response.status_code) + "] " + str(wait) + "초 대기...")
                time.sleep(wait)
            else:
                raise Exception("Gemini 오류: " + str(response.status_code))
        except Exception as e:
            print("[Gemini 오류] attempt " + str(attempt + 1) + ": " + str(e))
            if attempt < 2:
                time.sleep(20)
            else:
                raise
    raise Exception("Gemini 최대 재시도 초과")


def generate_post():
    print("\n[1단계] 네이버 많이 본 뉴스 수집...")
    ranking_news = get_naver_top_news()

    print("\n[2단계] 구글 트렌드 수집...")
    trending_keywords = get_google_trends()

    if not ranking_news:
        print("[경고] 랭킹 뉴스 수집 실패")
        return None

    selected = select_best_topic(ranking_news, trending_keywords)
    category = selected["category"]
    hot_title = selected["title"]
    hot_url = selected.get("url", "")

    print("\n[선택된 이슈] " + hot_title + " (" + category + ")")

    # ✅ 핵심: 기사 원문 크롤링
    article_data = {"image_url": "", "image_source": "", "body": "", "publisher": ""}
    related_articles = get_naver_news_with_url(hot_title[:15], category)

    # 원문 기사 크롤링 시도 (랭킹 URL 우선, 검색 결과 보조)
    crawl_targets = []
    if hot_url:
        crawl_targets.append({"url": hot_url, "publisher": ""})
    for art in related_articles[:3]:
        if art["url"]:
            crawl_targets.append({"url": art["url"], "publisher": ""})

    used_images = load_used_images()
    for target in crawl_targets:
        crawled = crawl_naver_article(target["url"])
        if crawled["image_url"] and crawled["image_url"] not in used_images:
            article_data = crawled
            save_used_image(crawled["image_url"])
            print("[이미지 확보] " + crawled["image_url"][:60])
            break
        elif crawled["body"] and not article_data["body"]:
            article_data["body"] = crawled["body"]
            article_data["publisher"] = crawled["publisher"]

    # 뉴스 컨텍스트 구성 (실제 기사 내용 포함)
    news_context = "=== 오늘(" + TODAY + ") 네이버 많이 본 뉴스 ===\n"
    news_context += "핵심 이슈 제목: " + hot_title + "\n"
    if article_data["body"]:
        news_context += "\n=== 기사 원문 내용 ===\n" + article_data["body"] + "\n"
    if related_articles:
        news_context += "\n=== 관련 기사 ===\n"
        for i, art in enumerate(related_articles[:4]):
            news_context += str(i+1) + ". " + art["title"] + ": " + art["desc"][:100] + "\n"

    # Gemini 칼럼 작성 (실제 기사 내용 기반)
    prompt = (
        "당신은 날카로운 시각을 가진 시사 해설 칼럼니스트입니다.\n"
        "아래 실제 기사 원문 내용을 반드시 기반으로 글을 쓰세요.\n"
        "원문에 없는 내용을 상상해서 쓰지 마세요. 팩트는 원문 기준으로만.\n"
        "한국어만 사용하세요.\n\n"
        "실제 기사 내용:\n" + news_context + "\n\n"
        "✅ 글쓰기 원칙:\n"
        "1. 첫 문장은 날카로운 질문 또는 역설적 사실로 시작.\n"
        "2. 팩트는 원문 기반으로만 정확하게. 추측 금지.\n"
        "3. '대부분 언론이 다루지 않는 이면'을 한 섹션 포함.\n"
        "4. 독자 일상과 연결되는 지점 한 섹션 포함.\n"
        "5. 마지막은 독자에게 생각거리를 던지는 질문으로 마무리.\n"
        "6. 절대 금지: '알아보겠습니다', '살펴보겠습니다', AI 나열식.\n"
        "7. 반드시 존댓말.\n\n"
        "글 구조:\n"
        "1. 훅 (2~3줄)\n"
        "2. ##핵심키워드##\n"
        "3. [📌 핵심 팩트 — 수치·날짜 포함]\n"
        "   [🔍 왜 지금 이 이슈가 터졌는가]\n"
        "   [💡 대부분이 모르는 이면]\n"
        "   [🙋 나와 무슨 상관인가]\n"
        "4. 마무리 질문 (2~3줄)\n"
        "5. [SUMMARY_START]\n핵심1\n핵심2\n핵심3\n[SUMMARY_END]\n\n"
        "분량: 3000자 이상. 반드시 완성된 글.\n"
        "카테고리: " + category + "\n\n"
        "출력:\n제목: (핵심 팩트 + 해석적 시각. 날짜·카테고리명 금지)\n---\n(본문)"
    )

    print("[AI] Gemini 칼럼 작성 중 (실제 기사 기반)...")
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
    if not title:
        title = hot_title[:40] + " — 지금 이슈"
    if not body:
        body = full_text

    if is_duplicate(title):
        print("[중복] 발행 건너뜀: " + title)
        return None

    save_used_title(title)
    print("[완료] 제목: " + title)
    print("[완료] 글자수: " + str(len(body)) + "자")

    return {
        "title": title,
        "body": body,
        "category": category,
        "article_image": article_data.get("image_url", ""),
        "article_publisher": article_data.get("publisher", ""),
        "article_url": hot_url,
    }


# ──────────────────────────────────────────────
# ✅ 핵심 2: 기사 원문 이미지 사용 + 저작권 방패
#    출처 명시 = 보도 목적 인용 (합법적 사용)
# ──────────────────────────────────────────────
def make_article_image_html(image_url, publisher, article_url, issue_title):
    """기사 원문 이미지 + 출처 명시 (저작권 방패)"""
    if not image_url:
        return ""
    source_text = publisher if publisher else "언론사"
    html = '<div style="text-align:center;margin:24px 0;">'
    html += '<img src="' + image_url + '" alt="' + issue_title[:30] + '" style="max-width:100%;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.15);"/>'
    html += '<p style="font-size:12px;color:#999;margin-top:8px;">'
    html += '© ' + source_text + ' | 보도 목적 인용 | '
    if article_url:
        html += '<a href="' + article_url + '" style="color:#999;" target="_blank" rel="noopener">원문 기사 보기</a>'
    html += '</p></div>\n'
    return html


def make_summary_html(summary_text):
    lines = [l.strip() for l in summary_text.strip().split("\n") if l.strip()]
    html = '<div style="background:#fff8e1;border-left:5px solid #f57f17;border-radius:8px;padding:20px 24px;margin:28px 0;">'
    html += '<p style="font-weight:700;font-size:17px;color:#f57f17;margin-bottom:12px;">📌 핵심 요약</p>'
    for line in lines:
        html += '<p style="margin:6px 0;font-size:15px;color:#333;">✅ ' + line + "</p>"
    html += "</div>\n"
    return html


def body_to_html(body, post_data):
    category = post_data["category"]
    article_image = post_data.get("article_image", "")
    article_publisher = post_data.get("article_publisher", "")
    article_url = post_data.get("article_url", "")
    issue_title = post_data["title"]

    emoji = CATEGORY_EMOJI.get(category, "📰")

    html = (
        '<div style="display:inline-block;background:#e65100;color:#fff;'
        'font-size:13px;padding:5px 14px;border-radius:20px;margin-bottom:8px;font-weight:600;">'
        + emoji + " " + category + "</div>\n"
        '<div style="font-size:13px;color:#888;margin-bottom:20px;">📅 ' + TODAY + "</div>\n"
    )

    # ✅ 기사 원문 이미지 (출처 명시)
    if article_image:
        html += make_article_image_html(article_image, article_publisher, article_url, issue_title)
    
    # 원본 기사 링크 박스
    if article_url:
        html += (
            '<div style="background:#f5f5f5;border-left:4px solid #e65100;'
            'padding:12px 16px;margin:16px 0;border-radius:0 8px 8px 0;">'
            '<p style="margin:0;font-size:13px;color:#666;">📰 이 글은 실제 보도된 뉴스를 기반으로 작성된 시사 해설입니다. '
            '<a href="' + article_url + '" target="_blank" rel="noopener" style="color:#e65100;font-weight:600;">원문 기사 보기 →</a></p>'
            '</div>\n'
        )

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

    for para in paragraphs:
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
            data={"message": message, "link": post_url, "access_token": FACEBOOK_ACCESS_TOKEN},
            timeout=10
        )
        print("[페이스북] 공유 성공!")
    except Exception as e:
        print("[페이스북 오류] " + str(e))


def post_to_blogger(post_data, retry=2):
    print("\n[Blogger] insaplayer 포스팅 시작...")
    category = post_data["category"]
    labels = [category, "시사칼럼", "이슈해설", "많이본뉴스"]

    for attempt in range(1, retry + 2):
        try:
            access_token = get_access_token()
            body_html = body_to_html(post_data["body"], post_data)
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
    print("insaplayer - 기사 원문 기반 시사칼럼 v10")
    print("실행 시각: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)

    if not GEMINI_API_KEY:
        print("[오류] GEMINI_API_KEY 없음")
        exit(1)

    try:
        post = generate_post()
        if post is None:
            print("[종료] 중복 또는 수집 실패")
            exit(0)
        post_to_blogger(post)
        print("\n모든 작업 완료!")
    except Exception as e:
        print("\n오류 발생: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
