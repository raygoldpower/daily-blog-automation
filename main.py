import requests
import base64
import os
import re

# 금고(Secrets)에서 정보 가져오기
API_KEY = os.environ.get("GEMINI_API_KEY")
WP_USER = os.environ.get("WP_USER")
WP_APP_PW = os.environ.get("WP_APP_PW")
WP_URL = os.environ.get("WP_URL").strip("/")

def run_final():
    print("🚀 엔진 가동: 오늘의 뉴스 분석 및 집필 시작...")
    
    # [1] 제미나이 작가 호출 (정식 v1 주소 사용)
    gen_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    prompt = """오늘의 글로벌 경제/기술 팩트를 하나 선정해 1,000자 내외의 담백한 에세이를 써라. 
    전문가 시각의 통찰을 담되 문체는 단조롭고 무심하게. HTML <p> 태그 사용. 제목은 첫 줄에 쓰고 '#' 쓰지 마라."""
    
    res = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]})
    full_text = res.json()['candidates'][0]['content']['parts'][0]['text']
    lines = full_text.strip().split('\n', 1)
    title = re.sub('<[^<]+?>', '', lines[0]).strip()
    body = lines[1] if len(lines) > 1 else ""

    # [2] 워드프레스 전송 설정
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PW}".encode()).decode()
    headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}
    
    # 흑백 이미지 및 본문 구성
    img = '<img src="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1000" style="width:100%; filter: grayscale(100%); margin-bottom:30px;">'
    data = {
        'title': title,
        'content': f"{img}\n{body}\n<p style='text-align:right; color:#999;'><em>글쓴이: 팩트의 이면을 기록하는 사람</em></p>",
        'status': 'publish' # <--- 이 'publish'가 핵심입니다!
    }

    # [3] 두 가지 경로로 번갈아 시도 (가장 확실한 방법)
    endpoints = [
        f"{WP_URL}/wp-json/wp/v2/posts",
        f"{WP_URL}/index.php?rest_route=/wp/v2/posts"
    ]
    
    for url in endpoints:
        print(f"📤 전송 중... ({url})")
        wp_res = requests.post(url, headers=headers, json=data)
        if wp_res.status_code in [200, 201]:
            print(f"✅ 드디어 발행 성공! 제목: {title}")
            return
    
    print(f"❌ 최종 실패. 응답코드: {wp_res.status_code}, 사유: {wp_res.text}")

if __name__ == "__main__":
    run_final()
