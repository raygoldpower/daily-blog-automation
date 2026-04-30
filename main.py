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
    "축구": "⚽",
    "농구": "🏀",
    "야구": "⚾",
    "공통": "🏆",
    "근육학": "💪",
    "재활": "🩺",
    "영양": "🥗",
    "심리": "🧠",
    "체력": "🔥",
    "유연성": "🤸"
}

TOPICS = [
    {"title": "당신의 드리블이 느린 진짜 이유", "keyword": "soccer dribbling technique", "sport": "축구", "series": "드리블 마스터", "episode": 1},
    {"title": "축구 스피드, 빠른 선수는 무엇이 다른가", "keyword": "soccer speed sprint", "sport": "축구", "series": "스피드 혁명", "episode": 1},
    {"title": "축구 슈팅력, 발이 아니라 몸통이 결정한다", "keyword": "soccer shooting power core", "sport": "축구", "series": "슈팅 마스터", "episode": 1},
    {"title": "90분을 뛰어도 지치지 않는 지구력 훈련", "keyword": "soccer endurance stamina", "sport": "축구", "series": "체력 마스터", "episode": 1},
    {"title": "농구 점프력, 타고나는 게 아니다", "keyword": "basketball jump vertical leap", "sport": "농구", "series": "점프력 혁명", "episode": 1},
    {"title": "농구 핸들링, 손이 아니라 뇌를 훈련하라", "keyword": "basketball ball handling", "sport": "농구", "series": "핸들링 마스터", "episode": 1},
    {"title": "농구 3점슛 성공률을 높이는 신체역학", "keyword": "basketball three point shooting biomechanics", "sport": "농구", "series": "슈팅 마스터", "episode": 1},
    {"title": "야구 타격 폼, 0.1초가 홈런을 결정한다", "keyword": "baseball batting swing speed", "sport": "야구", "series": "타격의 과학", "episode": 1},
    {"title": "투수의 어깨를 지키는 회전근개 강화법", "keyword": "baseball pitcher shoulder rotator cuff", "sport": "야구", "series": "투구의 과학", "episode": 1},
    {"title": "대퇴사두근(허벅지 앞 근육)을 제대로 키우는 법", "keyword": "quadriceps muscle training strength", "sport": "근육학", "series": "근육 해부학", "episode": 1},
    {"title": "햄스트링 부상을 예방하는 과학적 훈련법", "keyword": "hamstring injury prevention training", "sport": "근육학", "series": "근육 해부학", "episode": 2},
    {"title": "코어 근육의 모든 것, 복횡근부터 다열근까지", "keyword": "core muscles transverse abdominis multifidus", "sport": "근육학", "series": "코어 과학", "episode": 1},
    {"title": "어깨 근육 해부학, 삼각근과 회전근개의 역할", "keyword": "shoulder deltoid rotator cuff anatomy", "sport": "근육학", "series": "상체 해부학", "episode": 1},
    {"title": "종아리 근육(비복근, 가자미근)과 폭발적 스피드의 관계", "keyword": "calf muscle gastrocnemius soleus speed", "sport": "근육학", "series": "하체 해부학", "episode": 1},
    {"title": "근육 성장의 원리, 근비대를 유발하는 과학적 메커니즘", "keyword": "muscle hypertrophy growth mechanism", "sport": "근육학", "series": "근육 성장 과학", "episode": 1},
    {"title": "무릎 통증의 진짜 원인, 슬개건염부터 반월판 손상까지", "keyword": "knee pain patellar tendinitis meniscus", "sport": "재활", "series": "부상 재활", "episode": 1},
    {"title": "허리 통증을 없애는 요추 안정화 운동법", "keyword": "lower back pain lumbar stabilization", "sport": "재활", "series": "부상 재활", "episode": 2},
    {"title": "발목 염좌 후 완벽하게 회복하는 재활 프로그램", "keyword": "ankle sprain rehabilitation recovery", "sport": "재활", "series": "부상 재활", "episode": 3},
    {"title": "어깨 충돌 증후군, 올바른 재활과 예방법", "keyword": "shoulder impingement syndrome rehabilitation", "sport": "재활", "series": "부상 재활", "episode": 4},
    {"title": "운동 전후 단백질 섭취, 얼마나 언제 먹어야 하나", "keyword": "protein intake pre post workout timing", "sport": "영양", "series": "스포츠 영양학", "episode": 1},
    {"title": "탄수화물이 운동 퍼포먼스를 결정하는 이유", "keyword": "carbohydrates sports performance glycogen", "sport": "영양", "series": "스포츠 영양학", "episode": 2},
    {"title": "크레아틴, 과학이 증명한 가장 효과적인 보충제", "keyword": "creatine supplement muscle strength science", "sport": "영양", "series": "보충제 과학", "episode": 1},
    {"title": "수분 보충의 과학, 탈수가 운동 능력에 미치는 영향", "keyword": "hydration dehydration sports performance", "sport": "영양", "series": "스포츠 영양학", "episode": 3},
    {"title": "스포츠 루틴의 힘, 프로 선수들이 경기 전 반복하는 이유", "keyword": "sports pre game routine psychology", "sport": "심리", "series": "스포츠 심리학", "episode": 1},
    {"title": "압박 상황에서 최고의 퍼포먼스를 내는 멘탈 트레이닝", "keyword": "clutch performance mental training pressure", "sport": "심리", "series": "스포츠 심리학", "episode": 2},
    {"title": "슬럼프를 극복하는 스포츠 심리학적 접근법", "keyword": "slump recovery sports psychology", "sport": "심리", "series": "스포츠 심리학", "episode": 3},
    {"title": "VO2max란 무엇인가, 최대 산소 섭취량과 지구력의 관계", "keyword": "VO2max maximal oxygen uptake endurance", "sport": "체력", "series": "체력 과학", "episode": 1},
    {"title": "무산소 역치(젖산 역치)를 높이는 훈련법", "keyword": "lactate threshold anaerobic training", "sport": "체력", "series": "체력 과학", "episode": 2},
    {"title": "HIIT vs 저강도 유산소, 어떤 방법이 더 효과적인가", "keyword": "HIIT vs steady state cardio fat loss", "sport": "체력", "series": "유산소 과학", "episode": 1},
    {"title": "정적 스트레칭 vs 동적 스트레칭, 언제 무엇을 해야 하나", "keyword": "static dynamic stretching when to use", "sport": "유연성", "series": "유연성 과학", "episode": 1},
    {"title": "고관절 가동성이 스포츠 퍼포먼스를 결정한다", "keyword": "hip mobility sports performance", "sport": "유연성", "series": "가동성 혁명", "episode": 1},
    {"title": "폼롤러로 근막 이완하는 올바른 방법", "keyword": "foam roller myofascial release technique", "sport": "유연성", "series": "회복 과학", "episode": 1},
    {"title": "수면이 운동 회복과 근육 성장에 미치는 놀라운 영향", "keyword": "sleep recovery muscle growth hormones", "sport": "공통", "series": "회복 과학", "episode": 1},
    {"title": "과훈련 증후군(오버트레이닝)을 알아채는 방법과 대처법", "keyword": "overtraining syndrome symptoms recovery", "sport": "공통", "series": "회복 과학", "episode": 2},
    {"title": "아이의 스포츠 재능을 과학적으로 발견하고 키우는 방법", "keyword": "youth athletic development talent", "sport": "공통", "series": "스포츠 발달", "episode": 1},
    {"title": "나이가 들수록 꼭 해야 하는 기능성 운동의 모든 것", "keyword": "functional fitness aging sarcopenia", "sport": "공통", "series": "시니어 스포츠", "episode": 1},
    {"title": "체형 불균형이 부상의 원인이다, 체형 분석과 교정 운동", "keyword": "postural imbalance injury prevention correction", "sport": "공통", "series": "체형 교정", "episode": 1},
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
    # 최근 50개만 유지 (주제가 37개니까 충분)
    if len(used) > 50:
        used = used[-50:]
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
            + "이전 편의 내용을 자연스럽게 이어받아 더 심화된 내용을 다루세요.\n\n"
        )

    prompt = (
        "당신은 스포츠 과학, 운동역학, 해부학, 근육학, 스포츠 영양학, 스포츠 심리학을 깊이 이해하는 전문 블로거입니다.\n"
        "한자, 일본어, 중국어 등 한국어가 아닌 문자는 절대 사용하지 마세요.\n\n"
        + series_info
        + "가장 중요한 원칙: 독자가 글의 주인공입니다.\n"
        "글을 읽는 사람이 직접 변화하고 성장하는 느낌을 받아야 합니다.\n\n"
        "전문 용어 사용 원칙:\n"
        "근육 이름은 한글 명칭과 영문을 함께 표기하세요. 예: 대퇴사두근(Quadriceps), 햄스트링(Hamstrings)\n"
        "해부학 용어는 정확하게 사용하고 괄호 안에 쉬운 설명을 추가하세요.\n"
        "연구 결과 인용 시 구체적인 수치와 출처를 명시하세요. 예: 2022년 Journal of Strength에 따르면\n\n"
        "반드시 지켜야 할 원칙:\n"
        "반드시 존댓말을 사용하세요. 반말 금지.\n"
        "지침 내용을 절대 본문에 노출하지 마세요.\n"
        "한 단락은 3줄에서 4줄 이내로 끊어 쓰세요.\n"
        "단락 사이는 반드시 빈 줄을 넣으세요.\n"
        "소제목은 [소제목] 형식으로 표시하세요. 소제목 앞에 관련 이모지를 붙이세요.\n"
        "1500자에서 2500자로 작성하세요. 핵심만 간결하게 전달하세요.\n"
        "각 소제목 아래 최소 4개에서 5개 단락을 작성하세요.\n"
        "실천 목록은 최소 5가지 이상 구체적으로 제시하세요.\n"
        "각 훈련법의 효과, 작용 근육(정확한 해부학 명칭), 횟수, 주의사항까지 상세히 설명하세요.\n\n"
        "반드시 아래 요소들을 포함하세요:\n"
        "1. 훈련 프로그램 표: [TABLE_START]와 [TABLE_END] 사이에 작성하세요.\n"
        "형식: 훈련명|세트|횟수/시간|휴식|주요 작용 근육|효과\n"
        "[TABLE_START]\n"
        "훈련명|세트|횟수|휴식|주요 작용 근육|효과\n"
        "예시운동|3|12회|60초|대퇴사두근|하체 강화\n"
        "[TABLE_END]\n\n"
        "2. 핵심 포인트 요약: [SUMMARY_START]와 [SUMMARY_END] 사이에 3가지 핵심만 작성\n\n"
        "글의 흐름 - 기승전결로 점점 깊어지게:\n"
        "1. 독자가 공감하는 문제나 고민으로 시작하세요.\n"
        "2. 왜 그 문제가 생기는지 해부학, 생리학, 운동역학으로 과학적으로 설명하세요.\n"
        "3. 최신 연구 결과와 논문을 인용하듯 구체적 수치로 근거를 제시하세요.\n"
        "4. 독자가 당장 실천할 수 있는 구체적인 훈련 프로그램을 번호로 제시하세요.\n"
        "5. 영양, 회복, 멘탈 관리까지 포괄적으로 다루세요.\n"
        "6. 독자가 오늘 당장 변화를 시작하고 싶게 만드는 마무리로 끝내세요.\n\n"
        "카테고리: " + topic["sport"] + "\n"
        "주제: " + topic["title"] + "\n"
        "목표 분량: 1500자에서 2500자\n\n"
        "반드시 아래 형식으로 출력하세요:\n"
        "제목: (독자의 클릭을 유도하는 강렬한 제목)\n"
        "---\n"
        "(본문 내용)"
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
    html += '<p style="font-weight:700;font-size:17px;color:#1565c0;margin-bottom:12px;">📌 핵심 포인트 요약</p>'
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
        sport_emoji + " 새 포스팅 알림\n\n"
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
