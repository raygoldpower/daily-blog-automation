import os
import json
import requests
import random
from datetime import datetime

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
BLOG_ID = "4393162034375416055"

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

TOPICS = [
    {"title": "달리기 실력을 2배 높이는 보조 운동", "keyword": "running workout", "length": "long"},
    {"title": "무릎 통증, 원인과 해결법", "keyword": "knee pain exercise", "length": "long"},
    {"title": "100세 장수인들의 공통 생활 습관", "keyword": "healthy aging longevity", "length": "long"},
    {"title": "아이의 스포츠 재능을 키우는 방법", "keyword": "youth sports training", "length": "medium"},
    {"title": "허리 통증을 없애는 올바른 운동법", "keyword": "back pain exercise", "length": "long"},
    {"title": "근력 운동 vs 유산소 운동, 뭐가 더 효과적일까", "keyword": "strength cardio workout", "length": "medium"},
    {"title": "수면이 운동 효과에 미치는 놀라운 영향", "keyword": "sleep exercise recovery", "length": "medium"},
    {"title": "어깨 통증 완화를 위한 스트레칭 루틴", "keyword": "shoulder pain stretching", "length": "medium"},
    {"title": "체지방을 빠르게 태우는 과학적인 방법", "keyword": "fat burning exercise science", "length": "long"},
    {"title": "운동 전후 먹으면 좋은 음식 완벽 가이드", "keyword": "pre post workout nutrition", "length": "medium"},
    {"title": "나이가 들수록 꼭 해야 하는 운동 5가지", "keyword": "aging exercise health", "length": "medium"},
    {"title": "스트레칭만 잘해도 부상을 70% 줄일 수 있다", "keyword": "stretching injury prevention", "length": "long"},
    {"title": "멘탈이 운동 성과를 결정한다 — 스포츠 심리학", "keyword": "sports psychology mental training", "length": "long"},
    {"title": "걷기 운동, 제대로 하면 달리기보다 효과적이다", "keyword": "walking exercise health benefits", "length": "medium"},
    {"title": "당신의 자세가 통증의 원인이다 — 체형 교정법", "keyword": "posture correction exercise", "length": "long"},
]

WRITING_STYLE = """
당신은 10년 경력의 건강·운동 전문 블로거입니다.
독자에게 깊이 있는 정보를 따뜻하고 친절하게 전달하는 것이 목표입니다.

글쓰기 원칙:
1. 반드시 순수한 한국어만 사용하세요. 한자, 일본어, 중국어 절대 금지.
2. 전문 용어는 한글로 표기하고 괄호 안에 영어를 표기하세요. 예: 유산소 운동(Cardio)
3. 반드시 존댓말을 사용하세요. 반말 금지.
4. 첫 문장은 독자가 공감할 수 있는 질문이나 상황으로 시작하세요.
5. 과학적 근거나 연구 결과를 자연스럽게 포함하세요.
6. 한 단락은 반드시 3줄 이내로 짧게 끊어 쓰세요. 긴 단락 금지.
7. 단락과 단락 사이는 반드시 빈 줄 하나를 넣으세요.
8. 핵심 포인트는 번호 리스트로 정리하세요.
9. 소제목은 [소제목] 형식으로 표시하세요.
10. 글밥은 주제 깊이에 따라 자유롭게 조절하세요. medium: 1000~1500자, long: 1500~2500자
11. 마무리는 따뜻한 동기부여 문장으로 끝내세요.
12. 유튜브 영상 원고로도 자연스럽게 읽힐 수 있도록 작성하세요.
"""

def get_access_token():
    print("[인증] Google Access Token 발급 중...")
    url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": GOOGLE_REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=payload, timeout=10)
    if response.status_code != 200:
        raise Exception(f"토큰 발급 실패: {response.text}")
    print("[인증] 완료!")
    return response.json()["access_token"]

def generate_with_groq(prompt):
    print("[AI] Groq 사용 중...")
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 3000,
        "temperature": 0.8
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
    if response.status_code != 200:
        raise Exception(f"Groq 오류: {response.status_code}")
    return response.json()["choices"][0]["message"]["content"]

def generate_with_gemini(prompt):
    print("[AI] Gemini 사용 중...")
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.8, "maxOutputTokens": 3000}
    }
    response = requests.post(url, json=payload, timeout=30)
    if response.status_code != 200:
        raise Exception(f"Gemini 오류: {response.status_code} {response.text[:200]}")
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def generate_post():
    topic = random.choice(TOPICS)
    print(f"[글 생성] 주제: {topic['title']}")

    length_guide = {"medium": "1000~1500자", "long": "1500~2500자"}
    target_length = length_guide[topic["length"]]

    prompt = f"""{WRITING_STYLE}

주제: {topic['title']}
목표 분량: {target_length}

위 주제로 한국어 블로그 포스팅을 작성해주세요.
HTML 태그 없이 순수 텍스트로만 작성하세요.
소제목은 [소제목] 형식으로 표시하세요.

반드시 아래 형식으로 출력하세요:
제목: (클릭하고 싶은 제목)
---
(본문 내용)
"""

    try:
        full_text = generate_with_gemini(prompt)
    except Exception as e:
        print(f"[Gemini 실패] {e} → Groq으로 전환")
        full_text = generate_with_groq(prompt)

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

    print(f"[완료] 제목: {title}")
    print(f"[완료] 글자수: {len(body)}자")
    return {"title": title, "body": body, "topic": topic}

def get_images(keyword, count=2):
    if not UNSPLASH_ACCESS_KEY:
        return []
    try:
        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": keyword,
            "per_page": count,
            "orientation": "landscape",
            "client_id": UNSPLASH_ACCESS_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        images = []
        for photo in data.get("results", []):
            images.append({
                "url": photo["urls"]["regular"],
                "alt": photo.get("alt_description", keyword),
                "author": photo["user"]["name"],
                "author_url": photo["user"]["links"]["html"]
            })
        print(f"[이미지] {len(images)}장 수집 완료")
        return images
    except Exception as e:
        print(f"[이미지 오류] {e}")
        return []

def body_to_html(body, images):
    paragraphs = body.split("\n")
    html = ""
    total = len(paragraphs)
    mid = total // 2
    img_index = 0

    if images:
        img = images[0]
        html += f'''<div style="text-align:center;margin-bottom:30px;">
<img src="{img['url']}" alt="{img['alt']}" style="max-width:100%;border-radius:8px;"/>
<p style="font-size:12px;color:#888;margin-top:6px;">Photo by <a href="{img['author_url']}">{img['author']}</a> on Unsplash</p>
</div>\n'''
        img_index = 1

    for i, para in enumerate(paragraphs):
        if not para.strip():
            html += "<p style='margin:12px 0;'>&nbsp;</p>\n"
            continue
        if para.startswith("[") and "]" in para:
            heading = para.strip("[]").strip()
            html += f"<h2 style='margin-top:36px;margin-bottom:12px;font-size:22px;border-left:4px solid #4CAF50;padding-left:12px;'>{heading}</h2>\n"
        elif para.strip()[0] in "123456789" and para.strip()[1:3] in [") ", ". "]:
            html += f"<p style='margin:6px 0 6px 20px;line-height:1.9;'>{para}</p>\n"
        else:
            html += f"<p style='margin:10px 0;line-height:1.9;font-size:16px;'>{para}</p>\n"

        if i == mid and img_index < len(images):
            img = images[img_index]
            html += f'''<div style="text-align:center;margin:30px 0;">
<img src="{img['url']}" alt="{img['alt']}" style="max-width:100%;border-radius:8px;"/>
<p style="font-size:12px;color:#888;margin-top:6px;">Photo by <a href="{img['author_url']}">{img['author']}</a> on Unsplash</p>
</div>\n'''
            img_index += 1

    return html

def post_to_blogger(post_data, images):
    print(f"\n[Blogger] 포스팅 시작...")
    access_token = get_access_token()
    body_html = body_to_html(post_data["body"], images)

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "kind": "blogger#post",
        "title": post_data["title"],
        "content": body_html,
        "status": "LIVE",
    }

    print(f"[제목] {post_data['title']}")
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        params={"isDraft": "false"},
        timeout=30
    )
    print(f"[응답] 상태코드: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ 발행 완료!")
        print(f"   링크: {result.get('url', '')}")
        return True
    else:
        print(f"❌ 실패: {response.text[:300]}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print(f"AutoBlog Blogger Publisher")
    print(f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    try:
        post = generate_post()
        images = get_images(post["topic"]["keyword"], count=2)
        post_to_blogger(post, images)
        print(f"\n🎉 모든 작업 완료!")

    except Exception as e:
        print(f"\n💥 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
