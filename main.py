import requests
import base64
import os
import json
import re
import random

# [설정] 깃허브 Secrets
API_KEY = os.environ.get("GEMINI_API_KEY")
WP_USER = os.environ.get("WP_USER")
WP_APP_PW = os.environ.get("WP_APP_PW")
WP_URL = os.environ.get("WP_URL").strip("/")

def run_premium_editor():
    # 이 줄이 로그에 나오는지 확인하는 게 핵심입니다!
    print("🚀 [CHECK] VERSION 4.1 - STABLE ENGINE START")

    topics = ["Global sports talent analysis", "Human wellness and character", "Global celebrity positive influence"]
    selected_topic = random.choice(topics)

    # 주소에서 beta를 완전히 뺐습니다.
    gen_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": f"Write a 1,000-word humble and intellectual English column about {selected_topic}. Use HTML <p> tags."}]}],
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7}
    }

    res = requests.post(gen_url, json=payload)
    res_data = res.json()

    if 'candidates' not in res_data:
        print("❌ AI 응답 실패 사유:")
        print(json.dumps(res_data, indent=2, ensure_ascii=False))
        return

    full_text = res_data['candidates'][0]['content']['parts'][0]['text']
    # (이하 발행 로직 생략 - 핵심은 위 주소와 로그 확인입니다)
    
    print(f"✅ AI 글 생성 성공! 이제 발행을 시도합니다.")
    # 실제 발행 코드가 아래에 이어집니다...
    # (워드프레스 전송 로직 부분)
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PW}".encode()).decode()
    headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}
    wp_api_url = f"{WP_URL}/index.php?rest_route=/wp/v2/posts"
    requests.post(wp_api_url, headers=headers, json={'title': 'Global Insight', 'content': full_text, 'status': 'publish'})

if __name__ == "__main__":
    run_premium_editor()
