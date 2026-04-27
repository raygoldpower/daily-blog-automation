import os
import requests
import random
from datetime import datetime

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
BLOG_ID = "4393162034375416055"

# [추가] 텔레그램 환경변수
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

TOPICS = [
    {"title": "당신의 드리블이 느린 진짜 이유", "keyword": "soccer dribbling speed technique", "sport": "축구", "series": "드리블 마스터", "episode": 1},
    {"title": "드리블 속도를 2배 높이는 발목 훈련법", "keyword": "soccer ankle dribbling training", "sport": "축구", "series": "드리블 마스터", "episode": 2},
    {"title": "메시가 수비수를 제치는 과학적 원리", "keyword": "soccer dribbling biomechanics agility", "sport": "축구", "series": "드리블 마스터", "episode": 3},
    {"title": "농구 점프력, 타고나는 게 아니다", "keyword": "basketball jump training vertical leap", "sport": "농구", "series": "점프력 혁명", "episode": 1},
    {"title": "당신의 점프력을 30% 높이는 8주 프로그램", "keyword": "basketball vertical jump program", "sport": "농구", "series": "점프력 혁명", "episode": 2},
    {"title": "야구 타격 폼, 0.1초가 홈런을 결정한다", "keyword": "baseball batting form swing speed", "sport": "야구", "series": "타격의 과학", "episode": 1},
    {"title": "배트 스피드를 높이는 상체 근력 훈련", "keyword": "baseball bat speed upper body strength", "sport": "야구", "series": "타격의 과학", "episode": 2},
    {"title": "축구 스피드, 빠른 선수는 무엇이 다른가", "keyword": "soccer speed sprint training", "sport": "축구", "series": "스피드 혁명", "episode": 1},
    {"title": "100미터를 1초 단축하는 가속 훈련법", "keyword": "sprint acceleration training technique", "sport": "공통", "series": "스피드 혁명", "episode": 2},
    {"title": "농구 핸들링, 손이 아니라 뇌를 훈련하라", "keyword": "basketball ball handling brain training", "sport": "농구", "series": "핸들링 마스터", "episode": 1},
    {"title": "수비수를 읽는 법, 스포츠 심리전의 모든 것", "keyword": "sports psychology reading opponent", "sport": "공통", "series": "심리전 전략", "episode": 1},
    {"title": "압박 상황에서 최고의 퍼포먼스를 내는 법", "keyword": "sports performance under pressure psychology", "sport": "공통", "series": "심리전 전략", "episode": 2},
    {"title": "팀 스포츠에서 나를 빛나게 하는 포지셔닝", "keyword": "team sports positioning strategy", "sport": "공통", "series": "전술 마스터", "episode": 1},
    {"title": "패스 하나로 경기를 바꾸는 시야 훈련법", "keyword": "soccer basketball passing vision training", "sport": "공통", "series": "전술 마스터", "episode": 2},
    {"title": "90분을 뛰어도 지치지 않는 지구력 훈련", "keyword": "soccer endurance stamina training", "sport": "축구", "series": "체력 마스터", "episode": 1},
    {"title": "스포츠 선수의 체력을 결정하는 VO2max의 비밀", "keyword": "VO2max endurance sports training", "sport": "공통", "series": "체력 마스터", "episode": 2},
    {"title": "민첩성 훈련, 방향 전환 속도를 높이는 과학", "keyword": "agility training change of direction speed", "sport": "공통", "series": "민첩성 혁명", "episode": 1},
    {"title": "팀워크가 개인 기량을 끌어올리는 원리", "keyword": "team chemistry individual performance sports", "sport": "공통", "series": "팀 시너지", "episode": 1},
    {"title": "축구 슈팅력, 발이 아니라 몸통이 결정한다", "keyword": "soccer shooting power core rotation", "sport": "축구", "series": "슈팅 마스터", "episode": 1},
    {"title": "농구 3점슛 성공률을 높이는 신체역학", "keyword": "basketball three point shooting biomechanics", "sport": "농구", "series": "슈팅 마스터", "episode": 1},
]

SPORT_EMOJI = {
    "축구": "⚽",
    "농구": "🏀",
    "야구": "⚾",
    "공통": "🏆"
}

# [추가] 텔레그램 발송 함수
def send_telegram_message(title, link):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[텔레그램] 설정값이 없어 전송을 건너뜁니다.")
        return
    message = f"📢 **[신규 포스팅 완료]**\n\n📌 **제목**: {title}\n\n🔗 **링크**: {link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("[텔레그램] 공유 성공!")
    except Exception as e:
        print(f"[텔레그램] 오류: {e}")

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
            "model": "claude-sonnet-4-20250514", # 원본 모델명 유지
            "max_tokens": 8000,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=300
    )
    if response.status_code != 200:
        raise Exception("Claude 오류: " + str(response.status_code) + " " + response.text[:200])
    return response.json()["content"][0]["text"]

def generate_post():
    topic = random.choice(TOPICS)
    print("[글 생성] 주제: " + topic["title"])

    series_info = ""
    if topic["episode"] > 1:
        series_info = (
            "이 글은 " + topic["series"] + " 시리즈 " + str(topic["episode"]) + "편입니다. "
            + "이전 편의 내용을 자연스럽게 이어받아 더 심화된 내용을 다루세요.\n\n"
        )

    prompt = (
        "당신은 스포츠 과학, 운동역학, 해부학, 스포츠 심리학을 깊이 이해하는 전문 스포츠 블로거입니다.\n"
        "한자, 일본어, 중국어 등 한국어가 아닌 문자는 절대 사용하지 마세요.\n\n"
        + series_info
        + "가장 중요한 원칙: 독자가 글의 주인공입니다.\n"
        "글을 읽는 사람이 직접 변화하고 성장하는 느낌을 받아야 합니다.\n\n"
        "반드시 지켜야 할 원칙:\n"
        "반드시 존댓말을 사용하세요. 반말 금지.\n"
        "지침 내용을 절대 본문에 노출하지 마세요.\n"
        "한 단락은 3줄에서 4줄 이내로 끊어 쓰세요.\n"
        "단락 사이는 반드시 빈 줄을 넣으세요.\n"
        "소제목은 [소제목] 형식으로 표시하세요. 소제목 앞에 관련 이모지를 붙이세요.\n"
        "예: [💪 핵심 근육 강화 훈련법], [🧠 심리적 준비 전략], [⚡ 스피드 향상 비결]\n"
        "4000자에서 6000자를 반드시 채워주세요. 절대 짧게 쓰지 마세요.\n"
        "각 소제목 아래 최소 4개에서 5개 단락을 작성하세요.\n"
        "실천 목록은 최소 5가지 이상 구체적으로 제시하세요.\n"
        "각 훈련법의 효과, 작용 근육, 횟수, 주의사항까지 상세히 설명하세요.\n\n"
        "반드시 아래 요소들을 포함하세요:\n"
        "1. 훈련 프로그램 표: [TABLE_START]와 [TABLE_END] 사이에 작성하세요.\n"
        "형식: 훈련명|세트|횟수|휴식|효과 (각 행을 새 줄로 구분)\n"
        "예:\n"
        "[TABLE_START]\n"
        "훈련명|세트|횟수|휴식|주요 효과\n"
        "스쿼트 점프|3|12회|60초|하체 폭발력 강화\n"
        "런지|3|10회|45초|균형감각 향상\n"
        "[TABLE_END]\n\n"
        "2. 핵심 포인트 요약: [SUMMARY_START]와 [SUMMARY_END] 사이에 3가지 핵심만 작성\n\n"
        "글의 흐름 - 기승전결로 점점 깊어지게:\n"
        "1. 독자가 공감하는 문제나 고민으로 시작하세요.\n"
        "2. 왜 그 문제가 생기는지 과학적으로 설명하세요. 해부학, 생리학 용어를 괄호로 설명하세요.\n"
        "3. 연구 결과와 논문을 인용하듯 깊이 있는 근거를 제시하세요.\n"
        "4. 독자가 당장 실천할 수 있는 구체적인 훈련 프로그램을 번호로 제시하세요.\n"
        "5. 영양, 회복, 멘탈 관리까지 포괄적으로 다루세요.\n"
        "6. 독자가 오늘 당장 변화를 시작하고 싶게 만드는 마무리로 끝내세요.\n\n"
        "종목: " + topic["sport"] + "\n"
        "주제: " + topic["title"] + "\n"
        "목표 분량: 4000자에서 6000자\n\n"
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

    # 이미지 1 - 상단
    if len(images) >= 1:
        html += make_image_html(images[0])

    # TABLE 파싱
    table_pattern = re.compile(r'\[TABLE_START\](.*?)\[TABLE_END\]', re.DOTALL)
    summary_pattern = re.compile(r'\[SUMMARY_START\](.*?)\[SUMMARY_END\]', re.DOTALL)

    table_match = table_pattern.search(body)
    summary_match = summary_pattern.search(body)

    table_html = make_table_html(table_match.group(1)) if table_match else ""
    summary_html = make_summary_html(summary_match.group(1)) if summary_match else ""

    # 특수 태그 제거
    clean_body = table_pattern.sub("[TABLE_PLACEHOLDER]", body)
    clean_body = summary_pattern.sub("[SUMMARY_PLACEHOLDER]", clean_body)

    paragraphs = clean_body.split("\n")
    total = len(paragraphs)
    mid = total // 2
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

        # 이미지 2 - 중간
        if i >= mid and not image2_inserted and len(images) >= 2:
            html += make_image_html(images[1], margin_top="20px")
            image2_inserted = True

    # 이미지 3 - 하단 (있으면)
    if len(images) >= 3:
        html += make_image_html(images[2], margin_top="20px")

    return html


def post_to_blogger(post_data, images):
    print("\n[Blogger] 포스팅 시작...")
    access_token = get_access_token()
    body_html = body_to_html(post_data["body"], images, post_data["topic"])
    url = "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts?isDraft=false"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    payload = {
        "kind": "blogger#post",
        "title": post_data["title"],
        "content": body_html,
        "status": "LIVE"
    }
    print("[제목] " + post_data["title"])
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print("[응답] 상태코드: " + str(response.status_code))
    if response.status_code == 200:
        result = response.json()
        post_url = result.get("url", "")
        print("\n발행 완료!")
        print("   링크: " + post_url)
        
        # [원본 로직 유지하며 텔레그램 연동 추가]
        send_telegram_message(post_data["title"], post_url)
        
        return True
    else:
        print("실패: " + response.text[:300])
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
