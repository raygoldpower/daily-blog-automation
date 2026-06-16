import os
import re
import json
import random
import requests
from datetime import datetime, timezone, timedelta

# ============================================================
# 환경변수
# ============================================================
ANTHROPIC_API_KEY     = os.environ.get("ANTHROPIC_API_KEY", "")
UNSPLASH_ACCESS_KEY   = os.environ.get("UNSPLASH_ACCESS_KEY", "")
PEXELS_API_KEY        = os.environ.get("PEXELS_API_KEY", "")
PIXABAY_API_KEY       = os.environ.get("PIXABAY_API_KEY", "")
GOOGLE_CLIENT_ID      = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET  = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN3 = os.environ.get("GOOGLE_REFRESH_TOKEN3", "")
BLOGGER_BLOG_ID3      = os.environ.get("BLOGGER_BLOG_ID3", "")
TELEGRAM_BOT_TOKEN    = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID      = os.environ.get("TELEGRAM_CHAT_ID", "")
FACEBOOK_PAGE_ID      = os.environ.get("FACEBOOK_PAGE_ID", "")
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN", "")

COUPANG_LINK = "https://link.coupang.com/a/dRhOlCLu5Q"

KST = timezone(timedelta(hours=9))
TODAY = datetime.now(KST).strftime("%Y년 %m월 %d일")

USED_TOPICS_FILE = "used_topics3.json"

# ============================================================
# TOPICS
# ============================================================
TOPICS = [
    # 허리/척추
    {"symptom": "오래 앉아 있으면 허리가 끊어질 것 같다", "category": "허리통증", "img_keyword": "back pain office worker"},
    {"symptom": "자고 일어날 때마다 허리가 뻣뻣하고 움직이기 힘들다", "category": "허리통증", "img_keyword": "morning back stiffness"},
    {"symptom": "허리를 앞으로 굽히면 당기는 느낌이 온다", "category": "허리통증", "img_keyword": "lower back stretch pain"},
    {"symptom": "앉아 있다 일어설 때 허리에서 소리가 나고 아프다", "category": "허리통증", "img_keyword": "standing up back pain"},
    # 목/어깨
    {"symptom": "자고 일어나면 목이 뻐근하고 두통까지 온다", "category": "목어깨통증", "img_keyword": "neck pain pillow"},
    {"symptom": "컴퓨터 앞에 앉으면 어깨가 귀 쪽으로 올라간다", "category": "목어깨통증", "img_keyword": "shoulder tension desk"},
    {"symptom": "고개를 돌릴 때 목에서 뚝 소리가 나고 불편하다", "category": "목어깨통증", "img_keyword": "neck cracking stiffness"},
    {"symptom": "한쪽 어깨만 계속 뭉치고 팔이 저리다", "category": "목어깨통증", "img_keyword": "shoulder muscle tension"},
    # 무릎/발목
    {"symptom": "계단을 오르내릴 때마다 무릎이 시큰거린다", "category": "무릎관절", "img_keyword": "knee pain stairs"},
    {"symptom": "오래 걷고 나면 무릎 안쪽이 붓고 뻐근하다", "category": "무릎관절", "img_keyword": "knee swelling walking"},
    {"symptom": "발목을 자주 삐끗해서 걷는 게 불안하다", "category": "발목관절", "img_keyword": "ankle sprain walking"},
    {"symptom": "운동할 때마다 무릎에서 소리가 나고 불안하다", "category": "무릎관절", "img_keyword": "knee exercise joint"},
    # 발바닥/족저
    {"symptom": "아침에 일어나 첫 발을 디딜 때 발바닥이 너무 아프다", "category": "족저근막", "img_keyword": "plantar fasciitis morning foot"},
    {"symptom": "오래 서 있으면 발바닥 가운데가 타는 듯이 아프다", "category": "족저근막", "img_keyword": "foot pain standing"},
    {"symptom": "하이힐을 신은 다음 날 발이 퉁퉁 붓는다", "category": "족저근막", "img_keyword": "foot swelling heels"},
    # 자세/체형
    {"symptom": "거울을 보면 한쪽 어깨가 내려가 있고 골반이 틀어져 있다", "category": "체형교정", "img_keyword": "posture imbalance body"},
    {"symptom": "앉으면 자꾸 한쪽으로 기울어지고 허리가 굽는다", "category": "체형교정", "img_keyword": "sitting posture slouch"},
    {"symptom": "사진을 찍으면 항상 머리가 앞으로 나와 있다", "category": "체형교정", "img_keyword": "forward head posture"},
    {"symptom": "서 있을 때 배가 앞으로 나오고 허리가 꺾인다", "category": "체형교정", "img_keyword": "anterior pelvic tilt posture"},
    # 사무직/재택
    {"symptom": "재택근무 이후로 허리와 목이 더 나빠진 것 같다", "category": "사무직자세", "img_keyword": "home office posture back"},
    {"symptom": "노트북만 쓰다 보니 목이 항상 아래로 꺾여 있다", "category": "사무직자세", "img_keyword": "laptop neck pain posture"},
    {"symptom": "의자에 오래 앉아 있으면 엉덩이가 저리고 다리가 붓는다", "category": "사무직자세", "img_keyword": "office chair hip pain"},
    {"symptom": "하루 종일 마우스를 쓰다 보니 손목이 저리고 아프다", "category": "사무직자세", "img_keyword": "wrist pain mouse keyboard"},
    # 코어/근력
    {"symptom": "조금만 걸어도 허리가 아프고 금방 피곤해진다", "category": "코어강화", "img_keyword": "core weakness fatigue walking"},
    {"symptom": "윗몸일으키기를 하면 목이 당겨서 배 운동이 안 된다", "category": "코어강화", "img_keyword": "core exercise neck strain"},
    {"symptom": "플랭크 자세를 잡으면 허리가 꺾이고 버티기 힘들다", "category": "코어강화", "img_keyword": "plank core weakness"},
    {"symptom": "서 있을 때 배에 힘이 없어 금방 자세가 무너진다", "category": "코어강화", "img_keyword": "core posture standing weakness"},
    # 밸런스/균형
    {"symptom": "한 발로 서면 금방 흔들리고 균형을 잡기 힘들다", "category": "밸런스훈련", "img_keyword": "balance training one leg"},
    {"symptom": "계단이나 내리막에서 무릎이 불안하고 다리가 떨린다", "category": "밸런스훈련", "img_keyword": "balance instability stairs"},
    {"symptom": "운동을 해도 몸의 좌우 균형이 안 맞는 것 같다", "category": "밸런스훈련", "img_keyword": "body balance asymmetry training"},
    # 수면/피로
    {"symptom": "자고 일어나도 개운하지 않고 온몸이 무겁다", "category": "수면피로", "img_keyword": "sleep fatigue morning tired"},
    {"symptom": "베개가 맞지 않는지 자고 나면 목이 항상 뻐근하다", "category": "수면피로", "img_keyword": "pillow neck pain sleep"},
    {"symptom": "매트리스가 꺼져서 자는 내내 허리가 불편하다", "category": "수면피로", "img_keyword": "mattress back pain sleep"},
    # 다이어트/체중
    {"symptom": "운동은 하고 싶은데 헬스장 가기가 너무 귀찮다", "category": "홈트레이닝", "img_keyword": "home workout exercise equipment"},
    {"symptom": "야식을 끊고 싶은데 밤만 되면 배가 고프다", "category": "다이어트", "img_keyword": "late night snack diet"},
    {"symptom": "운동 후 근육통이 너무 심해서 다음 날 움직이기 힘들다", "category": "홈트레이닝", "img_keyword": "muscle soreness recovery"},
    {"symptom": "체중은 그대로인데 배만 점점 나오는 것 같다", "category": "다이어트", "img_keyword": "belly fat posture diet"},
    # 두통/눈피로
    {"symptom": "오후만 되면 눈이 빡빡하고 머리가 지끈거린다", "category": "눈피로두통", "img_keyword": "eye strain headache screen"},
    {"symptom": "모니터를 오래 보면 눈이 침침하고 시야가 흐려진다", "category": "눈피로두통", "img_keyword": "eye fatigue monitor blur"},
    # 손목/팔꿈치
    {"symptom": "스마트폰을 오래 보면 손목이 저리고 엄지가 아프다", "category": "손목통증", "img_keyword": "phone wrist pain thumb"},
    {"symptom": "골프나 테니스 후 팔꿈치 바깥쪽이 너무 아프다", "category": "손목통증", "img_keyword": "tennis elbow pain"},
    # 고령/부모님
    {"symptom": "부모님이 무릎이 아파서 앉았다 일어나는 게 힘드시다", "category": "관절노화", "img_keyword": "elderly knee pain standing"},
    {"symptom": "어머니가 등이 굽어서 걸음이 불편하시다", "category": "관절노화", "img_keyword": "elderly posture back bent"},
]


# ============================================================
# 중복 방지
# ============================================================
def load_used_topics():
    if os.path.exists(USED_TOPICS_FILE):
        with open(USED_TOPICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_used_topic(symptom):
    used = load_used_topics()
    used.append(symptom)
    if len(used) > len(TOPICS) * 2:
        used = used[len(TOPICS):]
    with open(USED_TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, ensure_ascii=False, indent=2)


def pick_topic():
    used = load_used_topics()
    unused = [t for t in TOPICS if t["symptom"] not in used]
    if not unused:
        unused = TOPICS.copy()
    return random.choice(unused)


# ============================================================
# Claude API 호출
# ============================================================
def call_claude(prompt, max_tokens=4000):
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": "claude-sonnet-4-6",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers, json=body, timeout=120
        )
        r.raise_for_status()
        data = r.json()
        return data["content"][0]["text"]
    except Exception as e:
        print("[Claude API 오류] " + str(e))
        return ""


# ============================================================
# 글 생성 프롬프트
# ============================================================
def build_prompt(topic):
    symptom  = topic["symptom"]
    category = topic["category"]

    return (
        "당신은 생활 속 불편함을 직접 경험하고 해결한 이야기를 솔직하게 쓰는 블로그 작가입니다.\n\n"
        "## 글쓰기 핵심 원칙\n"
        "- 화자인 '나'의 경험에서 시작하세요. 독자에게 질문하지 마세요.\n"
        "- '나는 이랬어요' → 독자가 '어? 나도 그런데' 하고 자연스럽게 따라오게 하세요.\n"
        "- 구조가 보이면 안 됩니다. 자연스럽게 흘러가는 이야기처럼 쓰세요.\n"
        "- 과장하거나 단정 짓지 마세요. 담담하고 솔직하게.\n"
        "- AI가 쓴 티 나는 나열식 표현, 번호 매기기 금지.\n\n"
        "## 글 흐름 (이 순서를 따르되 티 나지 않게)\n"
        "1. 나의 상황 묘사로 시작 — 구체적인 장면, 시간, 감정 포함\n"
        "2. 나도 처음엔 잘못 알고 있었던 것 — 반전 포인트\n"
        "3. 알고 보니 진짜 원인 — 쉬운 말로 설명\n"
        "4. 내가 실제로 써보고 달라진 것 — 제품 유형 자연스럽게 등장\n"
        "5. 지금도 완벽하진 않지만 — 솔직한 마무리\n\n"
        "## 제목 규칙\n"
        "- 증상이나 상황을 담을 것\n"
        "- 날짜, 카테고리명 절대 포함 금지\n"
        "- 클릭하고 싶게, 하지만 낚시성 금지\n"
        "- 예: '허리가 망가지고 나서야 알게 된 것들'\n\n"
        "## 출력 형식\n"
        "제목: (제목)\n\n"
        "(본문 — 2500자 이상)\n\n"
        "## 쿠팡 추천 섹션 (글 맨 마지막에 반드시 포함)\n"
        "[COUPANG_START]\n"
        "(이 글의 내용과 자연스럽게 연결되는 제품 설명 1~2문장. 친근한 말투로.)\n"
        "[KEYWORDS: 검색키워드1, 검색키워드2]\n"
        "[COUPANG_END]\n\n"
        "키워드는 쿠팡에서 검색할 때 쓸 법한 구체적인 단어로 2개 작성.\n\n"
        "## 오늘의 주제\n"
        "증상/상황: " + symptom + "\n"
        "카테고리: " + category + "\n"
    )


# ============================================================
# 이미지 수집
# ============================================================
def fetch_unsplash(keyword):
    if not UNSPLASH_ACCESS_KEY:
        return []
    try:
        page = random.randint(1, 3)
        r = requests.get(
            "https://api.unsplash.com/search/photos",
            params={"query": keyword, "per_page": 5, "page": page, "orientation": "landscape"},
            headers={"Authorization": "Client-ID " + UNSPLASH_ACCESS_KEY},
            timeout=10
        )
        images = [p["urls"]["regular"] for p in r.json().get("results", [])]
        random.shuffle(images)
        return images
    except Exception as e:
        print("[Unsplash 오류] " + str(e))
        return []


def fetch_pexels(keyword):
    if not PEXELS_API_KEY:
        return []
    try:
        r = requests.get(
            "https://api.pexels.com/v1/search",
            params={"query": keyword, "per_page": 5, "orientation": "landscape"},
            headers={"Authorization": PEXELS_API_KEY},
            timeout=10
        )
        return [p["src"]["large"] for p in r.json().get("photos", [])]
    except Exception as e:
        print("[Pexels 오류] " + str(e))
        return []


def fetch_pixabay(keyword):
    if not PIXABAY_API_KEY:
        return []
    try:
        r = requests.get(
            "https://pixabay.com/api/",
            params={"key": PIXABAY_API_KEY, "q": keyword, "image_type": "photo",
                    "per_page": 5, "orientation": "horizontal"},
            timeout=10
        )
        return [h["largeImageURL"] for h in r.json().get("hits", [])]
    except Exception as e:
        print("[Pixabay 오류] " + str(e))
        return []


def get_images(keyword):
    images = fetch_unsplash(keyword)
    if not images:
        images = fetch_pexels(keyword)
    if not images:
        images = fetch_pixabay(keyword)
    return images


# ============================================================
# 쿠팡 박스 HTML
# ============================================================
def make_coupang_html(coupang_text):
    keyword_pattern = re.compile(r'\[KEYWORDS:\s*(.+?)\]', re.DOTALL)
    keyword_match = keyword_pattern.search(coupang_text)
    keywords = []
    if keyword_match:
        keywords = [k.strip() for k in keyword_match.group(1).split(',') if k.strip()]
        coupang_text = keyword_pattern.sub('', coupang_text).strip()

    keywords_html = ''
    if keywords:
        keywords_html += '<p style="font-size:14px;color:#e65100;font-weight:700;margin:0 0 16px 0;">🔎 추천 검색어 &nbsp;'
        for kw in keywords:
            keywords_html += (
                '<span style="display:inline-block;background:#fff3e0;'
'border:1.5px solid #f57f17;border-radius:20px;'
'padding:4px 14px;margin:0 6px 6px 0;font-size:14px;'
'color:#e65100;font-weight:700;">' + kw + '</span>'
            )
        keywords_html += '</p>'

    return (
        '<div style="background:#fff8e1;border:2px solid #f57f17;'
'border-radius:12px;padding:24px 28px;margin:48px 0 32px 0;">'
        '<p style="font-weight:700;font-size:17px;color:#e65100;margin:0 0 12px 0;">'
        '🛍️ 관련 상품 추천</p>'
        '<p style="font-size:15px;line-height:1.9;color:#333;margin:0 0 16px 0;">'
        + coupang_text.strip() +
        '</p>'
        + keywords_html +
        '<a href="' + COUPANG_LINK + '" target="_blank" rel="nofollow" '
        'style="display:inline-block;background:#f57f17;color:#fff;'
        'padding:12px 24px;border-radius:8px;text-decoration:none;'
        'font-weight:700;font-size:15px;">🔍 쿠팡에서 검색하기</a>'
        '<p style="font-size:11px;color:#aaa;margin:16px 0 0 0;line-height:1.6;">'
        '※ 이 링크를 통해 구매 시 소정의 수수료를 받을 수 있습니다. '
        '구매자에게는 추가 비용이 발생하지 않습니다.</p>'
        '</div>\n'
    )


# ============================================================
# 이미지 HTML
# ============================================================
def make_image_html(url, margin_top="32px"):
    return (
        '<div style="text-align:center;margin:' + margin_top + ' 0 28px 0;">'
        '<img src="' + url + '" alt="관련 이미지" '
        'style="max-width:100%;border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,0.10);"/>'
        '</div>\n'
    )


# ============================================================
# 본문 → HTML 변환
# ============================================================
def body_to_html(body, images):
    coupang_pattern = re.compile(r'\[COUPANG_START\](.*?)\[COUPANG_END\]', re.DOTALL)
    coupang_match = coupang_pattern.search(body)
    if coupang_match:
        coupang_html = make_coupang_html(coupang_match.group(1))
        body = coupang_pattern.sub('', body).strip()
    else:
        coupang_html = make_coupang_html(
            "오늘 소개해드린 내용과 관련된 제품을 쿠팡에서 검색해보세요. "
            "빠른 배송과 합리적인 가격으로 만나보실 수 있어요."
        )

    html = ""

    if images:
        html += make_image_html(images[0])

    paragraphs = [p.strip() for p in body.split('\n') if p.strip()]
    mid = len(paragraphs) // 2
    image2_inserted = False
    para_count = 0

    for i, para in enumerate(paragraphs):
        if para.startswith("## "):
            html += (
                '<h2 style="font-size:20px;font-weight:700;color:#1a1a2e;'
'border-left:4px solid #f57f17;padding-left:14px;'
'margin:36px 0 16px 0;">'
                + para[3:] + '</h2>\n'
            )
            continue

        if para.startswith("### "):
            html += (
                '<h3 style="font-size:18px;font-weight:600;color:#333;'
'margin:28px 0 12px 0;">'
                + para[4:] + '</h3>\n'
            )
            continue

        if para.startswith("---"):
            html += '<hr style="border:none;border-top:1px solid #eee;margin:32px 0;"/>\n'
            continue

        para_count += 1

        if para_count % 5 == 0 and len(para) > 40:
            html += (
                '<div style="border-left:4px solid #f57f17;padding:16px 20px;'
'margin:24px 0;background:#fff8f0;border-radius:0 8px 8px 0;">'
                '<p style="margin:0;font-size:16px;line-height:1.9;'
                'color:#1a1a2e;font-weight:500;">'
                + para + '</p></div>\n'
            )
        else:
            html += (
                '<p style="margin:16px 0;line-height:1.95;font-size:16px;color:#333;">'
                + para + '</p>\n'
            )

        if i >= mid and not image2_inserted and len(images) >= 2:
            html += make_image_html(images[1], margin_top="24px")
            image2_inserted = True

    if len(images) >= 3:
        html += make_image_html(images[2], margin_top="24px")

    html += coupang_html

    return html


# ============================================================
# 글 생성
# ============================================================
def generate_post(topic):
    prompt = build_prompt(topic)
    print("[Claude] 글 생성 중... 주제: " + topic["symptom"])
    raw = call_claude(prompt, max_tokens=5000)

    if not raw:
        print("[오류] 글 생성 실패")
        return None, None

    title = ""
    lines = raw.split("\n")
    body_lines = []
    for line in lines:
        if line.startswith("제목:"):
            title = line.replace("제목:", "").strip()
        else:
            body_lines.append(line)

    if not title:
        for line in body_lines[:5]:
            if len(line.strip()) > 10 and not line.startswith("["):
                title = line.strip()
                break

    if not title:
        title = topic["category"] + " 이야기 — 직접 겪고 나서 알게 된 것"

    body = "\n".join(body_lines).strip()
    images = get_images(topic["img_keyword"])
    html_body = body_to_html(body, images)
    return title, html_body


# ============================================================
# Google OAuth 토큰 갱신
# ============================================================
def get_access_token():
    try:
        r = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "refresh_token": GOOGLE_REFRESH_TOKEN3,
                "grant_type": "refresh_token",
            },
            timeout=15
        )
        return r.json().get("access_token", "")
    except Exception as e:
        print("[토큰 갱신 오류] " + str(e))
        return ""


# ============================================================
# Google Indexing API 색인 자동 요청
# ============================================================
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


# ============================================================
# Blogger 발행
# ============================================================
def publish_to_blogger(title, html_body, category):
    access_token = get_access_token()
    if not access_token:
        print("[Blogger] 토큰 없음 — 발행 실패")
        return ""

    url = "https://www.googleapis.com/blogger/v3/blogs/" + BLOGGER_BLOG_ID3 + "/posts/"
    payload = {
        "title": title,
        "content": html_body,
        "labels": [category],
    }
    try:
        r = requests.post(
            url,
            headers={"Authorization": "Bearer " + access_token,
                     "Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        r.raise_for_status()
        post_url = r.json().get("url", "")
        print("[Blogger] 발행 성공: " + post_url)
        return post_url
    except Exception as e:
        print("[Blogger 오류] " + str(e))
        return ""


# ============================================================
# 텔레그램 전송
# ============================================================
def send_telegram(title, post_url):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    message = "📝 새 포스팅 (블로그3)\n\n📌 " + title + "\n\n🔗 " + post_url
    try:
        requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
            timeout=10
        )
        print("[텔레그램] 전송 완료")
    except Exception as e:
        print("[텔레그램 오류] " + str(e))


# ============================================================
# 페이스북 공유
# ============================================================
def share_facebook(title, post_url):
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        return
    message = title + "\n\n자세한 내용은 아래 링크에서 확인하세요 👇\n" + post_url
    try:
        r = requests.post(
            "https://graph.facebook.com/" + FACEBOOK_PAGE_ID + "/feed",
            data={
                "message": message,
                "link": post_url,
                "access_token": FACEBOOK_ACCESS_TOKEN,
            },
            timeout=15
        )
        if r.status_code == 200:
            print("[페이스북] 공유 완료")
        else:
            print("[페이스북 오류] " + r.text)
    except Exception as e:
        print("[페이스북 오류] " + str(e))


# ============================================================
# 메인
# ============================================================
def main():
    print("=== 블로그3 자동 발행 시작 (" + TODAY + ") ===")

    topic = pick_topic()
    print("[선택된 주제] " + topic["symptom"] + " / " + topic["category"])

    title, html_body = generate_post(topic)
    if not title or not html_body:
        print("[오류] 글 생성 실패 — 종료")
        return

    print("[제목] " + title)

    post_url = publish_to_blogger(title, html_body, topic["category"])
    if post_url:
        save_used_topic(topic["symptom"])
        request_google_indexing(post_url)
        send_telegram(title, post_url)
        share_facebook(title, post_url)
        print("=== 완료 ===")
    else:
        print("[오류] 발행 실패")


if __name__ == "__main__":
    main()
