import requests
import base64
import os
import json
import re
import random

# [환경 변수] 깃허브 Secrets
API_KEY = os.environ.get("GEMINI_API_KEY")
WP_USER = os.environ.get("WP_USER")
WP_APP_PW = os.environ.get("WP_APP_PW")
WP_URL = os.environ.get("WP_URL").strip("/")

def run_premium_editor():
    print("🚀 [V3.0] 정식 API 엔진으로 교체하여 집필을 시작합니다...")

    # [1] 대표님의 핵심 주제
    topics = [
        "A deep analysis of a world-class athlete's mindset and humble character",
        "How global health trends are helping people find true balance",
        "The inspiring human story behind a legendary sports performance",
        "Celebrities who use their influence for positive global change",
        "Practical wellness tips: Merging modern science with humble living",
        "The impact of personality and character on physical excellence"
    ]
    selected_topic = random.choice(topics)
    print(f"📌 오늘의 선정 주제: {selected_topic}")

    # [2] 제미나이 작가 호출 (정식 v1 주소로 변경)
    gen_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    prompt = f"""
    Write a deeply helpful and intellectual English column (minimum 1,000 words) about: [{selected_topic}].

    [Style Guidelines]
    - Persona: Humble, friendly, and professional. 
    - Voice: Mix 1st person reflections ("I") with 3rd person analysis ("They").
    - Structure: Narrative story -> Intellectual analysis -> Q&A section -> Bullet-point summary.
    - Language: Easy Global English with sophisticated vocabulary for depth.
    - Safety: Strictly avoid any controversial or political issues.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7}
    }

    res = requests.post(gen_url, json=payload)
    res_data = res.json()

    # [🚨 정밀 진단] 만약 여기서도 에러가 나면 상세 내용을 출력합니다.
    if 'candidates' not in res_data:
        print("❌ AI 호출 실패. 서버 응답 내용:")
        print(json.dumps(res_data, indent=2, ensure_ascii=False))
        return

    full_text = res_data['candidates'][0]['content']['parts'][0]['text']
    content_parts = full_text.strip().split('\n', 1)
    title = re.sub('<[^<]+?>', '', content_parts[0]).strip()
    body = content_parts[1] if len(content_parts) > 1 else ""

    # [3] 워드프레스 전송
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PW}".encode()).decode()
    headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}
    
    img_url = "https://images.unsplash.com/photo-1490818387583-1baba5e638af?auto=format&fit=crop&q=80&w=1200"
    styled_content = f"""
    <div style="font-family: 'Georgia', serif; line-height: 2.1; color: #333; font-size: 17px; max-width: 800px; margin: auto;">
        <img src="{img_url}" style="width: 100%; border-radius: 15px; margin-bottom: 40px;">
        {body}
        <p style="text-align: center; color: #999; margin-top: 60px; font-style: italic;">
            "Small insights for a better, healthier world."
        </p>
    </div>
    """

    # 가장 안정적인 API 경로
    wp_api_url = f"{WP_URL}/index.php?rest_route=/wp/v2/posts"
    wp_res = requests.post(wp_api_url, headers=headers, json={
        'title': title, 'content': styled_content, 'status': 'publish'
    })

    if wp_res.status_code in [200, 201]:
        print(f"✅ 드디어 발행 성공! 제목: {title}")
    else:
        print(f"❌ 워드프레스 전송 에러: {wp_res.text}")

if __name__ == "__main__":
    run_premium_editor()
