import os
import requests
import json
from datetime import datetime

# ========================================
# 설정
# ========================================
BLOGGER_API_KEY = os.environ.get("BLOGGER_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

BLOG_ID = "4393162034375416055"

TOPICS = [
    "marketing trends",
    "AI and technology news",
    "startup and side business",
    "SNS operation tips",
    "investment and finance",
    "health and lifestyle",
]

# ========================================
# Groq으로 글 생성
# ========================================
def generate_post():
    import random
    topic = random.choice(TOPICS)
    print(f"[글 생성] 주제: {topic}")

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

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.8
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
    print(f"[Groq 응답] 상태코드: {response.status_code}")

    if response.status_code != 200:
        print(f"[오류] Groq API 실패: {response.text}")
        raise Exception(f"Groq API error: {response.status_code}")

    result = response.json()
    full_text = result["choices"][0]["message"]["content"]

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
# Blogger에 포스팅
# ========================================
def post_to_blogger(post_data):
    print(f"\n[Blogger] 포스팅 시작...")

    api_url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts"

    body_html = body_to_html(post_data["body"])

    payload = {
        "kind": "blogger#post",
        "title": post_data["title"],
        "content": body_html,
    }

    params = {
        "key": BLOGGER_API_KEY,
    }

    headers = {
        "Content-Type": "application/json",
    }

    print(f"[요청] POST {api_url}")
    print(f"[제목] {post_data['title']}")

    response = requests.post(
        api_url,
        params=params,
        headers=headers,
        json=payload,
        timeout=30
    )

    print(f"[응답] 상태코드: {response.status_code}")

    try:
        result = response.json()
        print(f"[응답 JSON] {json.dumps(result, ensure_ascii=False, indent=2)[:500]}")
    except:
        print(f"[응답 텍스트] {response.text[:300]}")

    if response.status_code == 200:
        result = response.json()
        post_id = result.get("id", "")
        post_url = result.get("url", "")
        print(f"\n✅ [성공] 발행 완료!")
        print(f"   ID: {post_id}")
        print(f"   링크: {post_url}")
        return True
    elif response.status_code == 401:
        print(f"❌ [실패] 인증 오류 — OAuth 토큰이 필요해요")
        print(f"   Blogger API는 API 키만으로는 글 작성이 안 되고 OAuth가 필요합니다")
        return False
    elif response.status_code == 403:
        print(f"❌ [실패] 권한 오류")
        print(f"   응답: {response.text[:200]}")
        return False
    else:
        print(f"❌ [실패] 오류: {response.status_code}")
        print(f"   응답: {response.text[:300]}")
        return False


# ========================================
# 메인 실행
# ========================================
if __name__ == "__main__":
    print("=" * 50)
    print(f"AutoBlog Blogger Publisher")
    print(f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    try:
        post = generate_post()
        success = post_to_blogger(post)

        if success:
            print(f"\n🎉 모든 작업 완료!")
        else:
            print(f"\n💥 발행 실패")
            exit(1)

    except Exception as e:
        print(f"\n💥 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
