import requests
import base64
import os
import json
import re

API_KEY = os.environ.get("GEMINI_API_KEY")
WP_USER = os.environ.get("WP_USER")
WP_APP_PW = os.environ.get("WP_APP_PW")
WP_URL = os.environ.get("WP_URL")

def run_automation():
    print("🕵️ 정밀 진단 모드 가동...")
    
    # [1] 모델 탐색
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    list_res = requests.get(list_url)
    models = [m['name'] for m in list_res.json().get('models', []) if 'generateContent' in m['supportedGenerationMethods']]
    target_model = models[0] if models else "models/gemini-1.5-flash"

    # [2] 글 생성
    gen_url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={API_KEY}"
    prompt = "오늘의 글로벌 경제 팩트 하나를 선정해 1,000자 내외의 담백한 에세이를 써라. HTML p 태그 사용."
    res = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]})
    full_text = res.json()['candidates'][0]['content']['parts'][0]['text']
    
    lines = full_text.strip().split('\n', 1)
    title = "[진단 포스팅] " + re.sub('<[^<]+?>', '', lines[0]).replace('#', '').strip()
    body = lines[1] if len(lines) > 1 else ""

    # [3] 워드프레스 전송 및 응답 상세 분석
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PW}".encode()).decode()
    headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}
    
    # 404를 피하기 위해 가장 표준적인 API 주소로 시도합니다.
    wp_api_url = f"{WP_URL}/wp-json/wp/v2/posts"
    
    print(f"📤 전송 시도 주소: {wp_api_url}")
    wp_res = requests.post(wp_api_url, headers=headers, json={'title': title, 'content': body, 'status': 'publish'})

    # 결과 분석
    print(f"📡 서버 응답 상태 코드: {wp_res.status_code}")
    print("📝 서버 응답 본문(중요):")
    print(wp_res.text) # 서버가 실제로 한 말을 그대로 출력합니다.

    if wp_res.status_code in [200, 201]:
        print(f"🎉 서버가 수락했습니다! 제목: {title}")
    else:
        print("❌ 서버가 거절했습니다. 위 응답 본문을 확인하세요.")

if __name__ == "__main__":
    run_automation()
