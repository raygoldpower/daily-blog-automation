import os
import requests
import random
from datetime import datetime
import time
import json

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
GOOGLE_SEARCH_API_KEY = os.environ.get("GOOGLE_SEARCH_API_KEY", "")
GOOGLE_SEARCH_ENGINE_ID = os.environ.get("GOOGLE_SEARCH_ENGINE_ID", "")
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "")
BLOG_ID = "8468892944117983817"

TODAY = datetime.now().strftime("%Y년 %m월 %d일")
TODAY_EN = datetime.now().strftime("%Y-%m-%d")

CATEGORY_EMOJI = {
    "스포츠이슈": "⚽",
    "경제뉴스": "💰",
    "전국이슈": "🌍",
    "연예이슈": "🎭"
}

CATEGORIES = ["스포츠이슈", "경제뉴스", "전국이슈", "연예이슈"]

USED_TITLES_FILE = "used_titles2.json"


# ──────────────────────────────────────────────
# ✅ 이미지 키워드: 이슈/인물과 완전히 분리된
#    중립적 분위기 키워드만 사용 (저작권 리스크 제거)
# ──────────────────────────────────────────────
CATEGORY_IMAGE_KEYWORDS = {
    "스포츠이슈": [
        "stadium lights empty seats",
        "running track morning",
        "sports field grass sunlight",
        "finish line ribbon",
        "crowd cheering blur",
    ],
    "경제뉴스": [
        "city buildings skyline dusk",
        "office desk morning coffee",
        "graph chart paper desk",
        "coins stack blurred background",
        "busy street people walking",
    ],
    "전국이슈": [
        "city street Korea",
        "bridge river sunset",
        "crowd walking street blur",
        "newspaper coffee table",
        "urban night lights",
    ],
    "연예이슈": [
        "stage spotlight empty",
        "microphone stand concert hall",
        "dark auditorium lights",
        "music notes blur background",
        "curtain stage theater",
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


CATEGORY_KEYWORDS = {
    "스포츠이슈": {
        "naver": ["스포츠 이슈 오늘", "축구 뉴스 오늘", "야구 오늘", "농구 뉴스", "스포츠 선수 이슈"],
        "google": ["korea sports news today", "한국 스포츠 이슈"],
        "newsapi": ["korea sports international", "korean athlete world news"]
    },
    "경제뉴스": {
        "naver": ["경제 뉴스 오늘", "코스피 오늘", "부동산 뉴스", "환율 오늘", "주식 이슈"],
        "google": ["korea economy news today", "한국 경제 이슈"],
        "newsapi": ["korea economy global", "korean market international"]
    },
    "전국이슈": {
        "naver": ["오늘 사회 이슈", "정치 뉴스 오늘", "사건사고 오늘", "핫이슈 오늘", "전국 뉴스"],
        "google": ["korea news today", "한국 사회 이슈"],
        "newsapi": ["korea society global reaction", "south korea world news"]
    },
    "연예이슈": {
        "naver": ["연예 뉴스 오늘", "K팝 이슈", "드라마 화제", "아이돌 뉴스", "연예인 이슈"],
        "google": ["kpop news today", "한국 연예 이슈"],
        "newsapi": ["kpop global reaction", "korean entertainment worldwide"]
    }
}


def search_naver_news(query, display=5):
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        return []
    try:
        response = requests.get(
            "https://openapi.naver.com/v1/search/news.json",
            headers={
                "X-Naver-Client-Id": NAVER_CLIENT_ID,
                "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
            },
            params={"query": query, "display": display, "sort": "date"},
            timeout=10
        )
        if response.status_code == 200:
            items = response.json().get("items", [])
            results = []
            for item in items:
                title = item.get("title", "").replace("<b>", "").replace("</b>", "")
                desc = item.get("description", "").replace("<b>", "").replace("</b>", "")
                results.append(title + ": " + desc)
            print("[네이버] " + str(len(results)) + "개 수집")
            return results
    except Exception as e:
        print("[네이버 오류] " + str(e))
    return []


def search_google_news(query, num=3):
    if not GOOGLE_SEARCH_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        return []
    try:
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": GOOGLE_SEARCH_API_KEY,
                "cx": GOOGLE_SEARCH_ENGINE_ID,
                "q": query + " " + TODAY_EN,
                "num": num,
                "dateRestrict": "d1"
            },
            timeout=10
        )
        if response.status_code == 200:
            items = response.json().get("items", [])
            results = []
            for item in items:
                results.append(item.get("title", "") + ": " + item.get("snippet", ""))
            print("[구글] " + str(len(results)) + "개 수집")
            return results
    except Exception as e:
        print("[구글 오류] " + str(e))
    return []


def search_newsapi(query, page_size=3):
    if not NEWSAPI_KEY:
        return []
    try:
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": query,
                "sortBy": "publishedAt",
                "pageSize": page_size,
                "from": TODAY_EN,
                "apiKey": NEWSAPI_KEY
            },
            timeout=10
        )
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            results = []
            for article in articles:
                title = article.get("title", "") or ""
                desc = article.get("description", "") or ""
                results.append(title + ": " + desc)
            print("[NewsAPI] " + str(len(results)) + "개 수집")
            return results
    except Exception as e:
        print("[NewsAPI 오류] " + str(e))
    return []


def collect_news(category):
    print("[뉴스 수집] 카테고리: " + category)
    keywords = CATEGORY_KEYWORDS[category]

    naver_query1 = random.choice(keywords["naver"])
    remaining = [k for k in keywords["naver"] if k != naver_query1]
    naver_query2 = random.choice(remaining) if remaining else naver_query1
    google_query = random.choice(keywords["google"])
    newsapi_query = random.choice(keywords["newsapi"])

    naver_results1 = search_naver_news(naver_query1, display=5)
    naver_results2 = search_naver_news(naver_query2, display=3)
    google_results = search_google_news(google_query, num=3)
    newsapi_results = search_newsapi(newsapi_query, page_size=3)

    all_news = naver_results1 + naver_results2 + google_results + newsapi_results

    if not all_news:
        print("[경고] 뉴스 수집 실패 - 기본 뉴스 컨텍스트로 진행")
        return "=== 오늘(" + TODAY + ") 뉴스 수집 실패 - 최신 이슈로 작성 요청 ==="

    news_context = "=== 오늘(" + TODAY + ") 수집된 뉴스 ===\n"
    for i, news in enumerate(all_news[:5]):
        news_context += str(i + 1) + ". " + news + "\n"

    print("[수집 완료] 총 " + str(len(all_news)) + "개")
    return news_context


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
                    result = ""
                    for part in parts:
                        result += part.get("text", "")
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


def test_apis():
    print("[API 확인] GEMINI_API_KEY: " + ("있음" if GEMINI_API_KEY else "없음"))
    print("[API 확인] NAVER_CLIENT_ID: " + ("있음" if os.environ.get("NAVER_CLIENT_ID") else "없음"))
    print("[API 확인] GOOGLE_SEARCH_API_KEY: " + ("있음" if os.environ.get("GOOGLE_SEARCH_API_KEY") else "없음"))
    print("[API 확인] NEWSAPI_KEY: " + ("있음" if os.environ.get("NEWSAPI_KEY") else "없음"))
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY 없음 — GitHub Secrets 및 yml 확인 필요")


# ──────────────────────────────────────────────
# ✅ 핵심 변경: 프롬프트 전면 교체
#    - 페르소나: 기자 → 시사 해설 칼럼니스트
#    - 구조: 사건 나열 → 훅 질문 + 해석 + 이면 + 독자 연결
#    - 금지: "중립 객관" 강제 제거 → 해석과 관점 허용
# ──────────────────────────────────────────────
def generate_post():
    category = random.choice(CATEGORIES)
    print("[카테고리] " + category)

    news_context = collect_news(category)

    prompt = (
        "당신은 날카로운 시각을 가진 시사 해설 칼럼니스트입니다.\n"
        "사건을 '전달'하는 것이 아니라, 사건의 이면과 의미를 독자에게 '해석'해주는 사람입니다.\n"
        "독자가 다 읽고 나서 '이런 시각은 처음 봤다'고 느끼게 만드는 글을 씁니다.\n"
        "한국어만 사용하세요. 외국 문자 절대 금지.\n\n"

        "✅ 글쓰기 핵심 원칙:\n"
        "1. 첫 문장은 독자에게 던지는 날카로운 질문 또는 역설적 사실로 시작하세요.\n"
        "   예: '우리는 이 뉴스를 왜 이렇게 빨리 잊을까요?'\n"
        "   예: '승리했지만, 아무도 박수를 치지 않았습니다.'\n"
        "2. 팩트는 3줄 이내로 압축. 나머지 공간은 해석과 의미로 채우세요.\n"
        "3. '대부분 언론이 다루지 않는 이면'을 반드시 한 섹션 포함하세요.\n"
        "4. 독자의 일상과 연결되는 지점을 반드시 한 섹션 포함하세요.\n"
        "   (예: 이 경제 이슈가 내 월급·집값·소비에 어떤 영향을 주는가)\n"
        "5. 마지막은 '~될 것입니다' 결론 금지. 독자에게 생각거리를 던지는 질문으로 마무리.\n"
        "6. 문장 리듬: 짧은 문장 → 긴 문장 → 짧은 문장으로 변화를 주세요.\n"
        "7. 절대 금지: '~알아보겠습니다', '~살펴보겠습니다', '중요합니다', AI 나열식 표현.\n"
        "8. 반드시 존댓말. '~이다', '~한다' 반말 종결 절대 금지.\n\n"

        "아래는 오늘(" + TODAY + ") 실제 수집된 뉴스입니다:\n"
        + news_context + "\n\n"

        "위 뉴스 중 가장 사람들이 궁금해할 이슈 하나를 선택해서 칼럼을 작성하세요.\n"
        "단순 사실 나열이 절대 아닙니다. 이 사건이 왜 일어났는지, 무엇을 의미하는지,\n"
        "우리 삶과 어떻게 연결되는지를 풀어내야 합니다.\n\n"

        "절대 지켜야 할 원칙:\n"
        "1. 공식 확인된 팩트 기반으로 작성. 단, 해석과 분석은 적극적으로.\n"
        "2. 명예훼손 절대 금지.\n"
        "3. 제목과 내용 일치. 낚시성 제목 금지.\n"
        "4. 각 소제목 아래 최소 5문장 이상.\n"
        "5. 절대로 글을 중간에 끊거나 생략하지 말 것. 반드시 완성된 글 출력.\n\n"

        "글 구조 (반드시 이 순서로):\n\n"
        "1. 훅 (2~3줄)\n"
        "   독자를 멈추는 날카로운 질문 또는 역설적 사실. 이 글을 왜 읽어야 하는지 암시.\n\n"
        "2. ##핵심키워드##\n"
        "   이슈의 본질을 한 단어나 짧은 구로 던지세요. 아래 3~4문장으로 압축 설명.\n\n"
        "3. 소제목 구조 (4개 필수)\n"
        "   소제목 형식: [이모지 소제목내용 이모지]\n"
        "   ① [📌 핵심 팩트 📌] — 수치·날짜 포함, 3~4문장으로 압축\n"
        "   ② [🔍 왜 지금인가 🔍] — 이 이슈가 지금 터진 배경과 맥락\n"
        "   ③ [💡 대부분이 모르는 이면 💡] — 언론이 잘 다루지 않는 시각, 구조적 원인\n"
        "   ④ [🙋 나와 무슨 상관인가 🙋] — 독자 일상(돈·직업·소비·관계)과의 연결\n\n"
        "4. 마무리 질문 (2~3줄)\n"
        "   독자에게 하나의 생각거리를 던지며 끝. '~될 것입니다' 식 결론 절대 금지.\n\n"
        "5. 핵심 요약\n"
        "[SUMMARY_START]\n"
        "핵심1 (구체적 수치나 팩트)\n"
        "핵심2 (이면 또는 구조적 원인)\n"
        "핵심3 (독자 삶과의 연결 또는 생각거리)\n"
        "[SUMMARY_END]\n\n"

        "분량: 반드시 3000자 이상 4000자 이하.\n"
        "절대로 글을 중간에 끊지 말고 반드시 완성된 문장으로 마무리하세요.\n\n"
        "카테고리: " + category + "\n\n"
        "출력 형식:\n"
        "제목: (첫 줄에 '제목: '으로 시작. 실제 이슈의 핵심 팩트 + 해석적 시각 포함.\n"
        "       날짜·카테고리명·'핫이슈' 같은 일반어 절대 금지.\n"
        "       예시 스타일: '웸반야마가 MVP보다 더 위험한 이유'\n"
        "                    '금리 동결, 서민에게는 왜 기쁜 소식이 아닌가')\n"
        "---\n"
        "(본문 시작 — 훅부터 바로 작성. 반드시 완성된 전체 글 출력)"
    )

    print("[AI] Gemini 2.5 Flash 칼럼 작성 중...")
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
        print("[경고] 제목 파싱 실패 — 재추출 시도")
        title_prompt = (
            "다음 글에서 제목만 한 줄로 추출하세요. "
            "날짜나 카테고리명 포함 금지:\n\n" + full_text[:500]
        )
        try:
            title = call_gemini(title_prompt, max_tokens=100).strip().split("\n")[0]
            title = title.replace("제목:", "").strip()
        except Exception:
            title = category + " 칼럼 " + datetime.now().strftime("%H%M")

    if not body:
        body = full_text

    if is_duplicate(title):
        print("[중복 감지] 제목 중복 — 발행 건너뜀: " + title)
        return None

    save_used_title(title)
    print("[완료] 제목: " + title)
    print("[완료] 글자수: " + str(len(body)) + "자")
    return {"title": title, "body": body, "category": category}


# ──────────────────────────────────────────────
# ✅ 핵심 변경: 이미지 키워드를 이슈/인물과 완전 분리
#    - 카테고리별 중립 분위기 키워드 풀에서 랜덤 선택
#    - 특정 인물·사건명 키워드 → 저작권/초상권 리스크 제거
# ──────────────────────────────────────────────
def get_image_keyword(category):
    keywords = CATEGORY_IMAGE_KEYWORDS.get(category, ["city street morning"])
    chosen = random.choice(keywords)
    print("[이미지 키워드] " + chosen + " (카테고리 기반 중립 키워드)")
    return chosen


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


def get_images_pixabay(keyword, count=3):
    pixabay_key = os.environ.get("PIXABAY_API_KEY", "")
    if not pixabay_key:
        return []
    try:
        response = requests.get(
            "https://pixabay.com/api/",
            params={
                "key": pixabay_key,
                "q": keyword,
                "image_type": "photo",
                "orientation": "horizontal",
                "per_page": count,
                "safesearch": "true"
            },
            timeout=10
        )
        if response.status_code == 200:
            images = []
            for hit in response.json().get("hits", []):
                images.append({
                    "url": hit["webformatURL"],
                    "alt": keyword,
                    "author": hit["user"],
                    "author_url": "https://pixabay.com/users/" + hit["user"] + "-" + str(hit["user_id"]),
                    "source": "Pixabay"
                })
            return images
    except Exception as e:
        print("[Pixabay 오류] " + str(e))
    return []


def get_images(keyword, count=3, title="", category=""):
    # title 파라미터는 더 이상 키워드 생성에 사용하지 않음 (저작권 리스크 차단)
    keyword = get_image_keyword(category)
    print("[이미지 검색] 키워드: " + keyword)

    images = get_images_unsplash(keyword, count)
    if images:
        print("[이미지] Unsplash " + str(len(images)) + "장")
        return images

    images = get_images_pexels(keyword, count)
    if images:
        print("[이미지] Pexels " + str(len(images)) + "장")
        return images

    images = get_images_pixabay(keyword, count)
    if images:
        print("[이미지] Pixabay " + str(len(images)) + "장")
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
    import re

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


def request_google_indexing(post_url):
    import json as json_lib, time, base64
    service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if not service_account_json:
        print("[색인] GOOGLE_SERVICE_ACCOUNT_JSON 없음 - 건너뜀")
        return
    try:
        sa_info = json_lib.loads(service_account_json)
        now = int(time.time())
        header = base64.urlsafe_b64encode(
            json_lib.dumps({"alg": "RS256", "typ": "JWT"}).encode()
        ).rstrip(b"=").decode()
        payload_data = {
            "iss": sa_info["client_email"],
            "scope": "https://www.googleapis.com/auth/indexing",
            "aud": "https://oauth2.googleapis.com/token",
            "exp": now + 3600,
            "iat": now
        }
        payload_b64 = base64.urlsafe_b64encode(
            json_lib.dumps(payload_data).encode()
        ).rstrip(b"=").decode()
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
        private_key = serialization.load_pem_private_key(
            sa_info["private_key"].encode(), password=None
        )
        sign_input = (header + "." + payload_b64).encode()
        signature = private_key.sign(sign_input, padding.PKCS1v15(), hashes.SHA256())
        jwt_token = header + "." + payload_b64 + "." + base64.urlsafe_b64encode(signature).rstrip(b"=").decode()
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt_token},
            timeout=10
        )
        if token_response.status_code != 200:
            print("[색인] 토큰 발급 실패: " + token_response.text[:200])
            return
        access_token = token_response.json().get("access_token", "")
        index_response = requests.post(
            "https://indexing.googleapis.com/v3/urlNotifications:publish",
            headers={"Authorization": "Bearer " + access_token, "Content-Type": "application/json"},
            json={"url": post_url, "type": "URL_UPDATED"},
            timeout=10
        )
        if index_response.status_code == 200:
            print("[색인] 구글 색인 요청 완료! ✅ " + post_url)
        else:
            print("[색인] 색인 요청 실패: " + index_response.text[:200])
    except Exception as e:
        print("[색인 오류] " + str(e))


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
    # ✅ 태그: 날짜 제거, 의미 있는 키워드만
    labels = [category, "시사칼럼", "이슈해설"]

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
                request_google_indexing(post_url)
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
    print("insaplayer - 시사해설 칼럼 블로그 v7 (Gemini 2.5 Flash + 칼럼니스트 프롬프트)")
    print("실행 시각: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)
    test_apis()
    try:
        post = generate_post()
        if post is None:
            print("[종료] 중복 감지로 발행 건너뜀")
            exit(0)
        images = get_images("", count=3, title=post["title"], category=post["category"])
        post_to_blogger(post, images)
        print("\n모든 작업 완료!")
    except Exception as e:
        print("\n오류 발생: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
