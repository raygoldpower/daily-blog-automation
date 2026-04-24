import os
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
    {"title": "유산소와 근력운동, 둘 다 해야 하는 과학적 이유", "keyword": "cardio strength training", "length": "long"},
    {"title": "무릎 통증의 진짜 원인과 해결법", "keyword": "knee pain rehabilitation", "length": "long"},
    {"title": "100세 장수인들의 공통 생활 습관", "keyword": "longevity lifestyle", "length": "long"},
    {"title": "아이의 스포츠 재능, 어떻게 키울까", "keyword": "youth athletic development", "length": "medium"},
    {"title": "허리 통증을 없애는 올바른 운동법", "keyword": "lower back pain exercise", "length": "long"},
    {"title": "체지방을 빠르게 태우는 과학적 방법", "keyword": "fat burning metabolism", "length": "long"},
    {"title": "수면이 운동 효과를 결정한다", "keyword": "sleep athletic recovery", "length": "medium"},
    {"title": "어깨 통증, 회전근개부터 이해하자", "keyword": "shoulder rotator cuff exercise", "length": "long"},
    {"title": "달리기 실력을 높이는 보조 훈련법", "keyword": "running performance training", "length": "long"},
    {"title": "운동 전후 영양 전략 완벽 가이드", "keyword": "sports nutrition pre post workout", "length": "medium"},
    {"title": "나이가 들수록 꼭 해야 하는 기능성 운동", "keyword": "functional fitness aging", "length": "medium"},
    {"title": "스트레칭의 과학, 부상을 70% 줄이는 방법", "keyword": "stretching flexibility science", "length": "long"},
    {"title": "스포츠 심리학, 멘탈이 퍼포먼스를 결정한다", "keyword": "sports psychology performance", "length": "long"},
    {"title": "걷기 운동의 진짜 효과, 달리기와 비교", "keyword": "walking vs running health", "length": "medium"},
    {"title": "체형 불균형이 통증의 원인이다", "keyword": "posture imbalance pain correction", "length": "long"},
    {"title": "근육통의 원인과 빠른 회복 방법", "keyword": "muscle soreness DOMS recovery", "length": "medium"},
    {"title": "코어 근육의 모든 것, 왜 중요한가", "keyword": "core muscles stability training", "length": "long"},
    {"title": "단백질 섭취, 얼마나 어떻게 먹어야 하나", "keyword": "protein intake muscle building", "length": "medium"},
]

WRITING_STYLE = (
    "당신은 운동과학, 해부학, 생리학, 영양학을 깊이 이해하는 전문 건강 블로거입니다.\n\n"
    "반드시 지켜야 할 원칙:\n"
    "반드시 순수한 한국어만 사용하세요. 한자, 일본어, 중국어, 베트남어 등 외국어 절대 금지.\n"
    "반드시 존댓말을 사용하세요. 반말 금지.\n"
    "단계 번호나 지침 내용을 절대 본문에 노출하지 마세요. 자연스러운 글로만 작성하세요.\n"
    "한 단락은 3줄에서 4줄 이내로 끊어 쓰세요.\n"
    "단락 사이는 반드시 빈 줄을 넣으세요.\n"
    "소제목은 [소제목] 형식으로 표시하세요.\n"
    "medium 주제는 2500자에서 3500자, long 주제는 4000자에서 6000자로 작성하세요. 절대 짧게 쓰지 마세요.\n"
    "각 소제목 아래 최소 3개에서 5개 단락을 작성하세요.\n"
    "실천 목록은 최소 5가지 이상 제시하세요.\n"
    "각 운동이나 방법의 효과, 작용 근육, 주의사항까지 상세히 설명하세요.\n\n"
    "글의 흐름:\n"
    "첫째, 누구나 공감할 수 있는 일상적인 질문이나 상황으로 시작하세요. 독자가 공감하게 만드세요.\n"
    "둘째, 쉽고 친근한 언어로 기본 개념을 설명하세요. 전문 용어는 괄호 안에 한글 설명을 추가하세요. 예: 대퇴사두근(허벅지 앞쪽 근육)\n"
    "셋째, 해부학, 생리학, 운동역학 관점에서 깊이 있게 설명하세요. 연구 결과를 인용하듯 근거를 제시하세요.\n"
    "넷째, 구체적인 운동 목록을 번호로 정리하세요. 각 운동의 효과, 작용 근육, 세트 수, 횟수, 주의사항을 포함하세요.\n"
    "다섯째, 운동과 연계된 영양 정보를 포함하세요. 단백질, 탄수화물, 수분 섭취 등 구체적인 가이드를 제시하세요.\n"
    "마지막으로, 따뜻하고 동기부여가 되는 문장으로 끝내세요.\n"
)


def get_access_token():
    print("[인증] Google Access Token 발급 중...")
    response = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": GOOGLE_REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }, timeout=10)
    if response.status_code != 200:
        raise Exception("토큰 발급 실패: " + response.text)
    print("[인증] 완료!")
    return response.json()["access_token"]


def generate_with_gemini(prompt):
    print("[AI] Gemini 사용 중...")
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key=" + GEMINI_API_KEY
    response = requests.post(url, json={
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.85, "maxOutputTokens": 8000}
    }, timeout=120)
    if response.status_code != 200:
        raise Exception("Gemini 오류: " + str(response.status_code) + " " + response.text[:200])
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]


def generate_with_groq(prompt):
    print("[AI] Groq 사용 중...")
    response = requests.post(GROQ_API_URL, headers={
        "Authorization": "Bearer " + GROQ_API_KEY,
        "Content-Type": "application/json"
    }, json={
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 8000,
        "temperature": 0.85
    }, timeout=120)
    if response.status_code != 200:
        raise Exception("Groq 오류: " + str(response.status_code))
    return response.json()["choices"][0]["message"]["content"]


def generate_post():
    topic = random.choice(TOPICS)
    print("[글 생성] 주제: " + topic["title"])
    length_guide = {"medium": "2500자에서 3500자", "long": "4000자에서 6000자"}
    strict_rule = "경고: 한자, 일본어, 중국어, 베트남어, 태국어 등 한국어가 아닌 모든 문자는 절대 사용하지 마세요. 위반 시 글 전체가 무효입니다. 모든 단어는 반드시 한글 또는 영어 알파벳으로만 작성하세요.\n\n"

    prompt = (
        strict_rule +
        WRITING_STYLE + "\n\n"
        "주제: " + topic["title"] + "\n"
        "목표 분량: " + length_guide[topic["length"]] + "\n\n"
        "위 주제로 한국어 블로그 포스팅을 작성해주세요.\n"
        "HTML 태그 없이 순수 텍스트로만 작성하세요.\n"
        "소제목은 [소제목] 형식으로 표시하세요.\n"
        "기승전결 구조로 가벼운 질문에서 시작해 점점 전문적으로 깊어지는 방식으로 작성하세요.\n"
        "절대 짧게 끝내지 마세요. 목표 분량을 반드시 채워주세요.\n\n"
        "반드시 아래 형식으로 출력하세요:\n"
        "제목: (호기심을 자극하는 제목)\n"
        "---\n"
        "(본문 내용)\n"

    try:
        full_text = generate_with_gemini(prompt)
    except Exception as e:
        print("[Gemini 실패] " + str(e) + " → Groq으로 전환")
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

    print("[완료] 제목: " + title)
    print("[완료] 글자수: " + str(len(body)) + "자")
    return {"title": title, "body": body, "topic": topic}


def get_images(keyword, count=2):
    if not UNSPLASH_ACCESS_KEY:
        return []
    try:
        response = requests.get("https://api.unsplash.com/search/photos", params={
            "query": keyword,
            "per_page": count,
            "orientation": "landscape",
            "client_id": UNSPLASH_ACCESS_KEY
        }, timeout=10)
        images = []
        for photo in response.json().get("results", []):
            images.append({
                "url": photo["urls"]["regular"],
                "alt": photo.get("alt_description", keyword),
                "author": photo["user"]["name"],
                "author_url": photo["user"]["links"]["html"]
            })
        print("[이미지] " + str(len(images)) + "장 수집 완료")
        return images
    except Exception as e:
        print("[이미지 오류] " + str(e))
        return []


def body_to_html(body, images):
    paragraphs = body.split("\n")
    html = ""
    mid = len(paragraphs) // 2
    img_index = 0

    if images:
        img = images[0]
        html += '<div style="text-align:center;margin-bottom:30px;">'
        html += '<img src="' + img["url"] + '" alt="' + img["alt"] + '" style="max-width:100%;border-radius:8px;"/>'
        html += '<p style="font-size:12px;color:#888;margin-top:6px;">Photo by <a href="' + img["author_url"] + '">' + img["author"] + '</a> on Unsplash</p>'
        html += "</div>\n"
        img_index = 1

    for i, para in enumerate(paragraphs):
        if not para.strip():
            html += '<p style="margin:14px 0;">&nbsp;</p>\n'
            continue
        if para.startswith("[") and "]" in para:
            heading = para.strip("[]").strip()
            html += '<h2 style="margin-top:40px;margin-bottom:14px;font-size:22px;border-left:4px solid #2e7d32;padding-left:14px;color:#1a1a1a;">' + heading + "</h2>\n"
        elif len(para.strip()) > 1 and para.strip()[0].isdigit() and para.strip()[1] in [".", ")"]:
            html += '<p style="margin:8px 0 8px 24px;line-height:2.0;color:#333;">' + para + "</p>\n"
        else:
            html += '<p style="margin:12px 0;line-height:2.0;font-size:16px;color:#222;">' + para + "</p>\n"

        if i == mid and img_index < len(images):
            img = images[img_index]
            html += '<div style="text-align:center;margin:30px 0;">'
            html += '<img src="' + img["url"] + '" alt="' + img["alt"] + '" style="max-width:100%;border-radius:8px;"/>'
            html += '<p style="font-size:12px;color:#888;margin-top:6px;">Photo by <a href="' + img["author_url"] + '">' + img["author"] + '</a> on Unsplash</p>'
            html += "</div>\n"
            img_index += 1

    return html


def post_to_blogger(post_data, images):
    print("\n[Blogger] 포스팅 시작...")
    access_token = get_access_token()
    body_html = body_to_html(post_data["body"], images)
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
        print("\n✅ 발행 완료!")
        print("   링크: " + result.get("url", ""))
        return True
    else:
        print("❌ 실패: " + response.text[:300])
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("AutoBlog Blogger Publisher")
    print("실행 시각: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)
    try:
        post = generate_post()
        images = get_images(post["topic"]["keyword"], count=2)
        post_to_blogger(post, images)
        print("\n🎉 모든 작업 완료!")
    except Exception as e:
        print("\n💥 오류 발생: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
