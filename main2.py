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
YEAR = datetime.now().strftime("%Y")

CATEGORY_EMOJI = {
    "사회이슈": "🔥", "경제": "💰", "연예": "🎭", "스포츠": "⚽", "IT과학": "💻",
    "주민등록": "🪪", "부동산주거": "🏠", "금융세금": "💳", "자동차운전": "🚗",
    "육아출산": "👶", "신혼결혼": "💍", "취업청년": "🎓", "1인가구": "🏠",
    "복지의료": "🏥", "정부디지털": "📱", "사업자": "💼", "여권해외": "✈️",
}

USED_TITLES_FILE = "used_titles2.json"
USED_IMAGES_FILE = "used_images2.json"

# 네이버 뉴스 섹션ID
NAVER_SECTION_MAP = {
    "사회이슈": "102", "경제": "101", "연예": "106", "스포츠": "107", "IT과학": "105",
}

# ──────────────────────────────────────────────
# ✅ 생활정보 TOPICS 118개
# ──────────────────────────────────────────────
LIFE_TOPICS = [
    # 주민등록/신분증
    {"title": "주민등록등본 인터넷 발급방법 정부24 완벽 가이드", "category": "주민등록", "keyword": "주민등록등본 발급"},
    {"title": "주민등록초본 발급방법 및 등본과 차이점 정리", "category": "주민등록", "keyword": "주민등록초본 발급"},
    {"title": "주민등록증 분실 재발급 방법과 기간 총정리", "category": "주민등록", "keyword": "주민등록증 재발급"},
    {"title": "주민등록증 갱신 대상과 신청방법 " + YEAR, "category": "주민등록", "keyword": "주민등록증 갱신"},
    {"title": "전입신고 방법 완벽 가이드 (온라인/오프라인)", "category": "주민등록", "keyword": "전입신고 방법"},
    {"title": "주민등록 주소변경 후 해야 할 것들 총정리", "category": "주민등록", "keyword": "주소변경 후 할일"},
    {"title": "외국인등록증 발급 및 갱신 방법 한국어 가이드", "category": "주민등록", "keyword": "외국인등록증 발급"},
    # 가족관계/혼인
    {"title": "가족관계증명서 발급방법 종류별 완벽 정리", "category": "주민등록", "keyword": "가족관계증명서 발급"},
    {"title": "혼인관계증명서 발급방법과 용도 총정리", "category": "신혼결혼", "keyword": "혼인관계증명서 발급"},
    {"title": "혼인신고 방법 완벽 가이드 (온라인/오프라인 비교)", "category": "신혼결혼", "keyword": "혼인신고 방법"},
    {"title": "이혼신고 방법과 필요 서류 총정리", "category": "신혼결혼", "keyword": "이혼신고 방법"},
    {"title": "출생신고 방법 및 기간 (병원/동사무소/온라인)", "category": "육아출산", "keyword": "출생신고 방법"},
    {"title": "사망신고 방법 및 필요서류 총정리", "category": "복지의료", "keyword": "사망신고 방법"},
    # 부동산/주거
    {"title": "전입신고 안 하면 생기는 일 전세사기 예방 필독", "category": "부동산주거", "keyword": "전입신고 안하면"},
    {"title": "확정일자 받는 방법 완벽 가이드 (온라인/오프라인)", "category": "부동산주거", "keyword": "확정일자 받기"},
    {"title": "전세권 설정 방법과 비용 총정리", "category": "부동산주거", "keyword": "전세권 설정"},
    {"title": "임대차계약서 작성 시 반드시 확인할 것 10가지", "category": "부동산주거", "keyword": "임대차계약서 확인"},
    {"title": "전월세 신고제 대상과 신고방법 " + YEAR, "category": "부동산주거", "keyword": "전월세 신고제"},
    {"title": "부동산 등기부등본 보는 방법 완벽 가이드", "category": "부동산주거", "keyword": "등기부등본 보기"},
    {"title": "건축물대장 발급방법과 보는 법 총정리", "category": "부동산주거", "keyword": "건축물대장 발급"},
    {"title": "전세사기 피하는 법 체크리스트 완벽 정리", "category": "부동산주거", "keyword": "전세사기 예방"},
    {"title": "주택청약통장 만들기 및 청약 신청방법 총정리", "category": "부동산주거", "keyword": "주택청약 방법"},
    {"title": "청년 전세자금대출 조건과 신청방법 " + YEAR, "category": "취업청년", "keyword": "청년 전세자금대출"},
    {"title": "버팀목 전세자금대출 " + YEAR + " 조건 정리", "category": "부동산주거", "keyword": "버팀목 전세자금대출"},
    {"title": "LH 청년매입임대주택 신청방법 완벽 가이드", "category": "취업청년", "keyword": "LH 청년매입임대"},
    {"title": "행복주택 신청자격과 방법 총정리 " + YEAR, "category": "취업청년", "keyword": "행복주택 신청"},
    # 금융/세금
    {"title": "종합소득세 신고방법 직장인 프리랜서 완벽 가이드", "category": "금융세금", "keyword": "종합소득세 신고"},
    {"title": "연말정산 환급 최대로 받는 방법 " + YEAR, "category": "금융세금", "keyword": "연말정산 환급"},
    {"title": "연말정산 간소화 서비스 사용법 총정리", "category": "금융세금", "keyword": "연말정산 간소화"},
    {"title": "부가가치세 신고방법 간이 일반 완벽 정리", "category": "금융세금", "keyword": "부가가치세 신고"},
    {"title": "재산세 납부방법 및 감면 조건 총정리", "category": "금융세금", "keyword": "재산세 납부"},
    {"title": "자동차세 연납 신청방법 할인 받기 완벽 가이드", "category": "자동차운전", "keyword": "자동차세 연납"},
    {"title": "국민연금 납부예외 신청방법과 조건", "category": "금융세금", "keyword": "국민연금 납부예외"},
    {"title": "건강보험 피부양자 등록 방법과 조건 " + YEAR, "category": "금융세금", "keyword": "건강보험 피부양자"},
    {"title": "건강보험료 줄이는 합법적인 방법 총정리", "category": "금융세금", "keyword": "건강보험료 절감"},
    {"title": "지역건강보험료 계산법 및 감면 방법", "category": "금융세금", "keyword": "지역건강보험료"},
    {"title": "금융인증서 발급방법 공동인증서 대체 완벽 가이드", "category": "정부디지털", "keyword": "금융인증서 발급"},
    {"title": "신용점수 올리는 현실적인 방법 총정리", "category": "금융세금", "keyword": "신용점수 올리기"},
    # 자동차/운전
    {"title": "자동차 이전등록 방법 중고차 구매 후 총정리", "category": "자동차운전", "keyword": "자동차 이전등록"},
    {"title": "자동차 등록증 재발급 방법과 절차", "category": "자동차운전", "keyword": "자동차등록증 재발급"},
    {"title": "운전면허증 재발급 방법과 필요서류", "category": "자동차운전", "keyword": "운전면허 재발급"},
    {"title": "운전면허 갱신 대상과 방법 " + YEAR, "category": "자동차운전", "keyword": "운전면허 갱신"},
    {"title": "자동차 과태료 조회 및 납부방법 완벽 가이드", "category": "자동차운전", "keyword": "자동차 과태료"},
    # 육아/출산
    {"title": "부모급여 신청방법 및 " + YEAR + " 금액 정리", "category": "육아출산", "keyword": "부모급여 신청"},
    {"title": "아동수당 신청방법과 지급일 총정리 " + YEAR, "category": "육아출산", "keyword": "아동수당 신청"},
    {"title": "첫만남이용권 사용처와 신청방법 " + YEAR, "category": "육아출산", "keyword": "첫만남이용권"},
    {"title": "출산급여 신청방법 직장인 자영업자 비교", "category": "육아출산", "keyword": "출산급여 신청"},
    {"title": "육아휴직 신청방법과 급여 계산법 총정리", "category": "육아출산", "keyword": "육아휴직 신청"},
    {"title": "배우자 출산휴가 신청방법과 기간 총정리", "category": "육아출산", "keyword": "배우자 출산휴가"},
    {"title": "어린이집 입소 대기 빠르게 하는 법 실전 가이드", "category": "육아출산", "keyword": "어린이집 입소"},
    {"title": "아이사랑쿠폰 사용처와 신청방법 " + YEAR, "category": "육아출산", "keyword": "아이사랑쿠폰"},
    {"title": "다자녀 혜택 총정리 2명 3명 기준 " + YEAR, "category": "육아출산", "keyword": "다자녀 혜택"},
    # 신혼/결혼
    {"title": "신혼부부 버팀목 대출 " + YEAR + " 조건 정리", "category": "신혼결혼", "keyword": "신혼부부 대출"},
    {"title": "신혼부부 청약 조건 및 가점 계산법 " + YEAR, "category": "신혼결혼", "keyword": "신혼부부 청약"},
    {"title": "결혼 준비 순서와 비용 현실 총정리", "category": "신혼결혼", "keyword": "결혼 준비 비용"},
    {"title": "신혼부부 정부지원금 총정리 " + YEAR, "category": "신혼결혼", "keyword": "신혼부부 지원금"},
    {"title": "부부 건강보험 합산 방법과 절약 팁", "category": "신혼결혼", "keyword": "부부 건강보험"},
    # 취업/청년
    {"title": "청년도약계좌 " + YEAR + " 조건과 신청방법", "category": "취업청년", "keyword": "청년도약계좌"},
    {"title": "청년내일저축계좌 신청방법과 조건 " + YEAR, "category": "취업청년", "keyword": "청년내일저축계좌"},
    {"title": "청년월세지원금 신청방법 지역별 정리 " + YEAR, "category": "취업청년", "keyword": "청년월세지원금"},
    {"title": "국민취업지원제도 신청방법 및 지원금액 " + YEAR, "category": "취업청년", "keyword": "국민취업지원제도"},
    {"title": "국민내일배움카드 신청방법 훈련비 지원 " + YEAR, "category": "취업청년", "keyword": "국민내일배움카드"},
    {"title": "실업급여 신청 조건과 방법 완벽 가이드 " + YEAR, "category": "취업청년", "keyword": "실업급여 신청"},
    {"title": "실업급여 얼마나 받나 계산법 총정리", "category": "취업청년", "keyword": "실업급여 계산"},
    {"title": "퇴직금 계산법 및 받는 방법 총정리", "category": "취업청년", "keyword": "퇴직금 계산"},
    {"title": "자격증 국비지원 받는 방법 총정리 " + YEAR, "category": "취업청년", "keyword": "자격증 국비지원"},
    {"title": "IT 취업 국비지원 과정 신청방법 " + YEAR, "category": "취업청년", "keyword": "IT 국비지원"},
    # 1인가구/자취
    {"title": "자취 처음 시작할 때 체크리스트 완벽 정리", "category": "1인가구", "keyword": "자취 체크리스트"},
    {"title": "원룸 계약 시 반드시 확인할 것 10가지", "category": "1인가구", "keyword": "원룸 계약 확인"},
    {"title": "관리비에 포함되는 것 vs 따로 내는 것 정리", "category": "1인가구", "keyword": "관리비 포함 항목"},
    {"title": "혼자 사는 사람 건강보험료 줄이는 법", "category": "1인가구", "keyword": "1인가구 건강보험"},
    {"title": "1인가구 지원정책 총정리 " + YEAR, "category": "1인가구", "keyword": "1인가구 지원"},
    {"title": "이사 후 도시가스 신청방법 완벽 가이드", "category": "1인가구", "keyword": "도시가스 신청"},
    {"title": "이사 후 인터넷 TV 설치 방법 총정리", "category": "1인가구", "keyword": "이사 인터넷 설치"},
    # 복지/의료
    {"title": "기초생활수급자 신청방법과 조건 " + YEAR, "category": "복지의료", "keyword": "기초생활수급자 신청"},
    {"title": "차상위계층 신청방법과 혜택 총정리 " + YEAR, "category": "복지의료", "keyword": "차상위계층 신청"},
    {"title": "기초연금 신청방법 65세 이상 완벽 가이드", "category": "복지의료", "keyword": "기초연금 신청"},
    {"title": "장애인등록 방법과 혜택 총정리", "category": "복지의료", "keyword": "장애인등록 방법"},
    {"title": "긴급복지지원 신청방법과 대상 총정리", "category": "복지의료", "keyword": "긴급복지지원"},
    {"title": "복지로 원스톱 서비스 사용법 완벽 가이드", "category": "복지의료", "keyword": "복지로 사용법"},
    {"title": "노인장기요양보험 신청방법 총정리", "category": "복지의료", "keyword": "노인장기요양 신청"},
    {"title": "암환자 의료비 지원 신청방법 " + YEAR, "category": "복지의료", "keyword": "암환자 의료비 지원"},
    # 정부디지털
    {"title": "정부24 회원가입 및 사용법 완벽 가이드", "category": "정부디지털", "keyword": "정부24 사용법"},
    {"title": "정부24 모바일 앱 주요기능 총정리", "category": "정부디지털", "keyword": "정부24 앱"},
    {"title": "국민비서 구삐 알림 서비스 신청방법", "category": "정부디지털", "keyword": "국민비서 구삐"},
    {"title": "인터넷 등기소 사용법 완벽 가이드", "category": "정부디지털", "keyword": "인터넷 등기소"},
    {"title": "카카오 민원서비스 사용법 총정리", "category": "정부디지털", "keyword": "카카오 민원"},
    # 사업자/프리랜서
    {"title": "사업자등록증 발급방법 개인 법인 완벽 가이드", "category": "사업자", "keyword": "사업자등록 발급"},
    {"title": "간이과세자 vs 일반과세자 차이와 선택법", "category": "사업자", "keyword": "간이과세 일반과세"},
    {"title": "프리랜서 세금 신고방법 완벽 가이드 " + YEAR, "category": "사업자", "keyword": "프리랜서 세금"},
    {"title": "사업자 폐업신고 방법 총정리", "category": "사업자", "keyword": "폐업신고 방법"},
    {"title": "소상공인 지원금 신청방법 총정리 " + YEAR, "category": "사업자", "keyword": "소상공인 지원금"},
    # 여권/해외
    {"title": "여권 발급방법 신규 갱신 완벽 가이드 " + YEAR, "category": "여권해외", "keyword": "여권 발급방법"},
    {"title": "여권 분실 재발급 방법 해외에서도 가능할까", "category": "여권해외", "keyword": "여권 재발급"},
    {"title": "해외 장기 거주 시 건강보험 처리방법", "category": "여권해외", "keyword": "해외 건강보험"},
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
    if len(used) > 50:
        used = used[-50:]
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
# ✅ 기사 원문 크롤링 (이슈 글용)
# ──────────────────────────────────────────────
def crawl_article(article_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://news.naver.com",
        "Accept-Language": "ko-KR,ko;q=0.9",
    }
    result = {"image_url": "", "publisher": "", "body": ""}
    try:
        response = requests.get(article_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return result
        html = response.text
        og = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
        if not og:
            og = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html)
        if og:
            img = og.group(1).strip()
            if img.startswith("http"):
                result["image_url"] = img
        pub = re.search(r'<meta[^>]+property=["\']og:site_name["\'][^>]+content=["\']([^"\']+)["\']', html)
        if pub:
            result["publisher"] = pub.group(1).strip()
        for pattern in [r'<div[^>]*id="dic_area"[^>]*>(.*?)</div>', r'<article[^>]*>(.*?)</article>']:
            m = re.search(pattern, html, re.DOTALL)
            if m:
                text = re.sub(r'<[^>]+>', ' ', m.group(1))
                result["body"] = re.sub(r'\s+', ' ', text).strip()[:2000]
                break
        return result
    except Exception as e:
        print("[크롤링 오류] " + str(e))
        return result


def get_naver_top_news():
    print("[네이버 많이 본 뉴스] 수집 중...")
    today_str = datetime.now().strftime("%Y%m%d")
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "ko-KR,ko;q=0.9"}
    all_results = []
    for category, section_id in NAVER_SECTION_MAP.items():
        url = ("https://news.naver.com/main/ranking/popularDay.naver"
               "?rankingType=popular_day&sectionId=" + section_id + "&date=" + today_str)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                links = re.findall(
                    r'<a[^>]+href="(https://n\.news\.naver\.com/[^"]+)"[^>]*>\s*([^<]{8,80})\s*</a>',
                    response.text
                )
                seen = set()
                for link_url, title in links:
                    title = title.strip()
                    if len(title) > 7 and title not in seen:
                        seen.add(title)
                        all_results.append({"category": category, "title": title, "url": link_url})
                        print("[" + category + "] " + title[:40])
                        if len([r for r in all_results if r["category"] == category]) >= 5:
                            break
        except Exception as e:
            print("[랭킹 오류] " + category + ": " + str(e))
    print("[수집 완료] " + str(len(all_results)) + "개")
    return all_results


def get_naver_search(keyword):
    if not NAVER_CLIENT_ID:
        return []
    try:
        response = requests.get(
            "https://openapi.naver.com/v1/search/news.json",
            headers={"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET},
            params={"query": keyword, "display": 5, "sort": "date"},
            timeout=10
        )
        if response.status_code == 200:
            items = response.json().get("items", [])
            results = []
            for item in items:
                title = re.sub(r'<[^>]+>', '', item.get("title", "")).replace("&amp;", "&")
                desc = re.sub(r'<[^>]+>', '', item.get("description", "")).replace("&amp;", "&")
                link = item.get("link", "")
                results.append({"title": title, "desc": desc, "url": link})
            return results
    except Exception as e:
        print("[검색 오류] " + str(e))
    return []


def get_google_trends():
    try:
        response = requests.get(
            "https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR",
            headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )
        if response.status_code == 200:
            titles = re.findall(r'<title><!\[CDATA\[([^\]]+)\]\]></title>', response.text)
            return [t for t in titles if t != "Google Trends"][:10]
    except:
        pass
    return []


def call_gemini(prompt, max_tokens=8000):
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY 없음")
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           "gemini-2.5-flash:generateContent?key=" + GEMINI_API_KEY)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.85, "topP": 0.95}
    }
    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, timeout=120)
            print("[Gemini] " + str(response.status_code))
            if response.status_code == 200:
                candidates = response.json().get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    return "".join(p.get("text", "") for p in parts)
            elif response.status_code in [429, 503]:
                time.sleep(30 * (attempt + 1))
            else:
                raise Exception("Gemini " + str(response.status_code))
        except Exception as e:
            print("[Gemini 오류] " + str(e))
            if attempt < 2:
                time.sleep(20)
            else:
                raise
    raise Exception("Gemini 재시도 초과")


# ──────────────────────────────────────────────
# ✅ 모드 1: 이슈 칼럼
# ──────────────────────────────────────────────
def generate_issue_post():
    print("\n[이슈 모드] 네이버 랭킹 뉴스 기반 칼럼")
    ranking_news = get_naver_top_news()
    trending = get_google_trends()

    if not ranking_news:
        return None

    used = load_used_titles()
    filtered = [i for i in ranking_news if not any(i["title"][:8] in u or u[:8] in i["title"] for u in used)]
    if not filtered:
        filtered = ranking_news

    selected = None
    if trending:
        for item in filtered:
            for kw in trending:
                if len(kw) >= 3 and kw[:3] in item["title"]:
                    selected = item
                    break
            if selected:
                break
    if not selected:
        selected = random.choice(filtered[:5] if len(filtered) >= 5 else filtered)

    category = selected["category"]
    hot_title = selected["title"]
    hot_url = selected.get("url", "")
    print("[선택] " + hot_title[:40] + " (" + category + ")")

    # 기사 원문 크롤링
    article_data = {"image_url": "", "publisher": "", "body": ""}
    related = get_naver_search(hot_title[:15])
    crawl_targets = ([{"url": hot_url}] if hot_url else []) + [{"url": a["url"]} for a in related[:3] if a["url"]]
    used_images = load_used_images()
    for target in crawl_targets:
        crawled = crawl_article(target["url"])
        if crawled["image_url"] and crawled["image_url"] not in used_images:
            article_data = crawled
            save_used_image(crawled["image_url"])
            break
        elif crawled["body"] and not article_data["body"]:
            article_data.update(crawled)

    # 컨텍스트
    ctx = "=== 오늘(" + TODAY + ") 네이버 많이 본 뉴스 ===\n이슈: " + hot_title + "\n"
    if article_data["body"]:
        ctx += "\n[기사 원문]\n" + article_data["body"] + "\n"
    if related:
        ctx += "\n[관련 기사]\n" + "\n".join(str(i+1)+". "+a["title"]+": "+a["desc"][:80] for i,a in enumerate(related[:4]))

    prompt = (
        "당신은 날카로운 시각을 가진 시사 해설 칼럼니스트입니다.\n"
        "아래 실제 기사 원문을 반드시 기반으로 작성하세요. 원문에 없는 내용 상상 금지.\n"
        "한국어만 사용.\n\n"
        "기사 내용:\n" + ctx + "\n\n"
        "원칙: 날카로운 훅으로 시작, 팩트는 원문 기반만, 이면 분석, 독자 일상 연결, 질문으로 마무리.\n"
        "금지: '알아보겠습니다', '살펴보겠습니다', AI 나열식.\n\n"
        "구조:\n1. 훅(2~3줄)\n2. ##핵심키워드##\n"
        "3. [📌 핵심 팩트]\n[🔍 왜 지금인가]\n[💡 이면]\n[🙋 나와 상관]\n"
        "4. 마무리 질문\n5. [SUMMARY_START]\n핵심1\n핵심2\n핵심3\n[SUMMARY_END]\n\n"
        "분량: 3000자 이상. 카테고리: " + category + "\n\n"
        "출력:\n제목: (날짜/카테고리명 금지)\n---\n(본문)"
    )

    print("[AI] Gemini 이슈 칼럼 작성 중...")
    full_text = call_gemini(prompt)
    title, body = parse_output(full_text, hot_title)

    if is_duplicate(title):
        return None
    save_used_title(title)
    print("[완료] " + title)

    return {
        "title": title, "body": body, "category": category,
        "mode": "issue",
        "article_image": article_data["image_url"],
        "article_publisher": article_data["publisher"],
        "article_url": hot_url,
    }


# ──────────────────────────────────────────────
# ✅ 모드 2: 생활정보 가이드
# ──────────────────────────────────────────────
def generate_life_post():
    print("\n[생활정보 모드] 민원/생활 가이드")
    used = load_used_titles()
    available = [t for t in LIFE_TOPICS if not any(t["title"][:10] in u or u[:10] in t["title"] for u in used)]
    if not available:
        available = LIFE_TOPICS
    topic = random.choice(available)

    category = topic["category"]
    title_base = topic["title"]
    keyword = topic["keyword"]
    print("[선택] " + title_base + " (" + category + ")")

    # 관련 공식 정보 검색
    related = get_naver_search(keyword)
    ctx = "=== 작성 주제 ===\n" + title_base + "\n검색 키워드: " + keyword + "\n\n"
    if related:
        ctx += "=== 관련 정보 ===\n" + "\n".join(str(i+1)+". "+a["title"]+": "+a["desc"][:100] for i,a in enumerate(related[:5]))

    prompt = (
        "당신은 대한민국 행정/생활정보 전문 블로거입니다.\n"
        "독자가 이 글만 읽으면 실제로 업무를 처리할 수 있게 써야 합니다.\n"
        "한국어만 사용. 정확한 절차와 링크 안내 포함.\n\n"
        "주제: " + title_base + "\n"
        "참고 정보:\n" + ctx + "\n\n"
        "✅ 작성 원칙:\n"
        "1. 도입: '나도 처음엔 몰랐는데...' 같은 공감 문장으로 시작\n"
        "2. 핵심 정보를 단계별(1단계→2단계→3단계)로 명확하게\n"
        "3. 준비물/필요서류 목록 반드시 포함\n"
        "4. 처리 시간/비용/유의사항 포함\n"
        "5. 온라인(정부24 등) + 오프라인 방법 모두 안내\n"
        "6. 마지막에 자주 묻는 질문 2~3개\n"
        "7. 친근하고 실용적인 문체 (딱딱한 공문서체 금지)\n\n"
        "구조:\n"
        "1. 공감 도입 (2~3줄)\n"
        "2. ##핵심요약##\n"
        "3. [📋 준비물과 필요서류]\n"
        "   [💻 온라인 신청방법 단계별]\n"
        "   [🏛️ 오프라인 방문 방법]\n"
        "   [⚠️ 주의사항과 유의점]\n"
        "   [❓ 자주 묻는 질문]\n"
        "4. 마무리 한 줄 팁\n"
        "5. [SUMMARY_START]\n핵심1\n핵심2\n핵심3\n[SUMMARY_END]\n\n"
        "분량: 2500자 이상. 반드시 완성된 글.\n"
        "카테고리: " + category + "\n\n"
        "출력:\n제목: (검색에 유리한 제목. 연도 포함 가능)\n---\n(본문)"
    )

    print("[AI] Gemini 생활정보 가이드 작성 중...")
    full_text = call_gemini(prompt)
    title, body = parse_output(full_text, title_base)

    if is_duplicate(title):
        return None
    save_used_title(title)
    print("[완료] " + title)

    return {
        "title": title, "body": body, "category": category,
        "mode": "life",
        "article_image": "", "article_publisher": "", "article_url": "",
    }


def parse_output(full_text, fallback_title):
    lines = full_text.strip().split("\n")
    title, body_lines, sep = "", [], False
    for line in lines:
        if line.startswith("제목:"):
            title = line.replace("제목:", "").strip()
        elif not title and "제목" in line and ":" in line:
            title = line.split(":", 1)[-1].strip()
        elif line.strip() == "---":
            sep = True
        elif sep:
            body_lines.append(line)
    body = "\n".join(body_lines).strip()
    if not title:
        title = fallback_title[:50]
    if not body:
        body = full_text
    return title, body


def generate_post():
    # 50:50 확률로 이슈 칼럼 vs 생활정보 선택
    mode = random.choice(["issue", "issue", "life"])  # 이슈 칼럼 약간 더 자주
    print("\n[모드 선택] " + ("이슈 칼럼" if mode == "issue" else "생활정보 가이드"))

    if mode == "issue":
        post = generate_issue_post()
        if post is None:
            print("[이슈 실패] 생활정보 모드로 전환")
            post = generate_life_post()
    else:
        post = generate_life_post()
        if post is None:
            print("[생활정보 실패] 이슈 모드로 전환")
            post = generate_issue_post()
    return post


# ──────────────────────────────────────────────
# ✅ HTML 변환 (이슈/생활정보 공통)
# ──────────────────────────────────────────────
def make_article_image_html(image_url, publisher, article_url, issue_title):
    if not image_url:
        return ""
    source = publisher if publisher else "언론사"
    html = '<div style="text-align:center;margin:24px 0;">'
    html += '<img src="' + image_url + '" alt="' + issue_title[:30] + '" style="max-width:100%;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.15);"/>'
    html += '<p style="font-size:12px;color:#999;margin-top:8px;">© ' + source + ' | 보도 목적 인용 | '
    if article_url:
        html += '<a href="' + article_url + '" target="_blank" rel="noopener" style="color:#999;">원문 기사 보기</a>'
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
    mode = post_data.get("mode", "issue")
    emoji = CATEGORY_EMOJI.get(category, "📰")

    # 모드별 배지 색상
    badge_color = "#e65100" if mode == "issue" else "#1565c0"
    mode_label = "이슈해설" if mode == "issue" else "생활정보가이드"

    html = (
        '<div style="display:inline-block;background:' + badge_color + ';color:#fff;'
        'font-size:13px;padding:5px 14px;border-radius:20px;margin-bottom:4px;font-weight:600;">'
        + emoji + " " + category + "</div>\n"
        '<div style="display:inline-block;background:#f5f5f5;color:#666;'
        'font-size:12px;padding:4px 10px;border-radius:20px;margin-bottom:8px;margin-left:6px;">'
        + mode_label + "</div>\n"
        '<div style="font-size:13px;color:#888;margin-bottom:20px;">📅 ' + TODAY + "</div>\n"
    )

    # 이슈 모드: 기사 원문 이미지 + 출처
    if mode == "issue" and post_data.get("article_image"):
        html += make_article_image_html(
            post_data["article_image"], post_data["article_publisher"],
            post_data["article_url"], post_data["title"]
        )
        if post_data.get("article_url"):
            html += (
                '<div style="background:#f5f5f5;border-left:4px solid #e65100;'
                'padding:12px 16px;margin:16px 0;border-radius:0 8px 8px 0;">'
                '<p style="margin:0;font-size:13px;color:#666;">📰 실제 보도된 뉴스 기반 시사 해설 | '
                '<a href="' + post_data["article_url"] + '" target="_blank" rel="noopener" style="color:#e65100;font-weight:600;">원문 기사 →</a></p>'
                '</div>\n'
            )

    # 생활정보 모드: 정부 안내 배너
    if mode == "life":
        html += (
            '<div style="background:#e3f2fd;border-left:4px solid #1565c0;'
            'padding:12px 16px;margin:16px 0;border-radius:0 8px 8px 0;">'
            '<p style="margin:0;font-size:13px;color:#1565c0;font-weight:600;">'
            '📋 이 글은 정부 공식 정보를 기반으로 작성된 생활정보 가이드입니다. '
            '최신 정보는 <a href="https://www.gov.kr" target="_blank" style="color:#1565c0;">정부24</a> 또는 '
            '<a href="https://www.bokjiro.go.kr" target="_blank" style="color:#1565c0;">복지로</a>에서 확인하세요.</p>'
            '</div>\n'
        )

    summary_pattern = re.compile(r'\[SUMMARY_START\](.*?)\[SUMMARY_END\]', re.DOTALL)
    keyword_pattern = re.compile(r'##(.+?)##')

    summary_match = summary_pattern.search(body)
    summary_html = make_summary_html(summary_match.group(1)) if summary_match else ""
    clean_body = summary_pattern.sub("[SUMMARY_PLACEHOLDER]", body)

    headings = [h for h in re.findall(r'\[([^\]]+)\]', clean_body) if h != "SUMMARY_PLACEHOLDER"]
    if headings:
        toc = '<div style="background:#f8f9ff;border:1px solid #e0e0e0;border-radius:10px;padding:20px 24px;margin:24px 0;">'
        toc += '<p style="font-weight:700;font-size:15px;color:' + badge_color + ';margin-bottom:12px;">📋 목차</p>'
        toc += '<ol style="margin:0;padding-left:20px;">'
        for h in headings:
            clean_h = re.sub(r'^[^\w가-힣]+', '', h).strip()
            if clean_h:
                toc += '<li style="margin:6px 0;font-size:15px;color:#444;line-height:1.6;">' + clean_h + '</li>'
        toc += '</ol></div>\n'
        html += toc

    def replace_keyword(m):
        return (
            '<div style="margin:28px 0 12px 0;">'
            '<span style="display:inline-block;font-size:28px;font-weight:900;color:' + badge_color + ';'
            'border-bottom:3px solid ' + badge_color + ';padding-bottom:4px;">'
            + m.group(1) + '</span></div>\n'
        )

    para_count = 0
    for para in clean_body.split("\n"):
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
                'background:linear-gradient(90deg,' + badge_color + ',' + badge_color + 'dd);'
                'color:#fff;padding:12px 20px;border-radius:8px;">' + heading + "</h2>\n"
            )
            continue
        if len(para.strip()) > 1 and para.strip()[0].isdigit() and para.strip()[1] in [".", ")"]:
            html += (
                '<div style="display:flex;align-items:flex-start;margin:10px 0;padding:12px 16px;'
                'background:#f5f5f5;border-radius:8px;">'
                '<span style="color:' + badge_color + ';font-weight:700;margin-right:12px;">'
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
                '<div style="border-left:4px solid ' + badge_color + ';padding:14px 20px;margin:20px 0;'
                'background:#f9f9f9;border-radius:0 8px 8px 0;">'
                '<p style="margin:0;font-size:16px;line-height:1.9;color:#1a1a1a;font-weight:500;">'
                + para.strip() + '</p></div>\n'
            )
        else:
            html += '<p style="margin:14px 0;line-height:1.9;font-size:16px;color:#333;">' + para.strip() + '</p>\n'

    return html


def get_access_token():
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={"client_id": GOOGLE_CLIENT_ID, "client_secret": GOOGLE_CLIENT_SECRET,
              "refresh_token": GOOGLE_REFRESH_TOKEN, "grant_type": "refresh_token"},
        timeout=10
    )
    if response.status_code != 200:
        raise Exception("토큰 발급 실패")
    return response.json()["access_token"]


def send_telegram(title, post_url, category):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    emoji = CATEGORY_EMOJI.get(category, "📰")
    try:
        requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": emoji + " " + title + "\n\n👉 " + post_url},
            timeout=10
        )
        print("[텔레그램] 공유 성공!")
    except Exception as e:
        print("[텔레그램 오류] " + str(e))


def send_facebook(title, post_url, category):
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        return
    emoji = CATEGORY_EMOJI.get(category, "📰")
    try:
        requests.post(
            "https://graph.facebook.com/v19.0/" + FACEBOOK_PAGE_ID + "/feed",
            data={"message": emoji + " " + title + "\n\n자세히 읽기 👉 " + post_url,
                  "link": post_url, "access_token": FACEBOOK_ACCESS_TOKEN},
            timeout=10
        )
        print("[페이스북] 공유 성공!")
    except Exception as e:
        print("[페이스북 오류] " + str(e))


def post_to_blogger(post_data, retry=2):
    print("\n[Blogger] 포스팅 시작...")
    category = post_data["category"]
    mode = post_data.get("mode", "issue")
    labels = [category, "시사칼럼" if mode == "issue" else "생활정보", "많이본뉴스" if mode == "issue" else "민원가이드"]

    for attempt in range(1, retry + 2):
        try:
            access_token = get_access_token()
            body_html = body_to_html(post_data["body"], post_data)
            response = requests.post(
                "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts?isDraft=false",
                headers={"Authorization": "Bearer " + access_token, "Content-Type": "application/json"},
                json={"kind": "blogger#post", "title": post_data["title"],
                      "content": body_html, "labels": labels, "status": "LIVE"},
                timeout=30
            )
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
    print("insaplayer v11 — 이슈칼럼 + 생활정보 병행")
    print("실행 시각: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)

    if not GEMINI_API_KEY:
        print("[오류] GEMINI_API_KEY 없음")
        exit(1)

    try:
        post = generate_post()
        if post is None:
            print("[종료] 발행 실패 또는 중복")
            exit(0)
        post_to_blogger(post)
        print("\n모든 작업 완료!")
    except Exception as e:
        print("\n오류 발생: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
