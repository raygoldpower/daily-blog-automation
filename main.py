import requests
import base64
import os
import json
import re
import random

# [환경 변수] GitHub Secrets에서 정보를 호출합니다.
API_KEY = os.environ.get("GEMINI_API_KEY")
WP_USER = os.environ.get("WP_USER")
WP_APP_PW = os.environ.get("WP_APP_PW")
WP_URL = os.environ.get("WP_URL").strip("/")

def run_premium_editor():
    print("💎 하이엔드 에디터 엔진 가동: 심층 칼럼 집필을 시작합니다...")

    # [1] 대표님의 6가지 핵심 테마를 정교화
    topics = [
        "The psychological resilience of elite athletes: What we can learn from their mindset",
        "Modern wellness trends: Balancing high-performance living with humble self-care",
        "The cultural impact of global celebrities: Moving beyond the spotlight to human contribution",
        "Analyzing the unique technical strengths and personal character of world-class performers",
        "Global lifestyle shifts: How modern society is redefining the meaning of a 'healthy life'",
        "The human element in sports: Why personality and ethics matter more than records"
    ]
    selected_topic = random.choice(topics)

    # [2] 지능형 프롬프트 설계 (대표님의 페르소나 주입)
    gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    prompt = f"""
    You are a world-class English columnist known for your humble, friendly, and intellectual writing style.
    Your mission is to write a deeply helpful and insightful article about: [{selected_topic}].
    
    [Strict Guidelines for High Quality]
    1. Persona: A warm-hearted expert. Use "I" to share personal reflections (1st person) and "They/We" for objective analysis (3rd person). Be humble but authoritative.
    2. Length & Depth: Minimum 1,000 words. Do not skip details. Deeply explore the "Human" aspect of the topic.
    3. Structure (Must include all parts):
       - 'The Narrative Opening': Start with a personal, warm story related to the topic (approx. 200 words).
       - 'Technical Insight': An intellectual analysis of the strengths, traits, or trends (approx. 400 words).
       - 'The Human Perspective': Discuss the personality and character of the individuals involved (approx. 200 words).
       - 'Insightful Q&A': A section titled "Questions We Often Ask," answering a deep curiosity with kindness.
       - 'Practical Compass': 3-5 bullet points of humble advice for the reader.
    4. Language: Use "Global English" for accessibility, but weave in "Intellectual & Sophisticated vocabulary" to showcase professional depth. 
    5. Constraints: Strictly avoid sensitive or controversial social/political issues. Focus only on help and information.
    6. Formatting: Return clean HTML using only <p>, <ul>, <li>, and <strong> tags. No '#' characters.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 4096,
            "temperature": 0.7,
            "topP": 0.9
        }
    }

    res = requests.post(gen_url, json=payload)
    res_data = res.json()

    if 'candidates' not in res_data:
        print("❌ AI 집필 실패. 사유:", json.dumps(res_data, indent=2))
        return

    full_text = res_data['candidates'][0]['content']['parts'][0]['text']
    
    # 제목과 본문 분리 로직 강화
    content_parts = full_text.strip().split('\n', 1)
    title = re.sub('<[^<]+?>', '', content_parts[0]).strip()
    body = content_parts[1] if len(content_parts) > 1 else ""

    # [3] 워드프레스 전송 (깨끗하고 전문적인 레이아웃)
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PW}".encode()).decode()
    headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}
    
    # 고해상도 고퀄리티 이미지 매칭 (Clean & Bright)
    img_url = "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&q=80&w=1200"
    
    styled_content = f"""
    <div style="font-family: 'Georgia', serif; color: #2c3e50; line-height: 2.1; font-size: 17px; max-width: 800px; margin: auto;">
        <img src="{img_url}" style="width: 100%; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 50px;">
        {body}
        <hr style="border: 0; border-top: 1px solid #eee; margin: 60px 0;">
        <p style="text-align: center; color: #7f8c8d; font-style: italic;">
            "Seeking wisdom in the ordinary, sharing health for the heart."
        </p>
    </div>
    """

    post_data = {
        'title': title,
        'content': styled_content,
        'status': 'publish'
    }

    print(f"📤 워드프레스로 고퀄리티 칼럼을 전송합니다: {title}")
    wp_res = requests.post(f"{WP_URL}/index.php?rest_route=/wp/v2/posts", headers=headers, json=post_data)

    if wp_res.status_code in [200, 201]:
        print(f"✨ [성공] 글로벌 칼럼 발행이 완료되었습니다.")
    else:
        print(f"❌ [실패] 응답코드 {wp_res.status_code}: {wp_res.text}")

if __name__ == "__main__":
    run_premium_editor()
