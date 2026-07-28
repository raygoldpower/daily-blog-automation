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

NAVER_SECTION_MAP = {
    "사회이슈": "102",
    "경제": "101",
    "연예": "106",
    "스포츠": "107",
    "IT과학": "105",
}

def clean_url(url):
    """URL에서 ?m=1 및 모바일 파라미터를 완전히 제거하여 표준 URL로 만듭니다."""
    if not url:
        return ""
    return url.split('?m=1')[0].split('&m=1')[0]

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

def crawl_naver_article(article_url):
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

        og_image = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
        if not og_image:
            og_image = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html)
        if og_image:
            img_url = og_image.group(1).strip()
            if img_url and img_url.startswith("http"):
                result["image_url"] = img_url

        publisher = re.search(r'<meta[^>]+property=["\']og:site_name["\'][^>]+content=["\']([^"\']+)["\']', html)
        if not publisher:
            publisher = re.search(r'class="[^"]*press[^"]*"[^>]*>([^<]+)<', html)
        if publisher:
            result["publisher"] = publisher.group(1).strip()

        body_patterns = [
            r'<article[^>]*class="[^"]*go_trans[^"]*"[^>]*>(.*?)</article>',
            r'<div[^>]*id="dic_area"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*article_body[^"]*"[^>]*>(.*?)</div>',
        ]
        for pattern in body_patterns:
            body_match = re.search(pattern, html, re.DOTALL)
            if body_match:
                body_html = body_match.group(1)
                body_text = re.sub(r'<(?!img)[^>]+>', ' ', body_html)
                body_text = re.sub(r'\s+', ' ', body_text).strip()
                body_text = body_text[:2000]
                result["body"] = body_text
                break

        print("[크롤링] 이미지: " + (result["image_url"][:60] if result["image_url"] else "없음"))
        print("[크롤링] 본문: " + str(len(result["body"])) + "자")
        return result

    except Exception as e:
        print("[크롤링 오류] " + str(e))
        return result

def get_naver_top_news():
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

    article_data = {"image_url": "", "image_source": "", "body": "", "publisher": ""}
    related_articles = get_naver_news_with_url(hot_title[:15], category)

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

    news_context = "=== 오늘(" + TODAY + ") 네이버 많이 본 뉴스 ===\n"
    news_context += "핵심 이슈 제목: " + hot_title + "\n"
    if article_data["body"]:
        news_context += "\n=== 기사 원문 내용 ===\n" + article_data["body"] + "\n"

    prompt = (
        "당신은 깊이 있는 분석을 제공하는 전문 시사 칼럼니스트입니다.\n"
        "제공된 기사를 토대로 독창적이고 유용한 칼럼을 작성하세요.\n"
        "단순 뉴스 요약이 아닌, 이 사건이 사회/경제에 미칠 영향과 일반 대중에 주는 시사점을 깊이 있게 분석하세요.\n"
        "한국어만 사용하세요.\n\n"
        "실제 기사 내용:\n" + news_context + "\n\n"
        "글 작성 가이드:\n"
        "1. 자연스럽고 매끄러운 어조(경어체)를 사용하세요.\n"
        "2. '알아보겠습니다', '살펴보겠습니다' 같은 상투적인 AI 표현은 사용하지 마세요.\n"
        "3. 본문 내 무분별한 이모지 사용을 자제하고 깔끔한 문장으로 작성하세요.\n"
        "4. 소제목은 이 이슈만의 특색을 반영하여 창의적으로 지으세요. (소제목 형식: [소제목])\n\n"
        "글 구조:\n"
        "1. 훅 (2~3줄) — 독자를 멈추게 하는 통찰력 있는 첫 문장\n"
        "2. 소제목 3~4개 및 내용\n"
        "3. [SUMMARY_START]\n핵심 요약1\n핵심 요약2\n핵심 요약3\n[SUMMARY_END]\n\n"
        "출력 형식:\n"
        "제목: (검색에 잘 걸리는 매력적인 제목, 날짜/카테고리 표시 금지)\n"
        "---\n"
        "(본문 내용)"
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
    if not title:
        title = hot_title[:40]
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
        "article_url": clean_url(hot_url),
    }

def make_article_image_html(image_url, publisher, article_url, issue_title):
    if not image_url:
        return ""
    source_text = publisher if publisher else "언론사"
    html = '<div style="text-align:center;margin:24px 0;">'
    html += '<img src="' + image_url + '" alt="' + issue_title[:30] + '" style="max-width:100%;border-radius:8px;"/>'
    html += '<p style="font-size:12px;color:#888;margin-top:8px;">'
    html += '© ' + source_text + ' | 보도 인용'
    html += '</p></div>\n'
    return html

def body_to_html(body, post_data):
    category = post_data["category"]
    article_image = post_data.get("article_image", "")
    article_publisher = post_data.get("article_publisher", "")
    article_url = post_data.get("article_url", "")
    issue_title = post_data["title"]

    emoji = CATEGORY_EMOJI.get(category, "📰")

    html = (
        '<div style="font-size:14px;color:#e65100;font-weight:bold;margin-bottom:8px;">'
        + emoji + " " + category + '</div>\n'
    )

    if article_image:
        html += make_article_image_html(article_image, article_publisher, article_url, issue_title)

    summary_pattern = re.compile(r'\[SUMMARY_START\](.*?)\[SUMMARY_END\]', re.DOTALL)
    summary_match = summary_pattern.search(body)
    
    summary_html = ""
    if summary_match:
        lines = [l.strip() for l in summary_match.group(1).strip().split("\n") if l.strip()]
        summary_html = '<blockquote style="background:#f9f9f9;border-left:4px solid #e65100;padding:12px 16px;margin:20px 0;">'
        summary_html += '<strong>📌 핵심 포인트</strong><ul style="margin:8px 0 0 0;padding-left:20px;">'
        for line in lines:
            summary_html += '<li>' + line + '</li>'
        summary_html += '</ul></blockquote>\n'

    clean_body = summary_pattern.sub("", body)

    paragraphs = clean_body.split("\n")
    for para in paragraphs:
        p = para.strip()
        if not p:
            continue
        if p.startswith("[") and "]" in p:
            heading = p.strip("[]").strip()
            html += f'<h2 style="margin-top:32px;font-size:20px;color:#222;border-bottom:2px solid #f0f0f0;padding-bottom:8px;">{heading}</h2>\n'
        else:
            html += f'<p style="line-height:1.8;font-size:16px;color:#333;margin:16px 0;">{p}</p>\n'

    if summary_html:
        html += summary_html

    if article_url:
        html += f'<p style="font-size:13px;color:#888;margin-top:30px;">출처 및 참고 기사: <a href="{article_url}" target="_blank" rel="noopener">{article_url}</a></p>'

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
    clean_post_url = clean_url(post_url)
    emoji = CATEGORY_EMOJI.get(category, "📰")
    message = emoji + " " + title + "\n\n자세히 읽기 👉 " + clean_post_url
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
    clean_post_url = clean_url(post_url)
    emoji = CATEGORY_EMOJI.get(category, "📰")
    message = emoji + " " + title + "\n\n자세히 읽기 👉 " + clean_post_url
    try:
        r = requests.post(
            "https://graph.facebook.com/v19.0/" + FACEBOOK_PAGE_ID + "/feed",
            data={"message": message, "link": clean_post_url, "access_token": FACEBOOK_ACCESS_TOKEN},
            timeout=10
        )
        if r.status_code == 200:
            print("[페이스북] 공유 성공!")
        else:
            print("[페이스북] 실패: " + r.text[:200])
    except Exception as e:
        print("[페이스북 오류] " + str(e))

def post_to_blogger(post_data, retry=2):
    print("\n[Blogger] 블로그 포스팅 시작...")
    category = post_data["category"]
    labels = [category]

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
                raw_post_url = response.json().get("url", "")
                post_url = clean_url(raw_post_url)
                print("발행 완료! (표준 URL): " + post_url)
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
    print("블로그 자동 포스팅 엔진 (SEO 최적화 적용 버전)")
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
