import requests
import base64
import os
import json
import re
import random

# [환경 변수 호출]
API_KEY = os.environ.get("GEMINI_API_KEY")
WP_USER = os.environ.get("WP_USER")
WP_APP_PW = os.environ.get("WP_APP_PW")
WP_URL = os.environ.get("WP_URL", "").strip().rstrip("/")

def run_premium_editor():
    print("🔥 [V10.0-FINAL] 마지막 정밀 점검 엔진 가동 시작...")

    # [1] 대표님의 6대 지적 테마 (주제 선정)
    topics = [
        "Analysis of a world-class athlete's humble character and mindset",
        "Global wellness trends and practical lifestyle advice",
        "The inspiring human story behind sporting legends",
        "Positive social influence of global celebrities"
    ]
    selected_topic = random.choice(topics)
    print(f"📌 오늘의 선정 주제: {selected_topic}")

    # [2] 제미나이 1,000자 집필 요청 (정식 v1 주소)
    gen_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    prompt = f"""
    Write a DEEP and INTELLECTUAL English column (minimum 1,000 words) about: [{selected_topic}].
    - Structure: Narrative Story -> Deep Analysis -> Q&A -> Summary.
    - Style: Professional, humble, and friendly.
    - Format: Use HTML <p> tags for ALL paragraphs.
    """

    print("📡 AI에게 1,000자 대작 집필을 요청 중... (약 20-30초 소요)")
    res = requests.post(gen_url, json={
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7}
    })
    
    res_data = res.json()
    if 'candidates' not in res_data:
        print("❌ [AI 에러] AI가 글을 쓰지 못했습니다. API 키를 확인하세요.")
        print(json.dumps(res_data, indent=2))
        return

    full_text = res_data['candidates'][0]['content']['parts'][0]['text']
    print(f"✅ AI 글 생성 완료! (글자 수: 약 {len(full_text)}자)")

    # [3] 워드프레스 전송 (가장 확실한 경로)
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PW}".encode()).decode()
    headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}
    
    # 404를 피하기 위한 표준 API 경로
    wp_api_url = f"{WP_URL}/wp-json/wp/v2/posts"
    print(f"📤 전송 시도: {wp_api_url}")
    
    data = {
        'title': f'The Global Insight: {selected_topic}',
        'content': f"<div style='line-height:2.1; font-size:17px;'>{full_text}</div>",
        'status': 'publish'
    }

    wp_res = requests.post(wp_api_url, headers=headers, json=data)

    # [4] 결과 보고 (영수증 강제 출력)
    print("\n" + "="*50)
    if wp_res.status_code in [200, 201]:
        link = wp_res.json().get('link')
        print(f"✅ [최종 성공] 글이 블로그에 올라갔습니다!")
        print(f"🔗 확인 링크: {link}")
    else:
        print(f"❌ [발행 실패] 서버 응답 코드: {wp_res.status_code}")
        print(f"📝 실패 사유: {wp_res.text}")
        print("\n💡 조언: WP_URL 주소나 WP_APP_PW 비밀번호가 틀렸을 확률이 높습니다.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_premium_editor()
