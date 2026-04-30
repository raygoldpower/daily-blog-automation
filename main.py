import os
import requests
import random
from datetime import datetime
import json
import re

# [원본 유지] API 설정 및 환경 변수
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

# [원본 유지] 주제 리스트 (길이 관계상 생략, 기존 데이터 그대로 사용하시면 됩니다)
TOPICS = [
    {"title": "드리블 속도 올리는 발목 가동성 훈련 3가지", "keyword": "soccer dribbling ankle mobility", "sport": "축구", "series": "드리블 마스터", "episode": 1},
    # ... 나머지 주제 리스트 유지
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

def generate_with_claude(prompt):
    # [원본 모델 유지]
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

    # [매거진 요구사항 반영 프롬프트]
    prompt = (
        "당신은 스포츠 과학 전문 매거진의 수석 에디터입니다.\n"
        "한국어만 사용하세요. 한자, 일본어 등 외국 문자 절대 금지.\n\n"
        + series_info
        + "매거진 레이아웃 지침:\n"
        "1. 제목: 독자의 궁금증을 유발하는 강력한 훅(Hook)을 제목에 자연스럽게 포함하세요.\n"
        "2. 첫 글: 독자가 겪는 상황에 깊이 공감하는 1~2줄의 짧고 강한 문장으로 시작하세요.\n"
        "3. 임팩트 키워드: 본문의 핵심 주제를 관통하는 단어 하나를 [KEYWORD]단어[/KEYWORD] 형식으로 크게 제시하세요.\n"
        "4. 키워드 설명: 해당 키워드가 왜 중요한지 보통 크기로 짧고 굵게 설명하세요.\n\n"
        "본문 집필 원칙 (원본 유지):\n"
        "독자가 글의 주인공입니다. 기초 설명에 그치지 말고 메커니즘과 원리까지 파고드세요.\n"
        "전문 용어는 반드시 괄호 안에 쉬운 설명을 추가하세요.\n"
        "연구 결과나 수치를 인용할 때는 출처와 함께 구체적으로 제시하세요.\n"
        "한 단락은 3~4줄 이내. 단락 사이 빈 줄 필수.\n"
        "[소제목1] 원리 설명, [소제목2] 심화 분석, [소제목3] 전문 근거 순으로 내용의 깊이를 점점 더하세요.\n"
        "2500자에서 3500자로 작성하세요.\n\n"
        "실전 및 마무리:\n"
        "훈련/실천 표: [TABLE_START]와 [TABLE_END] 사이에 '훈련명|세트|횟수|휴식|작용 근육|효과' 형식으로 작성하세요.\n"
        "운동 보완 설명: 각 운동별 핵심 팁을 짧게 덧붙이세요.\n"
        "결론 및 조언: 오늘 당장 할 수 있는 행동 하나를 강하고 간결하게 조언하며 끝내세요.\n"
        "핵심 요약: 반드시 [SUMMARY_START]로 시작하고 [SUMMARY_END]로 닫으세요.\n\n"
        "카테고리: " + topic["sport"] + "\n"
        "주제: " + topic["title"] + "\n\n"
        "출력 형식:\n"
        "제목: (제목)\n"
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
    return {"title": title, "body": body, "topic": topic}

def get_images(keyword, count=3):
    if not UNSPLASH_ACCESS_KEY:
        return []
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query": keyword, "per_page": count, "orientation": "landscape", "client_id": UNSPLASH_ACCESS_KEY
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
        return images
    except Exception:
        return []

def make_table_html(table_text):
    rows = [r.strip() for r in table_text.strip().split("\n") if r.strip()]
    if not rows: return ""
    html = '<div style="overflow-x:auto;margin:24px 0;"><table style="width:100%;border-collapse:collapse;font-size:15px;">'
    for i, row in enumerate(rows):
        cols = row.split("|")
        html += "<tr>"
        for col in cols:
            if i == 0:
                html += f'<th style="background:#1565c0;color:#fff;padding:10px 14px;text-align:center;border:1px solid #1565c0;">{col.strip()}</th>'
            else:
                bg = "#f5f8ff" if i % 2 == 0 else "#ffffff"
                html += f'<td style="padding:9px 14px;text-align:center;border:1px solid #dde3f0;background:{bg};">{col.strip()}</td>'
        html += "</tr>"
    html += "</table></div>"
    return html

def make_summary_html(summary_text):
    lines = [l.strip() for l in summary_text.strip().split("\n") if l.strip()]
    html = '<div style="background:#e8f4fd;border-left:5px solid #1565c0;border-radius:8px;padding:20px 24px;margin:28px 0;">'
    html += '<p style="font-weight:700;font-size:17px;color:#1565c0;margin-bottom:12px;">📌 핵심 요약</p>'
    for line in lines:
        html += f'<p style="margin:6px 0;font-size:15px;color:#333;">✅ {line}</p>'
    html += "</div>"
    return html

def make_image_html(img, margin_top="0"):
    return (
        f'<div style="text-align:center;margin:30px 0;margin-top:{margin_top};">'
        f'<img src="{img["url"]}" alt="{img["alt"]}" style="max-width:100%;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.12);"/>'
        f'<p style="font-size:12px;color:#999;margin-top:8px;">Photo by <a href="{img["author_url"]}">{img["author"]}</a> on Unsplash</p></div>'
    )

def body_to_html(body, images, topic):
    import re
    sport_emoji = SPORT_EMOJI.get(topic["sport"], "🏆")

    # 1. 임팩트 키워드 스타일링 (Blogger에서 깨지지 않도록 완전한 div 태그 사용)
    def style_keyword(match):
        word = match.group(1).strip()
        return (
            f'</div><div style="text-align:center; margin:50px 0;">'
            f'<p style="font-size:14px; color:#666; margin-bottom:10px;">Focus Keyword</p>'
            f'<span style="font-size:42px; font-weight:900; color:#1565c0; letter-spacing:-1px; border-bottom:6px solid #1565c0; padding-bottom:5px;">{word}</span>'
            f'</div><div style="margin:14px 0;">'
        )
    body = re.sub(r'\[KEYWORD\](.*?)\[/KEYWORD\]', style_keyword, body)

    # 2. 레이아웃 시작
    series_badge = ""
    if topic.get("series"):
        series_badge = (
            f'<div style="display:inline-block;background:#1565c0;color:#fff;font-size:13px;padding:5px 14px;border-radius:20px;margin-bottom:20px;font-weight:600;">'
            f'{sport_emoji} {topic["series"]} {topic["episode"]}편</div>'
        )

    # 전체 문서를 감싸는 컨테이너 시작
    html = f'<div style="font-family:sans-serif; line-height:1.9; color:#333; font-size:16px;">{series_badge}'

    if len(images) >= 1:
        html += make_image_html(images[0])

    # 3. 특수 요소 파싱 (표, 요약)
    table_pattern = re.compile(r'\[TABLE_START\](.*?)\[TABLE_END\]', re.DOTALL)
    summary_pattern = re.compile(r'\[SUMMARY_START\](.*?)\[SUMMARY_END\]', re.DOTALL)

    table_match = table_pattern.search(body)
    summary_match = summary_pattern.search(body)

    table_html = make_table_html(table_match.group(1)) if table_match else ""
    summary_html = make_summary_html(summary_match.group(1)) if summary_match else ""

    clean_body = table_pattern.sub("[TABLE_PLACEHOLDER]", body)
    clean_body = summary_pattern.sub("[SUMMARY_PLACEHOLDER]", clean_body)

    # 4. 문단별 렌더링
    paragraphs = clean_body.split("\n")
    mid = len(paragraphs) // 2
    image2_inserted = False
    para_count = 0

    for i, para in enumerate(paragraphs):
        text = para.strip()
        if not text: continue

        if text == "[TABLE_PLACEHOLDER]":
            html += table_html
        elif text == "[SUMMARY_PLACEHOLDER]":
            html += summary_html
        elif text.startswith("[") and "]" in text: # 소제목
            heading = text.strip("[]")
            html += (
                f'<h2 style="margin-top:48px; margin-bottom:16px; font-size:22px; font-weight:700; '
                f'background:linear-gradient(90deg,#1565c0,#1976d2); color:#fff; padding:12px 20px; border-radius:8px;">{heading}</h2>'
            )
        elif len(text) > 2 and text[0].isdigit() and text[1] in [".", ")"]: # 번호 리스트
            html += (
                f'<div style="display:flex; align-items:flex-start; margin:10px 0; padding:12px 16px; background:#f5f8ff; border-radius:8px;">'
                f'<span style="color:#1565c0; font-weight:700; margin-right:12px; font-size:16px;">{text[0]}.</span>'
                f'<span>{text[2:].strip()}</span></div>'
            )
        else: # 일반 단락
            para_count += 1
            if para_count % 4 == 0 and para_count > 1 and len(text) > 30:
                html += (
                    f'<div style="border-left:4px solid #1565c0; padding:14px 20px; margin:20px 0; background:#f0f4ff; border-radius:0 8px 8px 0;">'
                    f'<p style="margin:0; font-weight:500;">{text}</p></div>'
                )
            else:
                html += f'<p style="margin:14px 0;">{text}</p>'

        if i >= mid and not image2_inserted and len(images) >= 2:
            html += make_image_html(images[1], margin_top="20px")
            image2_inserted = True

    if len(images) >= 3:
        html += make_image_html(images[2], margin_top="20px")

    return html + "</div>"

def send_telegram(title, post_url, topic):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID: return
    msg = f"{SPORT_EMOJI.get(topic['sport'], '🏆')} 새 포스팅\n\n📌 {title}\n🔗 {post_url}"
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=10)
    except Exception: pass

def send_facebook(title, post_url, topic):
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN: return
    msg = f"{SPORT_EMOJI.get(topic['sport'], '🏆')} 새 포스팅\n\n{title}\n자세히 읽기 👉 {post_url}"
    try:
        requests.post(f"https://graph.facebook.com/v19.0/{FACEBOOK_PAGE_ID}/feed", data={"message": msg, "link": post_url, "access_token": FACEBOOK_ACCESS_TOKEN}, timeout=10)
    except Exception: pass

def post_to_blogger(post_data, images):
    try:
        access_token = get_access_token()
        body_html = body_to_html(post_data["body"], images, post_data["topic"])
        url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        payload = {
            "kind": "blogger#post",
            "title": post_data["title"],
            "content": body_html,
            "labels": [post_data["topic"]["sport"], post_data["topic"]["series"]],
            "status": "LIVE"
        }
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            post_url = response.json().get("url", "")
            print(f"\n발행 완료! 링크: {post_url}")
            send_telegram(post_data["title"], post_url, post_data["topic"])
            send_facebook(post_data["title"], post_url, post_data["topic"])
            return True
        else:
            print(f"발행 실패: {response.text}")
    except Exception as e:
        print(f"오류: {e}")
    return False

if __name__ == "__main__":
    print(f"AutoBlog 시작: {datetime.now()}")
    try:
        post = generate_post()
        images = get_images(post["topic"]["keyword"], count=3)
        post_to_blogger(post, images)
    except Exception as e:
        print(f"최종 오류: {e}")
