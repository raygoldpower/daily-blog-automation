import os
import requests
import random
from datetime import datetime
import json

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
FACEBOOK_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "")
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN", "")
BLOG_ID = "4393162034375416055"

SPORT_EMOJI = {
    "축구": "⚽", "농구": "🏀", "야구": "⚾", "공통": "🏆",
    "근육학": "💪", "재활": "🩺", "영양": "🥗", "심리": "🧠",
    "체력": "🔥", "유연성": "🤸", "생리학": "🫀", "물리치료": "🏥",
    "역학": "⚙️", "해부학": "🦴", "신체균형": "⚖️", "스포츠의학": "🩻",
}

TOPICS = [
    # 축구
    {"title": "드리블 속도 올리는 발목 가동성 훈련 3가지", "keyword": "soccer dribbling ankle mobility", "sport": "축구", "series": "드리블 마스터", "episode": 1},
    {"title": "축구 순간 스피드 높이는 가속 훈련법", "keyword": "soccer acceleration sprint training", "sport": "축구", "series": "스피드 혁명", "episode": 1},
    {"title": "축구 슈팅력을 높이는 고관절 회전 훈련", "keyword": "soccer shooting hip rotation power", "sport": "축구", "series": "슈팅 마스터", "episode": 1},
    {"title": "전반 90분 체력 유지하는 지구력 훈련 루틴", "keyword": "soccer endurance 90 minutes stamina", "sport": "축구", "series": "체력 마스터", "episode": 1},
    {"title": "축구 선수 무릎 부상 예방 스쿼트 변형 동작", "keyword": "soccer knee injury prevention squat", "sport": "축구", "series": "부상 예방", "episode": 1},
    # 농구
    {"title": "농구 점프력 높이는 플라이오메트릭 훈련 루틴", "keyword": "basketball jump plyometric training", "sport": "농구", "series": "점프력 혁명", "episode": 1},
    {"title": "농구 핸들링 실력 올리는 뇌 훈련법", "keyword": "basketball dribbling brain hand coordination", "sport": "농구", "series": "핸들링 마스터", "episode": 1},
    {"title": "3점슛 성공률 높이는 손목 스냅 훈련", "keyword": "basketball three point wrist snap shooting", "sport": "농구", "series": "슈팅 마스터", "episode": 1},
    # 야구
    {"title": "배트 스피드 높이는 하체 회전 훈련", "keyword": "baseball bat speed hip rotation", "sport": "야구", "series": "타격의 과학", "episode": 1},
    {"title": "투수 어깨 부상 막는 회전근개 강화 운동", "keyword": "baseball pitcher rotator cuff injury prevention", "sport": "야구", "series": "투구의 과학", "episode": 1},
    # 근육학
    {"title": "허벅지 앞 근육 키우는 스쿼트 변형 4가지", "keyword": "quadriceps squat variation muscle building", "sport": "근육학", "series": "근육 해부학", "episode": 1},
    {"title": "햄스트링 파열 막는 편심성 수축 훈련법", "keyword": "hamstring eccentric training injury prevention", "sport": "근육학", "series": "근육 해부학", "episode": 2},
    {"title": "복횡근 활성화로 허리 통증 잡는 방법", "keyword": "transverse abdominis core activation back pain", "sport": "근육학", "series": "코어 과학", "episode": 1},
    {"title": "삼각근 3개 부위 균형 있게 키우는 훈련", "keyword": "deltoid three heads shoulder training", "sport": "근육학", "series": "상체 해부학", "episode": 1},
    {"title": "종아리 근육 강화로 발목 부상 예방하기", "keyword": "calf muscle ankle stability injury prevention", "sport": "근육학", "series": "하체 해부학", "episode": 1},
    {"title": "근육 성장 원리, 단백질 합성을 극대화하는 자극법", "keyword": "muscle protein synthesis hypertrophy", "sport": "근육학", "series": "근육 성장 과학", "episode": 1},
    {"title": "전거근 약화가 어깨 통증을 만드는 이유", "keyword": "serratus anterior weakness shoulder pain", "sport": "근육학", "series": "상체 해부학", "episode": 2},
    {"title": "중둔근 강화로 무릎 통증과 골반 불균형 잡기", "keyword": "gluteus medius knee pain pelvic balance", "sport": "근육학", "series": "하체 해부학", "episode": 2},
    # 재활
    {"title": "무릎 연골 보호하는 슬개건염 재활 운동 순서", "keyword": "patellar tendinitis rehabilitation exercise", "sport": "재활", "series": "부상 재활", "episode": 1},
    {"title": "허리 디스크 통증 줄이는 요추 안정화 운동", "keyword": "lumbar disc stabilization exercise", "sport": "재활", "series": "부상 재활", "episode": 2},
    {"title": "발목 염좌 후 빠른 복귀를 위한 재활 단계", "keyword": "ankle sprain rehabilitation return to sport", "sport": "재활", "series": "부상 재활", "episode": 3},
    {"title": "어깨 충돌 증후군 재활, 병원 가기 전 할 수 있는 것", "keyword": "shoulder impingement home rehabilitation", "sport": "재활", "series": "부상 재활", "episode": 4},
    {"title": "아킬레스건 통증 있을 때 하면 안 되는 운동", "keyword": "achilles tendinopathy exercise avoid", "sport": "재활", "series": "부상 재활", "episode": 5},
    # 영양
    {"title": "운동 1시간 전 뭘 먹어야 할까, 탄수화물 타이밍", "keyword": "pre workout meal carbohydrate timing", "sport": "영양", "series": "스포츠 영양학", "episode": 1},
    {"title": "탄수화물이 운동 퍼포먼스를 결정하는 과학적 이유", "keyword": "carbohydrate glycogen sports performance", "sport": "영양", "series": "스포츠 영양학", "episode": 2},
    {"title": "크레아틴 복용법, 언제 얼마나 먹어야 효과적인가", "keyword": "creatine dosage timing supplement", "sport": "영양", "series": "보충제 과학", "episode": 1},
    {"title": "운동 중 수분 보충 타이밍과 양, 탈수 막는 방법", "keyword": "hydration during exercise timing amount", "sport": "영양", "series": "스포츠 영양학", "episode": 3},
    {"title": "단백질 하루 섭취량, 체중별 정확한 계산법", "keyword": "protein daily intake calculation body weight", "sport": "영양", "series": "스포츠 영양학", "episode": 4},
    {"title": "운동 후 회복 빠르게 하는 영양 조합 3가지", "keyword": "post workout recovery nutrition combination", "sport": "영양", "series": "스포츠 영양학", "episode": 5},
    # 심리
    {"title": "경기 전 긴장 푸는 루틴, 프로 선수들의 비밀", "keyword": "pre game routine anxiety control athletes", "sport": "심리", "series": "스포츠 심리학", "episode": 1},
    {"title": "압박 상황에서 집중력 유지하는 멘탈 훈련법", "keyword": "focus under pressure mental training sports", "sport": "심리", "series": "스포츠 심리학", "episode": 2},
    {"title": "운동 슬럼프 극복하는 심리학적 접근 3단계", "keyword": "sports slump recovery psychology steps", "sport": "심리", "series": "스포츠 심리학", "episode": 3},
    {"title": "이미지 트레이닝이 실제 운동 실력을 올리는 원리", "keyword": "mental imagery visualization sports performance", "sport": "심리", "series": "스포츠 심리학", "episode": 4},
    # 체력
    {"title": "VO2max 높이는 인터벌 훈련 방법과 강도 설정", "keyword": "VO2max interval training intensity", "sport": "체력", "series": "체력 과학", "episode": 1},
    {"title": "젖산 역치 높이는 훈련으로 지구력 올리기", "keyword": "lactate threshold training endurance", "sport": "체력", "series": "체력 과학", "episode": 2},
    {"title": "HIIT 운동 효과 극대화하는 휴식 시간 설정법", "keyword": "HIIT rest interval optimization fat loss", "sport": "체력", "series": "유산소 과학", "episode": 1},
    {"title": "심박수 구간별 운동 강도 설정하는 방법", "keyword": "heart rate zone exercise intensity training", "sport": "체력", "series": "체력 과학", "episode": 3},
    # 유연성
    {"title": "운동 전 동적 스트레칭 루틴, 부상 예방 효과", "keyword": "dynamic stretching warm up injury prevention", "sport": "유연성", "series": "유연성 과학", "episode": 1},
    {"title": "고관절 유연성 높이는 스트레칭 5가지", "keyword": "hip flexor mobility stretching exercises", "sport": "유연성", "series": "가동성 혁명", "episode": 1},
    {"title": "폼롤러로 근막 이완하는 올바른 방법과 주의사항", "keyword": "foam rolling myofascial release technique", "sport": "유연성", "series": "회복 과학", "episode": 1},
    {"title": "흉추 가동성 높이면 어깨 통증이 사라지는 이유", "keyword": "thoracic spine mobility shoulder pain", "sport": "유연성", "series": "가동성 혁명", "episode": 2},
    # 생리학
    {"title": "운동할 때 근육에서 실제로 일어나는 일", "keyword": "muscle physiology exercise ATP energy", "sport": "생리학", "series": "운동 생리학", "episode": 1},
    {"title": "유산소 운동 중 지방이 타는 정확한 원리", "keyword": "fat oxidation aerobic exercise physiology", "sport": "생리학", "series": "운동 생리학", "episode": 2},
    {"title": "수면 중 성장호르몬이 근육을 키우는 메커니즘", "keyword": "growth hormone sleep muscle recovery", "sport": "생리학", "series": "운동 생리학", "episode": 3},
    {"title": "운동 후 통증(DOMS)이 생기는 진짜 이유와 해결법", "keyword": "DOMS delayed onset muscle soreness cause", "sport": "생리학", "series": "운동 생리학", "episode": 4},
    {"title": "심장이 운동에 적응하는 방식, 운동성 심비대", "keyword": "cardiac adaptation exercise athlete heart", "sport": "생리학", "series": "운동 생리학", "episode": 5},
    {"title": "코르티솔이 높으면 근육이 빠지는 이유", "keyword": "cortisol muscle loss stress hormone", "sport": "생리학", "series": "운동 생리학", "episode": 6},
    # 물리치료
    {"title": "어깨 통증 있을 때 물리치료사가 먼저 확인하는 것", "keyword": "shoulder pain physical therapy assessment", "sport": "물리치료", "series": "물리치료 가이드", "episode": 1},
    {"title": "무릎 통증 자가 진단, 병원 가야 할 신호", "keyword": "knee pain self diagnosis when to see doctor", "sport": "물리치료", "series": "물리치료 가이드", "episode": 2},
    {"title": "테니스 엘보 치료, 집에서 할 수 있는 운동", "keyword": "tennis elbow treatment home exercise", "sport": "물리치료", "series": "물리치료 가이드", "episode": 3},
    {"title": "족저근막염 아침 통증 줄이는 스트레칭 루틴", "keyword": "plantar fasciitis morning stretching routine", "sport": "물리치료", "series": "물리치료 가이드", "episode": 4},
    {"title": "거북목 교정 운동, 하루 5분으로 효과 보기", "keyword": "forward head posture correction exercise", "sport": "물리치료", "series": "물리치료 가이드", "episode": 5},
    # 역학 (스포츠 역학)
    {"title": "달리기 자세 분석, 무릎에 가해지는 충격 줄이기", "keyword": "running biomechanics knee impact reduction", "sport": "역학", "series": "스포츠 역학", "episode": 1},
    {"title": "스쿼트할 때 무릎이 안쪽으로 무너지는 원인", "keyword": "squat knee valgus cause biomechanics", "sport": "역학", "series": "스포츠 역학", "episode": 2},
    {"title": "데드리프트 허리 부상 막는 척추 중립 자세", "keyword": "deadlift spine neutral position injury prevention", "sport": "역학", "series": "스포츠 역학", "episode": 3},
    {"title": "점프 착지 자세가 전방십자인대 부상을 결정한다", "keyword": "landing mechanics ACL injury prevention", "sport": "역학", "series": "스포츠 역학", "episode": 4},
    # 해부학
    {"title": "무릎 관절 구조, 왜 이렇게 자주 다칠까", "keyword": "knee joint anatomy structure injury", "sport": "해부학", "series": "스포츠 해부학", "episode": 1},
    {"title": "어깨 관절 360도 움직임이 가능한 이유와 약점", "keyword": "shoulder joint anatomy mobility instability", "sport": "해부학", "series": "스포츠 해부학", "episode": 2},
    {"title": "발의 아치 구조가 달리기에 미치는 영향", "keyword": "foot arch structure running performance", "sport": "해부학", "series": "스포츠 해부학", "episode": 3},
    {"title": "척추 디스크 구조와 압력이 가해지는 자세", "keyword": "spinal disc anatomy pressure posture", "sport": "해부학", "series": "스포츠 해부학", "episode": 4},
    # 신체균형
    {"title": "골반 틀어짐이 허리·무릎 통증을 만드는 연결고리", "keyword": "pelvic tilt imbalance lower back knee pain", "sport": "신체균형", "series": "체형 교정", "episode": 1},
    {"title": "한쪽 어깨가 낮은 이유, 척추측만증 자가 체크법", "keyword": "shoulder uneven scoliosis self check", "sport": "신체균형", "series": "체형 교정", "episode": 2},
    {"title": "평발이 운동 능력에 미치는 영향과 교정 방법", "keyword": "flat feet sports performance correction", "sport": "신체균형", "series": "체형 교정", "episode": 3},
    {"title": "X자 다리 교정 운동, 중둔근부터 강화해야 하는 이유", "keyword": "knock knees correction gluteus medius", "sport": "신체균형", "series": "체형 교정", "episode": 4},
    # 스포츠의학
    {"title": "성장판 손상 없이 청소년이 안전하게 운동하는 방법", "keyword": "youth athlete growth plate safe training", "sport": "스포츠의학", "series": "스포츠의학 가이드", "episode": 1},
    {"title": "열사병 위험 신호, 여름 운동 시 주의사항", "keyword": "heat stroke warning signs summer exercise", "sport": "스포츠의학", "series": "스포츠의학 가이드", "episode": 2},
    {"title": "운동 중 갑자기 쥐가 나는 이유와 예방법", "keyword": "exercise cramp cause prevention electrolyte", "sport": "스포츠의학", "series": "스포츠의학 가이드", "episode": 3},
    {"title": "과훈련 증후군 자가 체크, 지금 쉬어야 할 신호", "keyword": "overtraining syndrome self check recovery", "sport": "스포츠의학", "series": "스포츠의학 가이드", "episode": 4},
    # 공통
    {"title": "수면 7시간이 근육 성장과 체력에 미치는 영향", "keyword": "sleep 7 hours muscle growth performance", "sport": "공통", "series": "회복 과학", "episode": 1},
    {"title": "나이 들수록 근육이 빠지는 이유와 막는 방법", "keyword": "sarcopenia aging muscle loss prevention", "sport": "공통", "series": "시니어 스포츠", "episode": 1},
    {"title": "아이 운동 시작 나이, 종목별 적합한 시기", "keyword": "youth sports age appropriate training", "sport": "공통", "series": "스포츠 발달", "episode": 1},
    {"title": "운동 초보자가 첫 달에 반드시 지켜야 할 원칙", "keyword": "beginner exercise first month principles", "sport": "공통", "series": "운동 입문", "episode": 1},
    {"title": "체중 감량과 근육 증가를 동시에 하는 방법", "keyword": "body recomposition fat loss muscle gain", "sport": "공통", "series": "운동 입문", "episode": 2},
]

USED_TOPICS_FILE = "used_topics.json"


def load_used_topics():
    try:
        with open(USED_TOPICS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_used_topic(title):
    used = load_used_topics()
    used.append(title)
    if len(used) > 80:
        used = used[-80:]
    try:
        with open(USED_TOPICS_FILE, "w") as f:
            json.dump(used, f, ensure_ascii=False)
    except Exception as e:
        print("[중복방지] 저장 실패: " + str(e))


def pick_topic():
    used = load_used_topics()
    available = [t for t in TOPICS if t["title"] not in used]
    if not available:
        print("[중복방지] 모든 주제 사용 완료, 초기화합니다.")
        available = TOPICS
        try:
            with open(USED_TOPICS_FILE, "w") as f:
                json.dump([], f)
        except Exception:
            pass
    topic = random.choice(available)
    save_used_topic(topic["title"])
    return topic


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


def generate_with_claude(prompt):
    print("[AI] Claude 사용 중...")
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=300
    )
    if response.status_code != 200:
        raise Exception("Claude 오류: " + str(response.status_code) + " " + response.text[:200])
    return response.json()["content"][0]["text"]


def generate_post():
    topic = pick_topic()
    print("[글 생성] 주제: " + topic["title"])

    series_info = ""
    if topic["episode"] > 1:
        series_info = (
            "이 글은 " + topic["series"] + " 시리즈 " + str(topic["episode"]) + "편입니다. "
            + "이전 편보다 심화된 내용을 다루세요.\n\n"
        )

    prompt = (
        "당신은 스포츠 과학, 운동역학, 해부학, 근육학, 생리학, 물리치료학, 스포츠의학을 깊이 이해하는 전문 블로거입니다.\n"
        "한국어만 사용하세요. 한자, 일본어 등 외국 문자 절대 금지.\n\n"
        + series_info
        + "핵심 원칙:\n"
        "독자가 글의 주인공입니다. 독자가 직접 변화하고 성장하는 느낌을 줘야 합니다.\n"
        "전문 블로그답게 깊이 있게 쓰세요. 기초 설명에 그치지 말고 메커니즘과 원리까지 파고드세요.\n"
        "전문 용어는 반드시 괄호 안에 쉬운 설명을 추가하세요. 예: 대퇴사두근(허벅지 앞 근육)\n"
        "연구 결과나 수치를 인용할 때는 출처와 함께 구체적으로 제시하세요.\n"
        "한 단락은 3~4줄 이내. 단락 사이 빈 줄 필수.\n"
        "소제목은 [소제목] 형식, 앞에 이모지 붙이세요.\n"
        "2500자에서 3500자로 작성하세요. 깊이 있는 내용을 충분히 전달하세요.\n"
        "첫 문장은 독자가 겪는 구체적 상황을 직접 묘사하세요. 질문형 금지.\n"
        "마무리는 오늘 당장 할 수 있는 행동 한 가지로 끝내세요. 격언 금지.\n"
        "AI가 쓴 티 나는 나열식 표현 금지. 자연스럽게 쓰세요.\n\n"
        "글의 깊이 기준:\n"
        "단순 방법 나열이 아니라 왜 그 방법이 효과적인지 생리학/해부학/역학적으로 설명하세요.\n"
        "독자가 읽고 나서 '이런 원리였구나'라고 느끼게 만드세요.\n"
        "실제 현장에서 쓰이는 전문적인 내용을 포함하세요.\n\n"
        "포함할 요소:\n"
        "훈련/실천 표: [TABLE_START]와 [TABLE_END] 사이에 작성\n"
        "형식: 훈련명|세트|횟수|휴식|작용 근육|효과\n"
        "[TABLE_START]\n"
        "훈련명|세트|횟수|휴식|작용 근육|효과\n"
        "예시|3|12회|60초|대퇴사두근|하체 강화\n"
        "[TABLE_END]\n\n"
        "핵심 요약: [SUMMARY_START]와 [SUMMARY_END] 사이에 3줄로 핵심만\n\n"
        "글 흐름:\n"
        "1. 독자가 겪는 구체적 상황 묘사로 시작\n"
        "2. 왜 그 문제가 생기는지 생리학/해부학/역학으로 깊이 설명\n"
        "3. 최신 연구 결과를 근거로 제시\n"
        "4. 실천법을 원리와 함께 구체적으로 제시\n"
        "5. 오늘 당장 할 수 있는 행동 하나로 마무리\n\n"
        "카테고리: " + topic["sport"] + "\n"
        "주제: " + topic["title"] + "\n"
        "SEO 핵심 키워드를 제목에 자연스럽게 포함하세요.\n\n"
        "출력 형식:\n"
        "제목: (검색에 잘 걸리는 구체적인 제목)\n"
        "---\n"
        "(본문)"
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
        title = topic["title"]
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
        data = response.json()
        images = []
        for photo in data.get("results", []):
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


def make_table_html(table_text):
    rows = [r.strip() for r in table_text.strip().split("\n") if r.strip()]
    if not rows:
        return ""
    html = '<div style="overflow-x:auto;margin:24px 0;">'
    html += '<table style="width:100%;border-collapse:collapse;font-size:15px;">'
    for i, row in enumerate(rows):
        cols = row.split("|")
        html += "<tr>"
        for col in cols:
            if i == 0:
                html += '<th style="background:#1565c0;color:#fff;padding:10px 14px;text-align:center;border:1px solid #1565c0;">' + col.strip() + "</th>"
            else:
                bg = "#f5f8ff" if i % 2 == 0 else "#ffffff"
                html += '<td style="padding:9px 14px;text-align:center;border:1px solid #dde3f0;background:' + bg + ';">' + col.strip() + "</td>"
        html += "</tr>"
    html += "</table></div>\n"
    return html


def make_summary_html(summary_text):
    lines = [l.strip() for l in summary_text.strip().split("\n") if l.strip()]
    html = '<div style="background:#e8f4fd;border-left:5px solid #1565c0;border-radius:8px;padding:20px 24px;margin:28px 0;">'
    html += '<p style="font-weight:700;font-size:17px;color:#1565c0;margin-bottom:12px;">📌 핵심 요약</p>'
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

    sport_emoji = SPORT_EMOJI.get(topic["sport"], "🏆")
    series_badge = ""
    if topic.get("series"):
        series_badge = (
            '<div style="display:inline-block;background:#1565c0;color:#fff;'
            'font-size:13px;padding:4px 12px;border-radius:20px;margin-bottom:16px;">'
            + sport_emoji + " " + topic["series"] + " " + str(topic["episode"]) + "편</div>\n"
        )

    html = series_badge

    if len(images) >= 1:
        html += make_image_html(images[0])

    table_pattern = re.compile(r'\[TABLE_START\](.*?)\[TABLE_END\]', re.DOTALL)
    summary_pattern = re.compile(r'\[SUMMARY_START\](.*?)\[SUMMARY_END\]', re.DOTALL)

    table_match = table_pattern.search(body)
    summary_match = summary_pattern.search(body)

    table_html = make_table_html(table_match.group(1)) if table_match else ""
    summary_html = make_summary_html(summary_match.group(1)) if summary_match else ""

    clean_body = table_pattern.sub("[TABLE_PLACEHOLDER]", body)
    clean_body = summary_pattern.sub("[SUMMARY_PLACEHOLDER]", clean_body)

    paragraphs = clean_body.split("\n")
    mid = len(paragraphs) // 2
    image2_inserted = False

    for i, para in enumerate(paragraphs):
        if not para.strip():
            html += '<p style="margin:14px 0;">&nbsp;</p>\n'
            continue
        if para.strip() == "[TABLE_PLACEHOLDER]":
            html += table_html
            continue
        if para.strip() == "[SUMMARY_PLACEHOLDER]":
            html += summary_html
            continue
        if para.startswith("[") and "]" in para:
            heading = para.strip("[]").strip()
            html += '<h2 style="margin-top:40px;margin-bottom:14px;font-size:22px;border-left:4px solid #1565c0;padding-left:14px;color:#1a1a1a;">' + heading + "</h2>\n"
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
    sport_emoji = SPORT_EMOJI.get(topic["sport"], "🏆")
    message = (
        sport_emoji + " 새 포스팅\n\n"
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
    sport_emoji = SPORT_EMOJI.get(topic["sport"], "🏆")
    message = (
        sport_emoji + " 새 포스팅\n\n"
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


def post_to_blogger(post_data, images, retry=2):
    print("\n[Blogger] 포스팅 시작...")
    topic = post_data["topic"]
    labels = [topic["sport"], topic["series"]]

    for attempt in range(1, retry + 2):
        try:
            access_token = get_access_token()
            body_html = body_to_html(post_data["body"], images, topic)
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
            print("[시도 " + str(attempt) + "] 제목: " + post_data["title"])
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            print("[응답] 상태코드: " + str(response.status_code))
            if response.status_code == 200:
                result = response.json()
                post_url = result.get("url", "")
                print("\n발행 완료!")
                print("   링크: " + post_url)
                send_telegram(post_data["title"], post_url, topic)
                send_facebook(post_data["title"], post_url, topic)
                return True
            else:
                print("실패: " + response.text[:300])
                if attempt <= retry:
                    print("[재시도] " + str(attempt) + "번째 재시도 중...")
        except Exception as e:
            print("[오류] " + str(e))
            if attempt <= retry:
                print("[재시도] " + str(attempt) + "번째 재시도 중...")
    return False


if __name__ == "__main__":
    print("=" * 50)
    print("AutoBlog Sports Publisher - Claude Edition")
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
