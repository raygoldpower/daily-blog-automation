import os
import requests
import json
from datetime import datetime

# ========================================
# 설정
# ========================================
WP_URL = "https://min85power-gwtmy.wordpress.com"
WP_USER = "min85power@gmail.com"
WP_APP_PASSWORD = "jitr hp5j 3dv6 fx6f"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

TOPICS = [
    "marketing trends",
    "AI and technology news",
    "startup and side business",
    "SNS operation tips",
    "investment and finance",
    "health and lifestyle",
]

# ========================================
# Gemini로 글 생성
# ========================================
def generate_post():
    import random
    topic = random.choice(TOPICS)
    print(f"[글 생성] 주제: {topic}")

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    prompt = f"""You are a warm and informative blogger. Write a blog post about "{topic}".

Requirements:
- Length: minimum 1,000 characters
- Tone: friendly, informative, polite (like a knowledgeable friend)
- Start with an engaging question or relatable opening
- Include practical tips and real examples
- End with an encouraging closing message
- Use subheadings with [Subheading] format
- NO markdown formatting, plain text only

Output format:
Title: (write title here)
---
(write body here)
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 2000,
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload, timeout=30)

    print(f"[Gemini 응답] 상태코드: {response.status_code}")

    if response.status_code != 200:
        print(f"[오류] Gemini API 실패: {response.text}")
        raise Exception(f"Gemini API error: {response.status_code}")

    result = response.json()
    full_text = result["candidates"][0]["content"]["parts"][0]["text"]

    # 제목/본문 분리
    lines = full_text.strip().split("\n")
    title = ""
    body_lines = []
    separator_found = False

    for line in lines:
        if line.startswith("Title:"):
            title = line.replace("Title:", "").strip()
        elif line.strip() == "---":
            separator_found = True
        elif separator_found:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()

    if not title:
        title = f"{topic.title()} - Today's Insight"
    if not body:
        body = full_text

    print(f"[완료] 제목: {title}")
    print(f"[완료] 글자수: {len(body)}자")

    return {"title": title, "body": body, "topic": topic}


# ========================================
# 본문 HTML 변환
# ========================================
def body_to_html(body):
    html = ""
    for para in body.split("\n"):
        if not para.strip():
            html += "<p>&nbsp;</p>\n"
            continue
        if para.startswith("[") and "]" in para:
            heading = para.strip("[]").strip()
            html += f"<h2><strong>{heading}</strong></h2>\n"
        else:
            html += f"<p>{para}</p>\n"
    return html


# ========================================
# WordPress에 포스팅
# ========================================
def post_to_wordpress(post_data):
    print(f"\n[WordPress] 포스팅 시작...")

    api_url = f"{WP_URL}/wp-json/wp/v2/posts"
    auth = (WP_USER, WP_APP_PASSWORD)

    body_html = body_to_html(post_data["body"])

    payload = {
        "title": post_data["title"],
        "content": body_html,
        "status": "publish",  # 바로 공개 발행
        "categories": [],
        "tags": [],
        "format": "standard",
    }

    print(f"[요청] POST {api_url}")
    print(f"[제목] {post_data['title']}")

    response = requests.post(
        api_url,
        auth=auth,
        json=payload,
        timeout=30
    )

    print(f"[응답] 상태코드: {response.status_code}")

    # 응답 전체 출력 (디버깅용)
    try:
        result = response.json()
        print(f"[응답 JSON] {json.dumps(result, ensure_ascii=False, indent=2)[:500]}")
    except:
        print(f"[응답 텍스트] {response.text[:300]}")

    if response.status_code == 201:
        result = response.json()
        post_id = result.get("id", "")
        post_link = result.get("link", "")
        post_status = result.get("status", "")
        print(f"\n✅ [성공] 발행 완료!")
        print(f"   ID: {post_id}")
        print(f"   상태: {post_status}")
        print(f"   링크: {post_link}")
        return True
    elif response.status_code == 200:
        print(f"⚠️ [주의] 200 응답 — 발행됐을 수 있어요. 블로그 확인 필요")
        print(f"   링크: {WP_URL}")
        return True
    elif response.status_code == 401:
        print(f"❌ [실패] 인증 오류 — 애플리케이션 비밀번호를 확인해주세요")
        print(f"   응답: {response.text[:200]}")
        return False
    elif response.status_code == 403:
        print(f"❌ [실패] 권한 오류 — 계정 권한을 확인해주세요")
        print(f"   응답: {response.text[:200]}")
        return False
    else:
        print(f"❌ [실패] 예상치 못한 오류: {response.status_code}")
        print(f"   응답: {response.text[:300]}")
        return False


# ========================================
# 메인 실행
# ========================================
if __name__ == "__main__":
    print("=" * 50)
    print(f"AutoBlog WordPress Publisher")
    print(f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    try:
        # 1. 글 생성
        post = generate_post()

        # 2. WordPress 발행
        success = post_to_wordpress(post)

        if success:
            print(f"\n🎉 모든 작업 완료!")
            print(f"블로그: {WP_URL}")
        else:
            print(f"\n💥 발행 실패 — 위 로그를 확인해주세요")
            exit(1)

    except Exception as e:
        print(f"\n💥 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
