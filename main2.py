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

TODAY = datetime.now().strftime("%Y\ub144 %m\uc6d4 %d\uc77c")
TODAY_EN = datetime.now().strftime("%Y-%m-%d")

CATEGORY_EMOJI = {
    "\uc2a4\ud3ec\uce20\uc774\uc288": "\u26bd",
    "\uacbd\uc81c\ub274\uc2a4": "\ud83d\udcb0",
    "\uc804\uad6d\uc774\uc288": "\ud83c\udf0d",
    "\uc5f0\uc608\uc774\uc288": "\ud83c\udfad"
}

CATEGORIES = ["\uc2a4\ud3ec\uce20\uc774\uc288", "\uacbd\uc81c\ub274\uc2a4", "\uc804\uad6d\uc774\uc288", "\uc5f0\uc608\uc774\uc288"]



YEAR = datetime.now().strftime("%Y")

# ── 생활정보 주제 풀 (95개) ──────────────────────────────
LIFE_TOPICS = [
    {"title": "주민등록등본 인터넷 발급방법 정부24 완벽 가이드", "category": "생활정보", "keyword": "주민등록등본 발급"},
    {"title": "주민등록초본 발급방법 및 등본과 차이점 정리", "category": "생활정보", "keyword": "주민등록초본 발급"},
    {"title": "주민등록증 분실 재발급 방법과 기간 총정리", "category": "생활정보", "keyword": "주민등록증 재발급"},
    {"title": "전입신고 방법 완벽 가이드 온라인 오프라인", "category": "생활정보", "keyword": "전입신고 방법"},
    {"title": "가족관계증명서 발급방법 종류별 완벽 정리", "category": "생활정보", "keyword": "가족관계증명서 발급"},
    {"title": "혼인신고 방법 완벽 가이드 온라인 오프라인 비교", "category": "생활정보", "keyword": "혼인신고 방법"},
    {"title": "출생신고 방법 및 기간 병원 동사무소 온라인", "category": "생활정보", "keyword": "출생신고 방법"},
    {"title": "전입신고 안 하면 생기는 일 전세사기 예방 필독", "category": "생활정보", "keyword": "전입신고 안하면"},
    {"title": "확정일자 받는 방법 완벽 가이드 온라인 오프라인", "category": "생활정보", "keyword": "확정일자 받기"},
    {"title": "부동산 등기부등본 보는 방법 완벽 가이드", "category": "생활정보", "keyword": "등기부등본 보기"},
    {"title": "전세사기 피하는 법 체크리스트 완벽 정리", "category": "생활정보", "keyword": "전세사기 예방"},
    {"title": "청년 전세자금대출 조건과 신청방법 " + YEAR, "category": "생활정보", "keyword": "청년 전세자금대출"},
    {"title": "버팀목 전세자금대출 " + YEAR + " 조건 정리", "category": "생활정보", "keyword": "버팀목 전세자금대출"},
    {"title": "LH 청년매입임대주택 신청방법 완벽 가이드", "category": "생활정보", "keyword": "LH 청년매입임대"},
    {"title": "연말정산 환급 최대로 받는 방법 " + YEAR, "category": "생활정보", "keyword": "연말정산 환급"},
    {"title": "종합소득세 신고방법 직장인 프리랜서 완벽 가이드", "category": "생활정보", "keyword": "종합소득세 신고"},
    {"title": "건강보험 피부양자 등록 방법과 조건 " + YEAR, "category": "생활정보", "keyword": "건강보험 피부양자"},
    {"title": "건강보험료 줄이는 합법적인 방법 총정리", "category": "생활정보", "keyword": "건강보험료 절감"},
    {"title": "국민연금 납부예외 신청방법과 조건", "category": "생활정보", "keyword": "국민연금 납부예외"},
    {"title": "자동차 이전등록 방법 중고차 구매 후 총정리", "category": "생활정보", "keyword": "자동차 이전등록"},
    {"title": "운전면허증 재발급 방법과 필요서류", "category": "생활정보", "keyword": "운전면허 재발급"},
    {"title": "자동차세 연납 신청방법 할인 받기 완벽 가이드", "category": "생활정보", "keyword": "자동차세 연납"},
    {"title": "부모급여 신청방법 및 " + YEAR + " 금액 정리", "category": "생활정보", "keyword": "부모급여 신청"},
    {"title": "아동수당 신청방법과 지급일 총정리 " + YEAR, "category": "생활정보", "keyword": "아동수당 신청"},
    {"title": "첫만남이용권 사용처와 신청방법 " + YEAR, "category": "생활정보", "keyword": "첫만남이용권"},
    {"title": "육아휴직 신청방법과 급여 계산법 총정리", "category": "생활정보", "keyword": "육아휴직 신청"},
    {"title": "출산급여 신청방법 직장인 자영업자 비교", "category": "생활정보", "keyword": "출산급여 신청"},
    {"title": "어린이집 입소 대기 빠르게 하는 법 실전 가이드", "category": "생활정보", "keyword": "어린이집 입소"},
    {"title": "다자녀 혜택 총정리 2명 3명 기준 " + YEAR, "category": "생활정보", "keyword": "다자녀 혜택"},
    {"title": "신혼부부 버팀목 대출 " + YEAR + " 조건 정리", "category": "생활정보", "keyword": "신혼부부 대출"},
    {"title": "신혼부부 청약 조건 및 가점 계산법 " + YEAR, "category": "생활정보", "keyword": "신혼부부 청약"},
    {"title": "신혼부부 정부지원금 총정리 " + YEAR, "category": "생활정보", "keyword": "신혼부부 지원금"},
    {"title": "결혼 준비 순서와 비용 현실 총정리", "category": "생활정보", "keyword": "결혼 준비 비용"},
    {"title": "청년도약계좌 " + YEAR + " 조건과 신청방법", "category": "생활정보", "keyword": "청년도약계좌"},
    {"title": "청년월세지원금 신청방법 지역별 정리 " + YEAR, "category": "생활정보", "keyword": "청년월세지원금"},
    {"title": "국민취업지원제도 신청방법 및 지원금액 " + YEAR, "category": "생활정보", "keyword": "국민취업지원제도"},
    {"title": "국민내일배움카드 신청방법 훈련비 지원 " + YEAR, "category": "생활정보", "keyword": "국민내일배움카드"},
    {"title": "실업급여 신청 조건과 방법 완벽 가이드 " + YEAR, "category": "생활정보", "keyword": "실업급여 신청"},
    {"title": "실업급여 얼마나 받나 계산법 총정리", "category": "생활정보", "keyword": "실업급여 계산"},
    {"title": "퇴직금 계산법 및 받는 방법 총정리", "category": "생활정보", "keyword": "퇴직금 계산"},
    {"title": "자격증 국비지원 받는 방법 총정리 " + YEAR, "category": "생활정보", "keyword": "자격증 국비지원"},
    {"title": "자취 처음 시작할 때 체크리스트 완벽 정리", "category": "생활정보", "keyword": "자취 체크리스트"},
    {"title": "원룸 계약 시 반드시 확인할 것 10가지", "category": "생활정보", "keyword": "원룸 계약 확인"},
    {"title": "1인가구 지원정책 총정리 " + YEAR, "category": "생활정보", "keyword": "1인가구 지원"},
    {"title": "혼자 사는 사람 건강보험료 줄이는 법", "category": "생활정보", "keyword": "1인가구 건강보험"},
    {"title": "이사 후 도시가스 신청방법 완벽 가이드", "category": "생활정보", "keyword": "도시가스 신청"},
    {"title": "기초생활수급자 신청방법과 조건 " + YEAR, "category": "생활정보", "keyword": "기초생활수급자 신청"},
    {"title": "차상위계층 신청방법과 혜택 총정리 " + YEAR, "category": "생활정보", "keyword": "차상위계층 신청"},
    {"title": "기초연금 신청방법 65세 이상 완벽 가이드", "category": "생활정보", "keyword": "기초연금 신청"},
    {"title": "긴급복지지원 신청방법과 대상 총정리", "category": "생활정보", "keyword": "긴급복지지원"},
    {"title": "복지로 원스톱 서비스 사용법 완벽 가이드", "category": "생활정보", "keyword": "복지로 사용법"},
    {"title": "정부24 회원가입 및 사용법 완벽 가이드", "category": "생활정보", "keyword": "정부24 사용법"},
    {"title": "사업자등록증 발급방법 개인 법인 완벽 가이드", "category": "생활정보", "keyword": "사업자등록 발급"},
    {"title": "프리랜서 세금 신고방법 완벽 가이드 " + YEAR, "category": "생활정보", "keyword": "프리랜서 세금"},
    {"title": "소상공인 지원금 신청방법 총정리 " + YEAR, "category": "생활정보", "keyword": "소상공인 지원금"},
    {"title": "여권 발급방법 신규 갱신 완벽 가이드 " + YEAR, "category": "생활정보", "keyword": "여권 발급방법"},
    {"title": "여권 분실 재발급 방법 해외에서도 가능할까", "category": "생활정보", "keyword": "여권 재발급"},
]

USED_LIFE_TITLES_FILE = "used_life_titles.json"


def load_used_life_titles():
    try:
        with open(USED_LIFE_TITLES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_used_life_title(title):
    used = load_used_life_titles()
    used.append(title)
    if len(used) > 50:
        used = used[-50:]
    try:
        with open(USED_LIFE_TITLES_FILE, "w") as f:
            json.dump(used, f, ensure_ascii=False)
    except Exception:
        pass

USED_TITLES_FILE = "used_titles2.json"


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
        print("[\uc911\ubcf5\ubc29\uc9c0] \uc800\uc7a5 \uc2e4\ud328: " + str(e))


def is_duplicate(title):
    used = load_used_titles()
    for t in used:
        if title[:10] in t or t[:10] in title:
            return True
    return False


CATEGORY_KEYWORDS = {
    "\uc2a4\ud3ec\uce20\uc774\uc288": {
        "naver": ["\uc2a4\ud3ec\uce20 \uc774\uc288 \uc624\ub298", "\ucd95\uad6c \ub274\uc2a4 \uc624\ub298", "\uc57c\uad6c \uc624\ub298", "\ub18d\uad6c \ub274\uc2a4", "\uc2a4\ud3ec\uce20 \uc120\uc218 \uc774\uc288"],
        "google": ["korea sports news today", "\ud55c\uad6d \uc2a4\ud3ec\uce20 \uc774\uc288"],
        "newsapi": ["korea sports international", "korean athlete world news"]
    },
    "\uacbd\uc81c\ub274\uc2a4": {
        "naver": ["\uacbd\uc81c \ub274\uc2a4 \uc624\ub298", "\ucf54\uc2a4\ud53c \uc624\ub298", "\ubd80\ub3d9\uc0b0 \ub274\uc2a4", "\ud658\uc728 \uc624\ub298", "\uc8fc\uc2dd \uc774\uc288"],
        "google": ["korea economy news today", "\ud55c\uad6d \uacbd\uc81c \uc774\uc288"],
        "newsapi": ["korea economy global", "korean market international"]
    },
    "\uc804\uad6d\uc774\uc288": {
        "naver": ["\uc624\ub298 \uc0ac\ud68c \uc774\uc288", "\uc815\uce58 \ub274\uc2a4 \uc624\ub298", "\uc0ac\uac74\uc0ac\uace0 \uc624\ub298", "\ud56b\uc774\uc288 \uc624\ub298", "\uc804\uad6d \ub274\uc2a4"],
        "google": ["korea news today", "\ud55c\uad6d \uc0ac\ud68c \uc774\uc288"],
        "newsapi": ["korea society global reaction", "south korea world news"]
    },
    "\uc5f0\uc608\uc774\uc288": {
        "naver": ["\uc5f0\uc608 \ub274\uc2a4 \uc624\ub298", "K\ud31d \uc774\uc288", "\ub4dc\ub77c\ub9c8 \ud654\uc81c", "\uc544\uc774\ub3cc \ub274\uc2a4", "\uc5f0\uc608\uc778 \uc774\uc288"],
        "google": ["kpop news today", "\ud55c\uad6d \uc5f0\uc608 \uc774\uc288"],
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
            print("[\ub124\uc774\ubc84] " + str(len(results)) + "\uac1c \uc218\uc9d1")
            return results
    except Exception as e:
        print("[\ub124\uc774\ubc84 \uc624\ub958] " + str(e))
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
            print("[\uad6c\uae00] " + str(len(results)) + "\uac1c \uc218\uc9d1")
            return results
    except Exception as e:
        print("[\uad6c\uae00 \uc624\ub958] " + str(e))
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
            print("[NewsAPI] " + str(len(results)) + "\uac1c \uc218\uc9d1")
            return results
    except Exception as e:
        print("[NewsAPI \uc624\ub958] " + str(e))
    return []


def collect_news(category):
    print("[\ub274\uc2a4 \uc218\uc9d1] \uce74\ud14c\uace0\ub9ac: " + category)
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
        print("[\uacbd\uace0] \ub274\uc2a4 \uc218\uc9d1 \uc2e4\ud328 - \uae30\ubcf8 \ub274\uc2a4 \ucee8\ud14d\uc2a4\ud2b8\ub85c \uc9c4\ud589")
        return "=== \uc624\ub298(" + TODAY + ") \ub274\uc2a4 \uc218\uc9d1 \uc2e4\ud328 - \ucd5c\uc2e0 \uc774\uc288\ub85c \uc791\uc131 \uc694\uccad ==="

    news_context = "=== \uc624\ub298(" + TODAY + ") \uc218\uc9d1\ub41c \ub274\uc2a4 ===\
"
    for i, news in enumerate(all_news[:5]):
        news_context += str(i + 1) + ". " + news + "\
"

    print("[\uc218\uc9d1 \uc644\ub8cc] \ucd1d " + str(len(all_news)) + "\uac1c")
    return news_context


def call_gemini(prompt, max_tokens=4000):
    """Gemini 2.0 Flash API \ud638\ucd9c"""
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY \uc5c6\uc74c")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash:generateContent?key=" + GEMINI_API_KEY
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.8,
            "topP": 0.95,
        }
    }

    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, timeout=120)
            print("[Gemini] \uc751\ub2f5 \uc0c1\ud0dc\ucf54\ub4dc: " + str(response.status_code))

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
                    raise Exception("Gemini \uc751\ub2f5\uc5d0 candidates \uc5c6\uc74c: " + str(data))

            elif response.status_code == 429:
                wait = 60 * (attempt + 1)
                print("[429] " + str(wait) + "\ucd08 \ub300\uae30 \ud6c4 \uc7ac\uc2dc\ub3c4...")
                time.sleep(wait)

            elif response.status_code == 503:
                wait = 30 * (attempt + 1)
                print("[503] " + str(wait) + "\ucd08 \ub300\uae30 \ud6c4 \uc7ac\uc2dc\ub3c4...")
                time.sleep(wait)

            else:
                raise Exception("Gemini \uc624\ub958: " + str(response.status_code) + " " + response.text[:200])

        except Exception as e:
            print("[Gemini \uc624\ub958] attempt " + str(attempt + 1) + ": " + str(e))
            if attempt < 2:
                time.sleep(20)
            else:
                raise

    raise Exception("Gemini \uc624\ub958: \ucd5c\ub300 \uc7ac\uc2dc\ub3c4 \ud69f\uc218 \ucd08\uacfc")


def test_apis():
    print("[API \ud655\uc778] GEMINI_API_KEY: " + ("\uc788\uc74c" if GEMINI_API_KEY else "\uc5c6\uc74c"))
    print("[API \ud655\uc778] NAVER_CLIENT_ID: " + ("\uc788\uc74c" if os.environ.get("NAVER_CLIENT_ID") else "\uc5c6\uc74c"))
    print("[API \ud655\uc778] GOOGLE_SEARCH_API_KEY: " + ("\uc788\uc74c" if os.environ.get("GOOGLE_SEARCH_API_KEY") else "\uc5c6\uc74c"))
    print("[API \ud655\uc778] NEWSAPI_KEY: " + ("\uc788\uc74c" if os.environ.get("NEWSAPI_KEY") else "\uc5c6\uc74c"))

    # Gemini \uc5f0\uacb0 \ud14c\uc2a4\ud2b8
    if GEMINI_API_KEY:
        try:
            result = call_gemini("\uc548\ub155\ud558\uc138\uc694. \ud14c\uc2a4\ud2b8\uc785\ub2c8\ub2e4. \ud55c \ubb38\uc7a5\uc73c\ub85c \uc751\ub2f5\ud574\uc8fc\uc138\uc694.", max_tokens=50)
            print("[Gemini \ud14c\uc2a4\ud2b8] \uc131\uacf5: " + result[:50])
        except Exception as e:
            print("[Gemini \ud14c\uc2a4\ud2b8 \uc624\ub958] " + str(e))


def generate_issue_post():
    category = random.choice(CATEGORIES)
    print("[\uce74\ud14c\uace0\ub9ac] " + category)

    news_context = collect_news(category)

    prompt = (
        "\ub2f9\uc2e0\uc740 20\ub144 \uacbd\ub825\uc758 \ubca0\ud14c\ub791 \uc2dc\ub2c8\uc5b4 \uae30\uc790\uc785\ub2c8\ub2e4.\
"
        "TV \ub274\uc2a4 \uc575\ucee4\ucc98\ub7fc \uba85\ud655\ud558\uace0 \uc2e0\ub8b0\uac10 \uc788\uc73c\uba70, \ub3c5\uc790\ub97c \ub04c\uc5b4\ub2f9\uae30\ub294 \ubb38\uc7a5\ub825\uc744 \uac16\uace0 \uc788\uc2b5\ub2c8\ub2e4.\
"
        "\ud55c\uad6d\uc5b4\ub9cc \uc0ac\uc6a9\ud558\uc138\uc694. \uc678\uad6d \ubb38\uc790 \uc808\ub300 \uae08\uc9c0.\
\
"
        "\uc544\ub798\ub294 \uc624\ub298(" + TODAY + ") \uc2e4\uc81c \uc218\uc9d1\ub41c \ub274\uc2a4\uc785\ub2c8\ub2e4:\
"
        + news_context + "\
\
"
        "\uc704 \ub274\uc2a4 \uc911 \uac00\uc7a5 \ud56b\ud558\uace0 \ub3c5\uc790 \uad00\uc2ec\uc774 \ub192\uc744 \uc774\uc288 \ud558\ub098\ub97c \uc120\ud0dd\ud574\uc11c \uae30\uc0ac\ub97c \uc791\uc131\ud558\uc138\uc694.\
"
        "\uad6d\ub0b4 \uc774\uc288\ub97c \uc911\uc2ec\uc73c\ub85c \uc791\uc131\ud558\ub418, \ud574\uc678 \ubc18\uc751\uc774\ub098 \uae00\ub85c\ubc8c \uad00\uc810\uc774 \uc788\ub2e4\uba74 \ube44\uad50 \ub0b4\uc6a9\uc744 \uc790\uc5f0\uc2a4\ub7fd\uac8c \ud55c \uc139\uc158 \ucd94\uac00\ud558\uc138\uc694.\
"
        "\ub2e8, \ud574\uc678 \ube44\uad50\ub294 \ubcf4\uc870\uc801\uc778 \ub0b4\uc6a9\uc774\uba70 \uad6d\ub0b4 \uc0c1\ud669\uc774 \ud56d\uc0c1 \uc911\uc2ec\uc774\uc5b4\uc57c \ud569\ub2c8\ub2e4.\
\
"
        "\uc808\ub300 \uc9c0\ucf1c\uc57c \ud560 \uc6d0\uce59:\
"
        "1. \uacf5\uc2dd \ud655\uc778\ub41c \ud329\ud2b8\ub9cc \uc791\uc131\ud558\uc138\uc694. \ub8e8\uba38, \ucd94\uce21 \uc808\ub300 \uae08\uc9c0.\
"
        "2. \uba85\uc608\ud6fc\uc190 \ub0b4\uc6a9 \uc808\ub300 \uae08\uc9c0.\
"
        "3. \ubc18\ub4dc\uc2dc \uc874\ub313\ub9d0\uc744 \uc0ac\uc6a9\ud558\uc138\uc694. '~\uc774\ub2e4', '~\ud55c\ub2e4' \ubc18\ub9d0 \uc885\uacb0 \uc808\ub300 \uae08\uc9c0.\
"
        "4. \uc911\ub9bd\uc801\uc774\uace0 \uac1d\uad00\uc801\uc778 \uc2dc\uac01\uc744 \uc720\uc9c0\ud558\uc138\uc694.\
"
        "5. \uc81c\ubaa9\uacfc \ub0b4\uc6a9\uc774 \uc77c\uce58\ud574\uc57c \ud569\ub2c8\ub2e4. \ub09a\uc2dc\uc131 \uc81c\ubaa9 \uae08\uc9c0.\
\
"
        "\uae00 \uad6c\uc870 (\ubc18\ub4dc\uc2dc \uc774 \uc21c\uc11c\ub85c):\
\
"
        "1. \ub9ac\ub4dc\ubb38 (2~3\uc904)\
"
        "\ud575\uc2ec \ud329\ud2b8\ub97c \uac15\ub82c\ud558\uac8c \uc804\ub2ec\ud558\uc138\uc694. \ub3c5\uc790\uac00 \uccab \ubb38\uc7a5\uc5d0 \uba48\ucd94\uac8c \ub9cc\ub4dc\uc138\uc694.\
\
"
        "2. ##\ud575\uc2ec\ud0a4\uc6cc\ub4dc##\
"
        "\uc774 \uc774\uc288\uc758 \ud575\uc2ec\uc744 \ud55c \ub2e8\uc5b4\ub098 \uc9e7\uc740 \uad6c\ub85c \ud06c\uac8c \ub358\uc9c0\uc138\uc694.\
"
        "\uadf8 \uc544\ub798 2~3\ubb38\uc7a5\uc73c\ub85c \uc27d\uac8c \ud480\uc5b4\uc4f0\uc138\uc694.\
\
"
        "3. \uc18c\uc81c\ubaa9 \uad6c\uc870 (3~4\uac1c)\
"
        "\uc18c\uc81c\ubaa9: [\uc774\ubaa8\uc9c0 \uc18c\uc81c\ubaa9\ub0b4\uc6a9 \uc774\ubaa8\uc9c0] \ud615\uc2dd. \uc55e\ub4a4 \uc774\ubaa8\uc9c0 \ud544\uc218.\
"
        "\uc608: [\ud83d\udccc \uc0ac\uac74\uc758 \uc804\ub9d0 \ud83d\udccc], [\ud83d\udcac \uac01\uacc4 \ubc18\uc751 \ud83d\udcac], [\ud83c\udf0d \ud574\uc678 \ubc18\uc751\uacfc \ube44\uad50 \ud83c\udf0d]\
"
        "\uac01 \uc18c\uc81c\ubaa9 \uc544\ub798: \ubc30\uacbd \u2192 \ud329\ud2b8 \u2192 \ubc18\uc751 \uc21c\uc73c\ub85c \uae4a\uc5b4\uc9c0\uac8c\
"
        "\ub2e8\ub77d 3~4\uc904 \uc774\ub0b4. \ube48 \uc904 \ud544\uc218.\
"
        "\uc218\uce58, \ub0a0\uc9dc, \ucd9c\ucc98 \uba85\ud655\ud788 \ud45c\uae30.\
\
"
        "4. \uc804\ub9dd + \ub3c5\uc790 \uad00\uc810\
"
        "\uc55e\uc73c\ub85c \uc5b4\ub5bb\uac8c \ub420\uc9c0 + \ub3c5\uc790\uc5d0\uac8c \uc758\ubbf8\ud558\ub294 \uac83\
"
        "\ubc18\ub4dc\uc2dc \uc874\ub313\ub9d0\ub85c \ub05d\ub0b4\uc138\uc694. \uaca9\uc5b8 \uae08\uc9c0.\
\
"
        "5. \ud575\uc2ec \uc694\uc57d\
"
        "[SUMMARY_START]\
"
        "\ud575\uc2ec1\
"
        "\ud575\uc2ec2\
"
        "\ud575\uc2ec3\
"
        "[SUMMARY_END]\
\
"
        "\uae00\uc4f0\uae30 \uc6d0\uce59:\
"
        "\ubc18\ub4dc\uc2dc \uc874\ub313\ub9d0. '~\uc774\ub2e4', '~\ud55c\ub2e4' \ubc18\ub9d0 \uc885\uacb0 \uc808\ub300 \uae08\uc9c0.\
"
        "AI \ud2f0 \ub098\ub294 \ub098\uc5f4\uc2dd \ud45c\ud604 \uae08\uc9c0.\
"
        "2500\uc790\uc5d0\uc11c 3500\uc790.\
\
"
        "\uce74\ud14c\uace0\ub9ac: " + category + "\
\
"
        "\ucd9c\ub825 \ud615\uc2dd:\
"
        "\uc81c\ubaa9: (\ud329\ud2b8 \uae30\ubc18 \uac15\ub82c\ud55c \uc81c\ubaa9)\
"
        "---\
"
        "(\ubcf8\ubb38)"
    )

    print("[AI] Gemini 2.0 Flash \uae30\uc0ac \uc791\uc131 \uc911...")
    full_text = call_gemini(prompt, max_tokens=4000)

    lines = full_text.strip().split("\
")
    title = ""
    body_lines = []
    separator_found = False

    for line in lines:
        if line.startswith("\uc81c\ubaa9:"):
            title = line.replace("\uc81c\ubaa9:", "").strip()
        elif line.strip() == "---":
            separator_found = True
        elif separator_found:
            body_lines.append(line)

    body = "\
".join(body_lines).strip()
    if not title:
        title = TODAY + " " + category + " \ud56b\uc774\uc288"
    if not body:
        body = full_text

    # \uc911\ubcf5 \uac10\uc9c0
    if is_duplicate(title):
        print("[\uc911\ubcf5 \uac10\uc9c0] \uc81c\ubaa9 \uc911\ubcf5 \u2014 \ubc1c\ud589 \uac74\ub108\ub700: " + title)
        return None

    save_used_title(title)
    print("[\uc644\ub8cc] \uc81c\ubaa9: " + title)
    print("[\uc644\ub8cc] \uae00\uc790\uc218: " + str(len(body)) + "\uc790")
    return {"title": title, "body": body, "category": category}




def generate_life_post():
    """생활정보 가이드 글 생성"""
    used = load_used_life_titles()
    available = [t for t in LIFE_TOPICS if not any(t["title"][:10] in u or u[:10] in t["title"] for u in used)]
    if not available:
        available = LIFE_TOPICS
        try:
            with open(USED_LIFE_TITLES_FILE, "w") as f:
                json.dump([], f)
        except Exception:
            pass

    topic = random.choice(available)
    keyword = topic["keyword"]
    title_base = topic["title"]
    print("[생활정보 모드] 주제: " + title_base)

    # 네이버 검색으로 관련 정보 수집
    related = []
    if NAVER_CLIENT_ID and NAVER_CLIENT_SECRET:
        try:
            response = requests.get(
                "https://openapi.naver.com/v1/search/news.json",
                headers={"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET},
                params={"query": keyword, "display": 5, "sort": "date"},
                timeout=10
            )
            if response.status_code == 200:
                items = response.json().get("items", [])
                for item in items:
                    title = item.get("title", "").replace("<b>", "").replace("</b>", "").replace("&amp;", "&")
                    desc = item.get("description", "").replace("<b>", "").replace("</b>", "").replace("&amp;", "&")
                    related.append(title + ": " + desc)
                print("[생활정보] 관련 정보 " + str(len(related)) + "개 수집")
        except Exception as e:
            print("[생활정보 검색 오류] " + str(e))

    ctx = "=== 작성 주제 ===\n" + title_base + "\n검색 키워드: " + keyword + "\n\n"
    if related:
        ctx += "=== 관련 최신 정보 ===\n" + "\n".join(str(i+1)+". "+r for i,r in enumerate(related[:5]))

    prompt = (
        "당신은 대한민국 행정/생활정보 전문 블로거입니다.\n"
        "독자가 이 글만 읽으면 실제로 업무를 처리할 수 있게 써야 합니다.\n"
        "한국어만 사용하세요.\n\n"
        "주제: " + title_base + "\n"
        "참고 정보:\n" + ctx + "\n\n"
        "✅ 작성 원칙:\n"
        "1. '나도 처음엔 몰랐는데...' 같은 공감 문장으로 시작\n"
        "2. 핵심 정보를 단계별(1단계→2단계→3단계)로 명확하게\n"
        "3. 준비물/필요서류 목록 반드시 포함\n"
        "4. 처리 시간/비용/유의사항 포함\n"
        "5. 온라인(정부24 등) + 오프라인 방법 모두 안내\n"
        "6. 마지막에 자주 묻는 질문 2~3개\n"
        "7. 친근하고 실용적인 문체. 딱딱한 공문서체 금지\n"
        "8. 반드시 존댓말\n\n"
        "글 구조:\n"
        "1. 공감 도입 (2~3줄)\n"
        "2. ##핵심요약##\n"
        "3. [📋 준비물과 필요서류]\n"
        "   [💻 온라인 신청방법 단계별]\n"
        "   [🏛️ 오프라인 방문 방법]\n"
        "   [⚠️ 주의사항과 유의점]\n"
        "   [❓ 자주 묻는 질문]\n"
        "4. 마무리 한 줄 팁\n"
        "5. [SUMMARY_START]\n핵심1\n핵심2\n핵심3\n[SUMMARY_END]\n\n"
        "분량: 2500자 이상. 반드시 완성된 글.\n\n"
        "출력:\n제목: (검색에 유리한 제목)\n---\n(본문)"
    )

    print("[AI] Gemini 생활정보 가이드 작성 중...")
    full_text = call_gemini(prompt, max_tokens=6000)

    lines = full_text.strip().split("\n")
    title = ""
    body_lines = []
    sep = False
    for line in lines:
        if line.startswith("제목:"):
            title = line.replace("제목:", "").strip()
        elif line.strip() == "---":
            sep = True
        elif sep:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    if not title:
        title = title_base
    if not body:
        body = full_text

    if is_duplicate(title):
        print("[중복] 건너뜀: " + title)
        return None

    save_used_life_title(title)
    save_used_title(title)
    print("[완료] " + title)
    return {"title": title, "body": body, "category": "생활정보"}


def generate_post():
    """이슈 칼럼(67%) 또는 생활정보(33%) 랜덤 선택"""
    mode = random.choice(["issue", "issue", "life"])
    print("[모드] " + ("이슈 칼럼" if mode == "issue" else "생활정보 가이드"))

    if mode == "issue":
        post = generate_issue_post()
        if post is None:
            print("[이슈 실패] 생활정보로 전환")
            post = generate_life_post()
    else:
        post = generate_life_post()
        if post is None:
            print("[생활정보 실패] 이슈로 전환")
            post = generate_issue_post()
    return post

def get_image_keyword_from_title(title, category):
    keyword_map = {
        "\ucd95\uad6c": "soccer football player",
        "\uc57c\uad6c": "baseball player",
        "\ub18d\uad6c": "basketball player",
        "\uc190\ud765\ubbfc": "soccer player football",
        "\ub958\ud604\uc9c4": "baseball pitcher",
        "\ucf54\uc2a4\ud53c": "stock market chart",
        "\ubd80\ub3d9\uc0b0": "real estate building",
        "\uae08\ub9ac": "finance money banking",
        "\ud658\uc728": "currency exchange money",
        "\ub4dc\ub77c\ub9c8": "korean drama tv",
        "\uc544\uc774\ub3cc": "kpop concert music",
        "\uc5f0\uc608": "entertainment stage performance",
        "\uc0ac\uac74": "police investigation",
        "\uc815\uce58": "government politics",
        "\uacbd\uc81c": "business finance economy",
    }
    for kor, eng in keyword_map.items():
        if kor in title:
            return eng
    category_defaults = {
        "\uc2a4\ud3ec\uce20\uc774\uc288": "sports athlete action",
        "\uacbd\uc81c\ub274\uc2a4": "business finance economy",
        "\uc804\uad6d\uc774\uc288": "city korea urban street",
        "\uc5f0\uc608\uc774\uc288": "stage performance music concert",
    }
    return category_defaults.get(category, "news media")


def get_images_unsplash(keyword, count=3):
    if not UNSPLASH_ACCESS_KEY:
        return []
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={"query": keyword, "per_page": count, "orientation": "landscape", "client_id": UNSPLASH_ACCESS_KEY},
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
            return images
    except Exception as e:
        print("[Unsplash \uc624\ub958] " + str(e))
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
        print("[Pexels \uc624\ub958] " + str(e))
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
        print("[Pixabay \uc624\ub958] " + str(e))
    return []


def get_images(keyword, count=3, title="", category=""):
    if title or category:
        keyword = get_image_keyword_from_title(title, category)
    print("[\uc774\ubbf8\uc9c0 \uac80\uc0c9] \ud0a4\uc6cc\ub4dc: " + keyword)

    images = get_images_unsplash(keyword, count)
    if images:
        print("[\uc774\ubbf8\uc9c0] Unsplash " + str(len(images)) + "\uc7a5")
        return images

    images = get_images_pexels(keyword, count)
    if images:
        print("[\uc774\ubbf8\uc9c0] Pexels " + str(len(images)) + "\uc7a5")
        return images

    images = get_images_pixabay(keyword, count)
    if images:
        print("[\uc774\ubbf8\uc9c0] Pixabay " + str(len(images)) + "\uc7a5")
        return images

    print("[\uc774\ubbf8\uc9c0] \ubaa8\ub4e0 \uc18c\uc2a4 \uc2e4\ud328")
    return []


def make_summary_html(summary_text):
    lines = [l.strip() for l in summary_text.strip().split("\
") if l.strip()]
    html = '<div style="background:#fff8e1;border-left:5px solid #f57f17;border-radius:8px;padding:20px 24px;margin:28px 0;">'
    html += '<p style="font-weight:700;font-size:17px;color:#f57f17;margin-bottom:12px;">\ud83d\udccc \ud575\uc2ec \uc694\uc57d</p>'
    for line in lines:
        html += '<p style="margin:6px 0;font-size:15px;color:#333;">\u2705 ' + line + "</p>"
    html += "</div>\
"
    return html


def make_image_html(img, margin_top="0"):
    source = img.get("source", "Unsplash")
    html = '<div style="text-align:center;margin:30px 0;margin-top:' + margin_top + ';">'
    html += '<img src="' + img["url"] + '" alt="' + img["alt"] + '" style="max-width:100%;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.12);"/>'
    html += '<p style="font-size:12px;color:#999;margin-top:8px;">Photo by <a href="' + img["author_url"] + '" style="color:#999;">' + img["author"] + '</a> on ' + source + '</p>'
    html += "</div>\
"
    return html


def body_to_html(body, images, category):
    import re

    emoji = CATEGORY_EMOJI.get(category, "\ud83d\udcf0")

    html = (
        '<div style="display:inline-block;background:#e65100;color:#fff;'
        'font-size:13px;padding:5px 14px;border-radius:20px;margin-bottom:8px;font-weight:600;">'
        + emoji + " " + category + "</div>\
"
        '<div style="font-size:13px;color:#888;margin-bottom:20px;">\ud83d\udcc5 ' + TODAY + "</div>\
"
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
        toc += '<p style="font-weight:700;font-size:15px;color:#e65100;margin-bottom:12px;">\ud83d\udccb \ubaa9\ucc28</p>'
        toc += '<ol style="margin:0;padding-left:20px;">'
        for h in headings:
            clean_h = re.sub(r'^[^\w\uac00-\ud7a3]+', '', h).strip()
            clean_h = re.sub(r'[^\w\uac00-\ud7a3\s]+$', '', clean_h).strip()
            if clean_h:
                toc += '<li style="margin:6px 0;font-size:15px;color:#444;line-height:1.6;">' + clean_h + '</li>'
        toc += '</ol></div>\
'
        html += toc

    def replace_keyword(m):
        return (
            '<div style="margin:28px 0 12px 0;">'
            '<span style="display:inline-block;font-size:30px;font-weight:900;'
            'color:#e65100;letter-spacing:-0.5px;'
            'border-bottom:3px solid #e65100;padding-bottom:4px;">'
            + m.group(1) + '</span></div>\
'
        )

    paragraphs = clean_body.split("\
")
    mid = len(paragraphs) // 2
    image2_inserted = False
    para_count = 0

    for i, para in enumerate(paragraphs):
        if not para.strip():
            html += '<div style="margin:10px 0;"></div>\
'
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
                + heading + "</h2>\
"
            )
            continue

        if len(para.strip()) > 1 and para.strip()[0].isdigit() and para.strip()[1] in [".", ")"]:
            html += (
                '<div style="display:flex;align-items:flex-start;margin:10px 0;padding:12px 16px;'
                'background:#fff3e0;border-radius:8px;">'
                '<span style="color:#e65100;font-weight:700;margin-right:12px;font-size:16px;">'
                + para.strip()[0] + '.</span>'
                '<span style="color:#333;font-size:16px;line-height:1.8;">'
                + para.strip()[2:].strip() + '</span></div>\
'
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
                + para.strip() + '</p></div>\
'
            )
        else:
            html += (
                '<p style="margin:14px 0;line-height:1.9;font-size:16px;color:#333;">'
                + para.strip() + '</p>\
'
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
        raise Exception("\ud1a0\ud070 \ubc1c\uae09 \uc2e4\ud328: " + response.text)
    return response.json()["access_token"]


def send_telegram(title, post_url, category):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    emoji = CATEGORY_EMOJI.get(category, "\ud83d\udcf0")
    message = emoji + " \uc0c8 \ud3ec\uc2a4\ud305\
\
\ud83d\udccc " + title + "\
\
\ud83d\udd17 " + post_url
    try:
        requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
            timeout=10
        )
        print("[\ud154\ub808\uadf8\ub7a8] \uacf5\uc720 \uc131\uacf5!")
    except Exception as e:
        print("[\ud154\ub808\uadf8\ub7a8 \uc624\ub958] " + str(e))


def send_facebook(title, post_url, category):
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        return
    emoji = CATEGORY_EMOJI.get(category, "\ud83d\udcf0")
    message = emoji + " \uc0c8 \ud3ec\uc2a4\ud305\
\
" + title + "\
\
\uc790\uc138\ud788 \uc77d\uae30 \ud83d\udc49 " + post_url
    try:
        requests.post(
            "https://graph.facebook.com/v19.0/" + FACEBOOK_PAGE_ID + "/feed",
            data={"message": message, "link": post_url, "access_token": FACEBOOK_ACCESS_TOKEN},
            timeout=10
        )
        print("[\ud398\uc774\uc2a4\ubd81] \uacf5\uc720 \uc131\uacf5!")
    except Exception as e:
        print("[\ud398\uc774\uc2a4\ubd81 \uc624\ub958] " + str(e))


def post_to_blogger(post_data, images, retry=2):
    print("\
[Blogger] insaplayer \ud3ec\uc2a4\ud305 \uc2dc\uc791...")
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
            print("[\uc2dc\ub3c4 " + str(attempt) + "] " + post_data["title"])
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                post_url = response.json().get("url", "")
                print("\ubc1c\ud589 \uc644\ub8cc! " + post_url)
                send_telegram(post_data["title"], post_url, category)
                send_facebook(post_data["title"], post_url, category)
                return True
            else:
                print("\uc2e4\ud328: " + response.text[:200])
                if attempt <= retry:
                    time.sleep(10)
        except Exception as e:
            print("[\uc624\ub958] " + str(e))
            if attempt <= retry:
                time.sleep(10)
    return False


if __name__ == "__main__":
    print("=" * 50)
    print("insaplayer - \uc2e4\uc2dc\uac04 \ub274\uc2a4 \ube14\ub85c\uadf8 v12 (Gemini 2.5 Flash + 이슈칼럼 + 생활정보)")
    print("\uc2e4\ud589 \uc2dc\uac01: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)
    test_apis()
    try:
        post = generate_post()
        if post is None:
            print("[\uc885\ub8cc] \uc911\ubcf5 \uac10\uc9c0\ub85c \ubc1c\ud589 \uac74\ub108\ub700")
            exit(0)
        images = get_images("", count=3, title=post["title"], category=post["category"])
        post_to_blogger(post, images)
        print("\
\ubaa8\ub4e0 \uc791\uc5c5 \uc644\ub8cc!")
    except Exception as e:
        print("\
\uc624\ub958 \ubc1c\uc0dd: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
