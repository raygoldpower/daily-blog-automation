import requests
import base64
import os
import json
import re

# 깃허브 금고(Secrets)에서 정보를 안전하게 가져옵니다.
API_KEY = os.environ.get("GEMINI_API_KEY")
WP_USER = os.environ.get("WP_USER")
WP_APP_PW = os.environ.get("WP_APP_PW")
WP_URL = os.environ.get("WP_URL")

def run_automation():
    print("📰 오늘의 글로벌 뉴스 팩트를 분석하여 집필을 시작합니다...")
    
    # [1] 모델 탐색 (404 에러 방지)
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    list_res = requests.get(list_url)
    models = [m['name'] for m in list_res.json().get('models', []) if 'generateContent' in m['supportedGenerationMethods']]
    target_model = models[0] if models else "models/gemini-1.5-flash"

    # [2] 뉴스 팩트 기반 집필 지시 (글로벌 팩트 중심)
    gen_url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={API_KEY}"
    prompt = """
    너는 기술과 경제의 본질을 기록하는 시니어 작가다. 
    오늘의 정치, 경제, 혹은 세계적인 주요 뉴스 팩트 하나를 선정해라.
    
    [집필 규칙]
    1. 팩트 중심: 현재 세계가 직면한 거대한 흐름(반도체, 공급망, 인플레이션 등)의 사실을 담아라.
    2. 여운의 미학: 수식어는 빼고, 단조롭고 무심한 문체로 써라. 하지만 읽고 나면 깊은 사유를 하게 만들어라.
    3. 분량: 1,000자 내외. HTML <p> 태그 사용.
    4. 보안: 박민규 대표님의 개인정보는 절대 언급하지 마라.
    
    제목은 순수 텍스트로, 본문은 HTML로 작성해라.
    """

    res = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]})
    full_text = res.json()['candidates'][0]['content']['parts'][0]['text']
    
    lines = full_text.strip().split('\n', 1)
    title = re.sub('<[^<]+?>', '', lines[0]).replace('#', '').strip()
    body = lines[1] if len(lines) > 1 else ""

    # [3] 블로그 전송
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PW}".encode()).decode()
    img_tag = '<img src="https://images.unsplash.com/photo-1451187530230-b237ee20672a?auto=format&fit=crop&q=80&w=1000" style="width:100%; filter: grayscale(100%); margin-bottom:30px;">'
    final_content = f"{img_tag}\n{body}\n<p style='text-align:right; color:#999; margin-top:50px;'><em>글쓴이: 팩트의 이면을 기록하는 사람</em></p>"

    wp_api_url = f"{WP_URL}/index.php?rest_route=/wp/v2/posts"
    wp_res = requests.post(wp_api_url, 
                           headers={'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}, 
                           json={'title': title, 'content': final_content, 'status': 'publish'})
    
    if wp_res.status_code in [200, 201]:
        print(f"🎉 발행 성공: {title}")
    else:
        print(f"❌ 전송 실패: {wp_res.text}")

if __name__ == "__main__":
    run_automation()
