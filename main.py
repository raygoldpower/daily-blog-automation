import requests
import base64
import os
import json
import re
import random

# [환경 변수] 
API_KEY = os.environ.get("GEMINI_API_KEY")
WP_USER = os.environ.get("WP_USER")
WP_APP_PW = os.environ.get("WP_APP_PW")
WP_URL = os.environ.get("WP_URL", "").strip("/")

def run_premium_editor():
    # 이 문구가 로그에 뜨는지 반드시 확인하세요!
    print("🚀 [FINAL CONFIRMATION] VERSION 6.0 - THE MASTER ENGINE START")

    # [1] 대표님이 원하신 6대 지적 테마
    topics = [
        "A deep analysis of a world-class athlete's mindset and humble character",
        "How global health trends are helping people find true balance",
        "The inspiring human story behind a legendary sports performance",
        "Celebrities who use their influence for positive global change",
        "Practical wellness tips: Merging modern science with humble living",
        "The impact of personality and character on physical excellence"
    ]
    selected_topic = random.choice(topics)
    print(f"📌 주제 선정 완료: {selected_topic}")

    # [2] 제미나이 정식 v1 주소 (에러의 핵심 해결책)
    gen_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    # 1,000자 이상의 고품격 집필을 위한 마스터 프롬프트
    prompt = f"""
    Write a deeply helpful and intellectual English column (minimum 1,000 words) about: [{selected_topic}].
    - Persona: Humble, friendly, and professional storyteller.
    - Perspective: Mix 1st person ('I') and 3rd person ('They/We').
    - Structure: Warm Narrative Opening -> Intellectual Analysis -> Human Personality Focus -> Q&A -> Bullet-point Summary.
    - Format: Use HTML <p> tags for all paragraphs.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7}
    }

    print("📡 AI에게 1,000자 대작 집필을 요청 중입니다 (약 30초 소요)...")
    res = requests.post(gen_url, json=payload)
    res_data = res.json()

    if 'candidates' not in res_data:
        print("❌ AI 응답 실패. 아래 내용을 확인하세요:")
        print(json.dumps(res_data, indent=2))
        return

    full_text = res_data['candidates'][0]['content']['parts'][0]['text']
    
    # [3] 워드프레스 전송 (고급스러운 디자인 레이아웃)
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PW}".encode()).decode()
    headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}
    
    img_url = "https://images.unsplash.com/photo-1490818387583-1baba5e638af?auto=format&fit=crop&q=80&w=1200"
    styled_content = f"""
    <div style="font-family: 'Georgia', serif; line-height: 2.1; color: #333; font-size: 17px; max-width: 800px; margin: auto;">
        <img src="{img_url}" style="width: 100%; border-radius: 20px; margin-bottom: 40px;">
        {full_text}
        <p style="text-align: center; color: #999; margin-top: 60px; font-style: italic;">
            "Small insights for a better, healthier world."
        </p>
    </div>
    """

    wp_api_url = f"{WP_URL}/index.php?rest_route=/wp/v2/posts"
    print(f"📤 워드프레스로 고품격 칼럼을 전송합니다...")
    
    wp_res = requests.post(wp_api_url, headers=headers, json={
        'title': f'Global Insight: {selected_topic}',
        'content': styled_content,
        'status': 'publish'
    })

    if wp_res.status_code in [200, 201]:
        print(f"✅ [대성공] 블로그 발행이 완료되었습니다! 제목: {selected_topic}")
    else:
        print(f"❌ 워드프레스 에러: {wp_res.text}")

if __name__ == "__main__":
    run_premium_editor()
