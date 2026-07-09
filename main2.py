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
GOOGLE_SEARCH_API_KEY = os.environ.get("GOOGLE_SEARCH_API_KEY", "")
GOOGLE_SEARCH_ENGINE_ID = os.environ.get("GOOGLE_SEARCH_ENGINE_ID", "")
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "")
BLOG_ID = "8468892944117983817"

TODAY = datetime.now().strftime("%Y년 %m월 %d일")
TODAY_EN = datetime.now().strftime("%Y-%m-%d")
YEAR = datetime.now().strftime("%Y")

CATEGORY_EMOJI = {
    "스포츠이슈": "⚽",
    "경제뉴스": "💰",
    "전국이슈": "🌍",
    "연예이슈": "🎭",
    "생활정보": "📋",
}

CATEGORIES = ["스포츠이슈", "경제뉴스", "전국이슈", "연예이슈"]

USED_TITLES_FILE = "used_titles2.json"
USED_LIFE_FILE = "used_life.json"

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

LIFE_TOPICS = [
    {"title": "주민등록등본 인터넷 발급방법 정부24 완벽 가이드", "keyword": "주민등록등본 발급"},
    {"title": "주민등록초본 발급방법 및 등본과 차이점 정리", "keyword": "주민등록초본 발급"},
    {"title": "주민등록증 분실 재발급 방법과 기간 총정리", "keyword": "주민등록증 재발급"},
    {"title": "전입신고 방법 완벽 가이드 온라인 오프라인", "keyword": "전입신고 방법"},
    {"title": "가족관계증명서 발급방법 종류별 완벽 정리", "keyword": "가족관계증명서 발급"},
    {"title": "혼인신고 방법 완벽 가이드 온라인 오프라인 비교", "keyword": "혼인신고 방법"},
    {"title": "출생신고 방법 및 기간 병원 동사무소 온라인", "keyword": "출생신고 방법"},
    {"title": "확정일자 받는 방법 완벽 가이드 온라인 오프라인", "keyword": "확정일자 받기"},
    {"title": "전세사기 피하는 법 체크리스트 완벽 정리", "keyword": "전세사기 예방"},
    {"title": "부동산 등기부등본 보는 방법 완벽 가이드", "keyword": "등기부등본 보기"},
    {"title": "연말정산 환급 최대로 받는 방법 " + YEAR, "keyword": "연말정산 환급"},
    {"title": "종합소득세 신고방법 직장인 프리랜서 완벽 가이드", "keyword": "종합소득세 신고"},
    {"title": "건강보험 피부양자 등록 방법과 조건 " + YEAR, "keyword": "건강보험 피부양자"},
    {"title": "건강보험료 줄이는 합법적인 방법 총정리", "keyword": "건강보험료 절감"},
    {"title": "국민연금 납부예외 신청방법과 조건", "keyword": "국민연금 납부예외"},
    {"title": "자동차 이전등록 방법 중고차 구매 후 총정리", "keyword": "자동차 이전등록"},
    {"title": "운전면허증 재발급 방법과 필요서류", "keyword": "운전면허 재발급"},
    {"title": "자동차세 연납 신청방법 할인 받기 완벽 가이드", "keyword": "자동차세 연납"},
    {"title": "부모급여 신청방법 및 " + YEAR + " 금액 정리", "keyword": "부모급여 신청"},
    {"title": "아동수당 신청방법과 지급일 총정리 " + YEAR, "keyword": "아동수당 신청"},
    {"title": "첫만남이용권 사용처와 신청방법 " + YEAR, "keyword": "첫만남이용권"},
    {"title": "육아휴직 신청방법과 급여 계산법 총정리", "keyword": "육아휴직 신청"},
    {"title": "출산급여 신청방법 직장인 자영업자 비교", "keyword": "출산급여 신청"},
    {"title": "어린이집 입소 대기 빠르게 하는 법 실전 가이드", "keyword": "어린이집 입소"},
    {"title": "다자녀 혜택 총정리 2명 3명 기준 " + YEAR, "keyword": "다자녀 혜택"},
    {"title": "신혼부부 버팀목 대출 " + YEAR + " 조건 정리", "keyword": "신혼부부 대출"},
    {"title": "신혼부부 청약 조건 및 가점 계산법 " + YEAR, "keyword": "신혼부부 청약"},
    {"title": "신혼부부 정부지원금 총정리 " + YEAR, "keyword": "신혼부부 지원금"},
    {"title": "결혼 준비 순서와 비용 현실 총정리", "keyword": "결혼 준비 비용"},
    {"title": "청년도약계좌 " + YEAR + " 조건과 신청방법", "keyword": "청년도약계좌"},
    {"title": "청년월세지원금 신청방법 지역별 정리 " + YEAR, "keyword": "청년월세지원금"},
    {"title": "국민취업지원제도 신청방법 및 지원금액 " + YEAR, "keyword": "국민취업지원제도"},
    {"title": "국민내일배움카드 신청방법 훈련비 지원 " + YEAR, "keyword": "국민내일배움카드"},
    {"title": "실업급여 신청 조건과 방법 완벽 가이드 " + YEAR, "keyword": "실업급여 신청"},
    {"title": "실업급여 얼마나 받나 계산법 총정리", "keyword": "실업급여 계산"},
    {"title": "퇴직금 계산법 및 받는 방법 총정리", "keyword": "퇴직금 계산"},
    {"title": "자격증 국비지원 받는 방법 총정리 " + YEAR, "keyword": "자격증 국비지원"},
    {"title": "자취 처음 시작할 때 체크리스트 완벽 정리", "keyword": "자취 체크리스트"},
    {"title": "원룸 계약 시 반드시 확인할 것 10가지", "keyword": "원룸 계약 확인"},
    {"title": "1인가구 지원정책 총정리 " + YEAR, "keyword": "1인가구 지원"},
    {"title": "혼자 사는 사람 건강보험료 줄이는 법", "keyword": "1인가구 건강보험"},
    {"title": "이사 후 도시가스 신청방법 완벽 가이드", "keyword": "도시가스 신청"},
    {"title": "기초생활수급자 신청방법과 조건 " + YEAR, "keyword": "기초생활수급자 신청"},
    {"title": "차상위계층 신청방법과 혜택 총정리 " + YEAR, "keyword": "차상위계층 신청"},
    {"title": "기초연금 신청방법 65세 이상 완벽 가이드", "keyword": "기초연금 신청"},
    {"title": "긴급복지지원 신청방법과 대상 총정리", "keyword": "긴급복지지원"},
    {"title": "복지로 원스톱 서비스 사용법 완벽 가이드", "keyword": "복지로 사용법"},
    {"title": "정부24 회원가입 및 사용법 완벽 가이드", "keyword": "정부24 사용법"},
    {"title": "사업자등록증 발급방법 개인 법인 완벽 가이드", "keyword": "사업자등록 발급"},
    {"title": "프리랜서 세금 신고방법 완벽 가이드 " + YEAR, "keyword": "프리랜서 세금"},
    {"title": "소상공인 지원금 신청방법 총정리 " + YEAR, "keyword": "소상공인 지원금"},
    {"title": "여권 발급방법 신규 갱신 완벽 가이드 " + YEAR, "keyword": "여권 발급방법"},
    {"title": "여권 분실 재발급 방법 해외에서도 가능할까", "keyword": "여권 재발급"},
    {"title": "버팀목 전세자금대출 " + YEAR + " 조건 정리", "keyword": "버팀목 전세자금대출"},
    {"title": "청년 전세자금대출 조건과 신청방법 " + YEAR, "keyword": "청년 전세자금대출"},
    {"title": "LH 청년매입임대주택 신청방법 완벽 가이드", "keyword": "LH 청년매입임대"},
]


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


def load_used_life():
    try:
        with open(USED_LIFE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_used_life(title):
    used = load_used_life()
    used.append(title)
    if len(used) > 50:
        used = used[-50:]
    try:
        with open(USED_LIFE_FILE, "w") as f:
            json.dump(used, f, ensure_ascii=False)
    except Exception:
        pass


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
                t = article.get("title", "") or ""
                d = article.get("description", "") or ""
                results.append(t + ": " + d)
            print("[NewsAPI] " + str(len(results)) + "개 수집")
            return results
    except Exception as e:
        print("[NewsAPI 오류] " + str(e))
    return []


def collect_news(category):
    print("[뉴스 수집] 카테고리: " + category)
    keywords = CATEGORY_KEYWORDS[category]

    naver_q1 = random.choice(keywords["naver"])
    remaining = [k for k in keywords["naver"] if k != naver_q1]
    naver_q2 = random.choice(remaining) if remaining else naver_q1
    google_q = random.choice(keywords["google"])
    newsapi_q = random.choice(keywords["newsapi"])

    r1 = search_naver_news(naver_q1, display=5)
    r2 = search_naver_news(naver_q2, display=3)
    r3 = search_google_news(google_q, num=3)
    r4 = search_newsapi(newsapi_q, page_size=3)

    all_news = r1 + r2 + r3 + r4

    if not all_news:
        return "=== 오늘(" + TODAY + ") 뉴스 수집 실패 - 최신 이슈로 작성 요청 ==="

    ctx = "=== 오늘(" + TODAY + ") 수집된 뉴스 ===\n"
    for i, news in enumerate(all_news[:5]):
        ctx += str(i + 1) + ". " + news + "\n"
    print("[수집 완료] 총 " + str(len(all_news)) + "개")
    return ctx


def call_gemini(prompt, max_tokens=4000):
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


def test_apis():
    print("[API 확인] GEMINI_API_KEY: " + ("있음" if GEMINI_API_KEY else "없음"))
    print("[API 확인] NAVER_CLIENT_ID: " + ("있음" if os.environ.get("NAVER_CLIENT_ID") else "없음"))
    print("[API 확인] GOOGLE_SEARCH_API_KEY: " + ("있음" if os.environ.get("GOOGLE_SEARCH_API_KEY") else "없음"))
    print("[API 확인] NEWSAPI_KEY: " + ("있음" if os.environ.get("NEWSAPI_KEY") else "없음"))

    if GEMINI_API_KEY:
        try:
            result = call_gemini("테스트입니다. 한 문장으로 응답해주세요.", max_tokens=50)
            print("[Gemini 테스트] 성공: " + result[:50])
        except Exception as e:
            print("[Gemini 테스트 오류] " + str(e))


def parse_gemini_output(full_text, fallback_title):
    """Gemini 출력에서 제목과 본문 파싱"""
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
        title = fallback_title
    if not body:
        body = full_text
    return title, body


def generate_issue_post():
    """이슈 칼럼 생성 (네이버/구글/NewsAPI 3중 수집)"""
    category = random.choice(CATEGORIES)
    print("[이슈 모드] 카테고리: " + category)

    news_context = collect_news(category)

    prompt = (
        "당신은 20년 경력의 베테랑 시니어 기자입니다.\n"
        "TV 뉴스 앵커처럼 명확하고 신뢰감 있으며, 독자를 끌어당기는 문장력을 갖고 있습니다.\n"
        "한국어만 사용하세요. 외국 문자 절대 금지.\n\n"
        "아래는 오늘(" + TODAY + ") 실제 수집된 뉴스입니다:\n"
        + news_context + "\n\n"
        "위 뉴스 중 가장 핫하고 독자 관심이 높을 이슈 하나를 선택해서 기사를 작성하세요.\n"
        "절대 지켜야 할 원칙:\n"
        "1. 공식 확인된 팩트만 작성. 루머, 추측 절대 금지.\n"
        "2. 명예훼손 내용 절대 금지.\n"
        "3. 반드시 존댓말. '~이다', '~한다' 반말 종결 절대 금지.\n"
        "4. 제목과 내용 일치. 낚시성 제목 금지.\n\n"
        "글 구조 (반드시 이 순서로):\n\n"
        "1. 리드문 (2~3줄)\n"
        "핵심 팩트를 강렬하게 전달. 독자가 첫 문장에 멈추게 만드세요.\n\n"
        "2. ##핵심키워드##\n"
        "이 이슈의 핵심을 한 단어나 짧은 구로 크게 던지세요.\n"
        "그 아래 2~3문장으로 쉽게 풀어쓰세요.\n\n"
        "3. 소제목 구조 (3~4개)\n"
        "소제목 형식: [이모지 소제목내용 이모지]\n"
        "각 소제목 아래: 배경 → 팩트 → 반응 순으로 깊어지게\n"
        "단락 3~4줄 이내. 빈 줄 필수.\n"
        "수치, 날짜, 출처 명확히 표기.\n\n"
        "4. 전망 + 독자 관점\n"
        "앞으로 어떻게 될지 + 독자에게 의미하는 것\n"
        "반드시 존댓말로 끝내세요. 격언 금지.\n\n"
        "5. 핵심 요약\n"
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

    print("[AI] Gemini 이슈 칼럼 작성 중...")
    full_text = call_gemini(prompt, max_tokens=4000)
    title, body = parse_gemini_output(full_text, TODAY + " " + category + " 핫이슈")

    if is_duplicate(title):
        print("[중복 감지] 발행 건너뜀: " + title)
        return None

    save_used_title(title)
    print("[완료] 제목: " + title)
    print("[완료] 글자수: " + str(len(body)) + "자")
    return {"title": title, "body": body, "category": category}


def generate_life_post():
    """생활정보 가이드 생성"""
    used = load_used_life()
    available = [t for t in LIFE_TOPICS if not any(t["title"][:10] in u or u[:10] in t["title"] for u in used)]
    if not available:
        available = LIFE_TOPICS
        try:
            with open(USED_LIFE_FILE, "w") as f:
                json.dump([], f)
        except Exception:
            pass

    topic = random.choice(available)
    keyword = topic["keyword"]
    title_base = topic["title"]
    print("[생활정보 모드] 주제: " + title_base)

    # 네이버에서 관련 정보 수집
    related = search_naver_news(keyword, display=5)

    ctx = "주제: " + title_base + "\n키워드: " + keyword
    if related:
        ctx += "\n\n관련 정보:\n" + "\n".join(str(i+1) + ". " + r for i, r in enumerate(related[:5]))

    prompt = (
        "당신은 대한민국 행정/생활정보 전문 블로거입니다.\n"
        "독자가 이 글만 읽으면 실제로 업무를 처리할 수 있게 써야 합니다.\n"
        "한국어만 사용하세요.\n\n"
        "주제: " + title_base + "\n"
        "참고:\n" + ctx + "\n\n"
        "작성 원칙:\n"
        "1. '나도 처음엔 몰랐는데...' 같은 공감 문장으로 시작\n"
        "2. 단계별 명확한 안내 (1단계 2단계 3단계)\n"
        "3. 준비물과 필요서류 목록 포함\n"
        "4. 온라인 + 오프라인 방법 모두 안내\n"
        "5. 자주 묻는 질문 2~3개 포함\n"
        "6. 친근한 존댓말. 공문서체 금지\n\n"
        "글 구조:\n"
        "1. 공감 도입 2~3줄\n"
        "2. ##핵심요약##\n"
        "3. [📋 준비물과 필요서류]\n"
        "   [💻 온라인 신청방법]\n"
        "   [🏛️ 오프라인 방법]\n"
        "   [⚠️ 주의사항]\n"
        "   [❓ 자주 묻는 질문]\n"
        "4. 마무리 팁\n"
        "5. [SUMMARY_START]\n핵심1\n핵심2\n핵심3\n[SUMMARY_END]\n\n"
        "분량: 2500자 이상. 반드시 완성된 글.\n\n"
        "출력:\n제목: (검색에 유리한 제목)\n---\n(본문)"
    )

    print("[AI] Gemini 생활정보 작성 중...")
    full_text = call_gemini(prompt, max_tokens=6000)
    title, body = parse_gemini_output(full_text, title_base)

    if is_duplicate(title):
        print("[중복] 건너뜀: " + title)
        return None

    save_used_life(title)
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
        "축구": "soccer football player",
        "야구": "baseball player",
        "농구": "basketball player",
        "손흥민": "soccer player football",
        "류현진": "baseball pitcher",
        "코스피": "stock market chart",
        "부동산": "real estate building",
        "금리": "finance money banking",
        "환율": "currency exchange money",
        "드라마": "korean drama tv",
        "아이돌": "kpop concert music",
        "연예": "entertainment stage performance",
        "사건": "police investigation",
        "정치": "government politics",
        "경제": "business finance economy",
    }
    for kor, eng in keyword_map.items():
        if kor in title:
            return eng
    category_defaults = {
        "스포츠이슈": "sports athlete action",
        "경제뉴스": "business finance economy",
        "전국이슈": "city korea urban street",
        "연예이슈": "stage performance music concert",
        "생활정보": "document office paperwork",
    }
    return category_defaults.get(category, "news media")


def get_images_unsplash(keyword, count=3):
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


def get_images(keyword, count=3, title="", category=""):
    if title or category:
        keyword = get_image_keyword_from_title(title, category)
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
    html += '<p style="font-size:12px;color:#999;margin-top:8px;">Photo by <a href="' + img["author_url"] + '" style="color:#999;">' + img["author"] + "</a> on " + source + "</p>"
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
        raise Exception("토큰 발급 실패 상태코드: " + str(response.status_code))
    data = response.json()
    token = data.get("access_token", "")
    if not token:
        raise Exception("access_token 없음: " + str(data))
    return token


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
    labels = [category, "시사칼럼", "이슈해설"]

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
            print("[응답] 상태코드: " + str(response.status_code))
            if response.status_code == 200:
                post_url = response.json().get("url", "")
                print("발행 완료! " + post_url)
                send_telegram(post_data["title"], post_url, category)
                send_facebook(post_data["title"], post_url, category)
                return True
            else:
                print("실패: " + response.text[:300])
                if attempt <= retry:
                    time.sleep(10)
        except Exception as e:
            print("[오류] " + str(e))
            if attempt <= retry:
                time.sleep(10)
    return False


if __name__ == "__main__":
    print("=" * 50)
    print("insaplayer v13 - 이슈칼럼 + 생활정보 병행")
    print("실행 시각: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)
    test_apis()
    try:
        post = generate_post()
        if post is None:
            print("[종료] 중복 또는 수집 실패")
            exit(0)
        images = get_images("", count=3, title=post["title"], category=post["category"])
        post_to_blogger(post, images)
        print("\n모든 작업 완료!")
    except Exception as e:
        print("\n오류 발생: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
