import requests
import base64
import os
import json
import re
import random

# [설정] 깃허브 Secrets에서 안전하게 정보를 가져옵니다.
API_KEY = os.environ.get("GEMINI_API_KEY")
WP_USER = os.environ.get("WP_USER")
WP_APP_PW = os.environ.get("WP_APP_PW")
WP_URL = os.environ.get("WP_URL").strip("/")

def run_premium_automation():
    print("🚀 다정하고 지적인 글로벌 에디터 엔진을 가동합니다...")

    # [1] 대표님이 선정한 6대 핵심 주제
    topics = [
        "A deep look into a sports star's unique talent and humble personality",
        "How global health trends are helping people live more meaningful lives",
        "The inspiring human story behind a world-class athlete's success",
        "Analyzing the traits of celebrities who make a positive impact on society",
        "Wellness and longevity: Practical tips from global health experts",
        "The intersection of human character and physical excellence in sports"
    ]
    selected_topic = random.choice(topics)
    print(f"📌 오늘의 주제: {selected_topic}")

    # [2] 제미나이 작가 호출 (v1beta 주소로 안정성 강화)
    gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    # 1,000자 이상의 고품격 글을 위한 정교한 지시사항
    prompt = f"""
    Write a deeply helpful and insightful English column (minimum 1,000 words) about: [{selected_topic}].

    [Persona & Tone]
    - Be a humble, kind, and intelligent storyteller. Your goal is to provide 'help' and 'information'.
    - Mix 1st person ("I believe", "I observed") and 3rd person ("Experts say", "The data shows") naturally.
    - Use easy 'Global English' for accessibility, but weave in 'Sophisticated and Intellectual vocabulary' to maintain depth.
    - Strictly avoid sensitive, political, or controversial issues. Keep it clean and positive.

    [Structure - Must follow for length and quality]
    1. Introduction: A warm, narrative opening that draws the reader in (approx. 200 words).
    2. Main Analysis: Deeply explore the technical strengths, personality, or trends (approx. 400 words).
    3. Deep Q&A: A section titled "Things We Wonder," answering common questions about this topic with kindness (approx. 250 words).
    4. Personal Insight & Summary: Humble advice from a personal perspective, followed by a clear summary (approx. 150 words).

    [Formatting]
    - Return clean HTML using ONLY <p>, <ul>, <li>, and <strong> tags.
    - No '#' symbols. Title must be on the first line.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 4000, # 1,000자 이상을 위해 충분한 한도 설정
            "temperature": 0.7
        }
    }

    res = requests.post(gen_url, json=payload)
    res_data = res.json()

    # [🚨 중요: 에러 진단 로직]
    if 'candidates' not in res_data:
        print("❌ AI가 글을 쓰지 못했습니다. 진짜 이유는 아래와 같습니다:")
        print(json.dumps(res_data, indent=2, ensure_ascii=False))
        return

    full_text = res_data['candidates'][0]['content']['parts'][0]['text']
    lines = full_text.strip().split('\n', 1)
    title = re.sub('<[^<]+?>', '', lines[0]).strip()
    body = lines[1] if len(lines) > 1 else ""

    # [3] 워드프레스 전송 (깨끗하고 다정한 레이아웃)
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PW}".encode()).decode()
    headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}
    
    # 깨끗하고 평화로운 이미지
    img_url = "https://images.unsplash.com/photo-1490818387583-1baba5e638af?auto=format&fit=crop&q=80&w=1200"
    
    styled_content = f"""
    <div style="font-family: 'Georgia', serif; line-height: 2; color: #333; font-size: 17px; max-width: 800px; margin: auto;">
        <img src="{img_url}" style="width: 100%; border-radius: 15px; margin-bottom: 40px;">
        {body}
        <p style="text-align: center; color: #999; margin-top: 50px; font-style: italic;">
            "Small insights for a healthier, kinder world."
        </p>
    </div>
    """

    print("📤 워드프레스로 전송 중...")
    wp_res = requests.post(f"{WP_URL}/index.php?rest_route=/wp/v2/posts", headers=headers, json={
        'title': title,
        'content': styled_content,
        'status': 'publish'
    })

    if wp_res.status_code in [200, 201]:
        print(f"✨ 발행 성공! 제목: {title}")
    else:
        print(f"❌ 워드프레스 전송 실패: {wp_res.text}")

if __name__ == "__main__":
    run_premium_automation()
