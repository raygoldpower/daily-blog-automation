import requests
import base64
import os
import json
import re
import random

# [환경 변수 설정]
API_KEY = os.environ.get("GEMINI_API_KEY")
WP_USER = os.environ.get("WP_USER")
WP_APP_PW = os.environ.get("WP_APP_PW")
WP_URL = "https://min85power-gwtmy.wordpress.com"

def run_global_insight_blog():
    print("🚀 오늘의 뉴스 팩트 분석 및 고품격 칼럼 발행을 시작합니다...")

    # [1] 뉴스 기반의 지적인 주제 선정
    topics = [
        "A psychological study on elite athletes' resilience and humble beginnings",
        "Global shifts in workplace wellness: How human-centric design is winning",
        "The impact of influential figures on positive social trends",
        "Exploring the hidden character traits of world-class performers",
        "Modern health trends: Beyond the surface of global wellness movements"
    ]
    selected_topic = random.choice(topics)

    # [2] 지능형 에디팅 (1,000자 이상의 다정하고 지적인 글)
    gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    prompt = f"""
    Write a 1,000-word deep English column about: [{selected_topic}].
    
    [Requirements]
    - Persona: Humble, friendly, and intellectual. Helping the reader is the priority.
    - Perspective: Mix 1st person (personal reflection) and 3rd person (fact analysis).
    - Structure: Narrative story -> Deep analysis -> Q&A -> Summary points.
    - Vocabulary: Easy Global English with occasional sophisticated, intelligent terms.
    - Safety: No controversial or political issues.
    - Format: HTML <p>, <ul>, <li> tags only.
    """

    res = requests.post(gen_url, json={
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7}
    })
    
    res_data = res.json()
    if 'candidates' not in res_data:
        print("❌ 실패:", json.dumps(res_data, indent=2))
        return

    full_text = res_data['candidates'][0]['content']['parts'][0]['text']
    content_parts = full_text.strip().split('\n', 1)
    title = re.sub('<[^<]+?>', '', content_parts[0]).strip()
    body = content_parts[1] if len(content_parts) > 1 else ""

    # [3] 워드프레스 발행
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PW}".encode()).decode()
    headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}
    
    img_url = "https://images.unsplash.com/photo-1493612276216-ee3925520721?auto=format&fit=crop&q=80&w=1200"
    styled_content = f"""
    <div style="font-family: 'Georgia', serif; color: #333; line-height: 2; font-size: 17px;">
        <img src="{img_url}" style="width: 100%; border-radius: 15px; margin-bottom: 40px;">
        {body}
        <p style="text-align: center; color: #888; margin-top: 50px;"><em>In pursuit of helpful wisdom for the global community.</em></p>
    </div>
    """

    wp_res = requests.post(f"{WP_URL}/index.php?rest_route=/wp/v2/posts", headers=headers, json={
        'title': title,
        'content': styled_content,
        'status': 'publish'
    })

    if wp_res.status_code in [200, 201]:
        print(f"✨ 발행 성공: {title}")
    else:
        print(f"❌ 워드프레스 에러: {wp_res.text}")

if __name__ == "__main__":
    run_global_insight_blog()
