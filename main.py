import os
import requests
import random
from datetime import datetime

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
BLOG_ID = "4393162034375416055"

TOPICS = [
    {"title": "당신의 드리블이 느린 진짜 이유", "keyword": "soccer dribbling speed technique", "sport": "축구", "series": "드리블 마스터", "episode": 1},
    {"title": "드리블 속도를 2배 높이는 발목 훈련법", "keyword": "soccer ankle dribbling training", "sport": "축구", "series": "드리블 마스터", "episode": 2},
    {"title": "메시가 수비수를 제치는 과학적 원리", "keyword": "soccer dribbling biomechanics agility", "sport": "축구", "series": "드리블 마스터", "episode": 3},
    {"title": "농구 점프력, 타고나는 게 아니다", "keyword": "basketball jump training vertical leap", "sport": "농구", "series": "점프력 혁명", "episode": 1},
    {"title": "당신의 점프력을 30% 높이는 8주 프로그램", "keyword": "basketball vertical jump program", "sport": "농구", "series": "점프력 혁명", "episode": 2},
    {"title": "야구 타격 폼, 0.1초가 홈런을 결정한다", "keyword": "baseball batting form swing speed", "sport": "야구", "series": "타격의 과학", "episode": 1},
    {"title": "배트 스피드를 높이는 상체 근력 훈련", "keyword": "baseball bat speed upper body strength", "sport": "야구", "series": "타격의 과학", "episode": 2},
    {"title": "축구 스피드, 빠른 선수는 무엇이 다른가", "keyword": "soccer speed sprint training", "sport": "축구", "series": "스피드 혁명", "episode": 1},
    {"title": "100미터를 1초 단축하는 가속 훈련법", "keyword": "sprint acceleration training technique", "sport": "공통", "series": "스피드 혁명", "episode": 2},
    {"title": "농구 핸들링, 손이 아니라 뇌를 훈련하라", "keyword": "basketball ball handling brain training", "sport": "농구", "series": "핸들링 마스터", "episode": 1},
    {"title": "수비수를 읽는 법, 스포츠 심리전의 모든 것", "keyword": "sports psychology reading opponent", "sport": "공통", "series": "심리전 전략", "episode": 1},
    {"title": "압박 상황에서 최고의 퍼포먼스를 내는 법", "keyword": "sports performance under pressure psychology", "sport": "공통", "series": "심리전 전략", "episode": 2},
    {"title": "팀 스포츠에서 나를 빛나게 하는 포지셔닝", "keyword": "team sports positioning strategy", "sport": "공통", "series": "전술 마스터", "episode": 1},
    {"title": "패스 하나로 경기를 바꾸는 시야 훈련법", "keyword": "soccer basketball passing vision training", "sport": "공통", "series": "전술 마스터", "episode": 2},
    {"title": "90분을 뛰어도 지치지 않는 지구력 훈련", "keyword": "soccer endurance stamina training", "sport": "축구", "series": "체력 마스터", "episode": 1},
    {"title": "스포츠 선수의 체력을 결정하는 VO2max의 비밀", "keyword": "VO2max endurance sports training", "sport": "공통", "series": "체력 마스터", "episode": 2},
    {"title": "민첩성 훈련, 방향 전환 속도를 높이는 과학", "keyword": "agility training change of direction speed", "sport": "공통", "series": "민첩성 혁명", "episode": 1},
    {"title": "팀워크가 개인 기량을 끌어올리는 원리", "keyword": "team chemistry individual performance sports", "sport": "공통", "series": "팀 시너지", "episode": 1},
    {"title": "축구 슈팅력, 발이 아니라 몸통이 결정한다", "keyword": "soccer shooting power core rotation", "sport": "축구", "series": "슈팅 마스터", "episode": 1},
    {"title": "농구 3점슛 성공률을 높이는 신체역학", "keyword": "basketball three point shooting biomechanics", "sport": "농구", "series": "슈팅 마스터", "episode": 1},
]


def get_access_token():
    print("[인증] Google Access Token 발급 중...")
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "refresh_token": GOOGLE_REFRESH_TOKEN,
            "grant_type": "refresh_token"
        },
        timeout=10
    )
    if response.status_code != 200:
        raise Exception("토큰 발급 실패: " + response.text)
    print("[인증] 완료!")
    return response.json()["access_token"]


def generate_with_claude(prompt):
    print("[AI] Claude 사용 중...")
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 8000,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=120
    )
    if response.status_code != 200:
        raise Exception("Claude 오류: " + str(response.status_code) + " " + response.text[:200])
    return response.json()["content"][0]["text"]


def generate_post():
    topic = random.choice(TOPICS)
    print("[글 생성] 주제: " + topic["title"])

    series_info = ""
    if topic["episode"] > 1:
        series_info = (
            "이 글은 " + topic["series"] + " 시리즈 " + str(topic["episode"]) + "편입니다. "
            + "이전 편의 내용을 자연스럽게 이어받아 더 심화된 내용을 다루세요.\n\n"
        )

    prompt = (
        "당신은 스포츠 과학, 운동역학, 해부학, 스포츠 심리학을 깊이 이해하는 전문 스포츠 블로거입니다.\n"
        "경고: 한자, 일본어, 중국어 등 한국어가 아닌 문자는 절대 사용하지 마세요.\n"
        "모든 단어는 반드시 한글 또는 영어 알파벳으로만 작성하세요.\n\n"
        + series_info
        + "가장 중요한 원칙: 독자가 글의 주인공입니다.\n"
        "글을 읽는 사람이 직접 변화하고 성장하는 느낌을 받아야 합니다.\n"
        "메시의 드리블이 아니라, 당신의 드리블이 왜 느린지를 설명하세요.\n\n"
        "반드시 지켜야 할 원칙:\n"
        "반드시 존댓말을 사용하세요. 반말 금지.\n"
        "지침 내용을 절대 본문에 노출하지 마세요.\n"
        "한 단락은 3줄에서 4줄 이내로 끊어 쓰세요.\n"
        "단락 사이는 반드시 빈 줄을 넣으세요.\n"
        "소제목은 [소제목] 형식으로 표시하세요.\n"
        "4000자에서 6000자를 반드시 채워주세요. 절대 짧게 쓰지 마세요.\n"
        "각 소제목 아래 최소 4개에서 5개 단락을 작성하세요.\n"
        "실천 목록은 최소 5가지 이상 구체적으로 제시하세요.\n"
        "각 훈련법의 효과, 작용 근육, 횟수, 주의사항까지 상세히 설명하세요.\n\n"
        "글의 흐름 - 기승전결로 점점 깊어지게:\n"
        "1. 독자가 공감하는 문제나 고민으로 시작하세요.\n"
        "2. 왜 그 문제가 생기는지 과학적으로 설명하세요. 해부학, 생리학, 운동역학 용어를 괄호로 설명하세요.\n"
        "3. 연구 결과와 논문을 인용하듯 깊이 있는 근거를 제시하세요.\n"
        "4. 독자가 당장 실천할 수 있는 구체적인 훈련 프로그램을 번호로 제시하세요.\n"
        "5. 영양, 회복, 멘탈 관리까지 포괄적으로 다루세요.\n"
        "6. 독자가 오늘 당장 변화를 시작하고 싶게 만드는 마무리로 끝내세요.\n\n"
        "종목: " + topic["sport"] + "\n"
        "주제: " + topic["title"] + "\n"
        "목표 분량: 4000자에서 6000자\n\n"
        "위 주제로 한국어 블로그 포스팅을 작성해주세요.\n"
        "HTML 태그 없이 순수 텍스트로만 작성하세요.\n"
        "소제목은 [소제목] 형식으로 표시하세요.\n"
        "독자가 글의 주인공이 되도록, 독자 중심으로 작성하세요.\n"
        "기승전결 구조로 가벼운 공감에서 시작해 점점 전문적으로 깊어지세요.\n"
        "절대 짧게 끝내지 마세요. 목표 분량을 반드시 채워주세요.\n\n"
        "반드시 아래 형식으로 출력하세요:\n"
        "제목: (독자의 클릭을 유도하는 강렬한 제목)\n"
        "---\n"
        "(본문 내용)"
    )

    full_text = generate_with_claude(prompt)

    lines = full_text.strip().split("\n")
    title = ""
    body_lines = []
    separator_found = False

    for line in lines:
        if line.startswith("제목:"):
            title = line.replace("제목:", "").strip()
        elif line.strip() == "---":
            separator_found = True
        elif separator_found:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    if not title:
        title = topic["title"]
    if not body:
        body = full_text

    print("[완료] 제목: " + title)
    print("[완료] 글자수: " + str(len(body)) + "자")
    return {"title": title, "body": body, "topic": topic}


def get_images(keyword, count=2):
    if not UNSPLASH_ACCESS_KEY:
        return []
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query": keyword,
                "per_page": count,
                "orientation": "landscape",
                "client_id": UNSPLASH_ACCESS_KEY
            },
            timeout=10
        )
        images = []
        for photo in response.json().get("results", []):
            images.append({
                "url": photo["urls"]["regular"],
                "alt": photo.get("alt_description", keyword),
                "author": photo["user"]["name"],
                "author_url": photo["user"]["links"]["html"]
            })
        print("[이미지] " + str(len(images)) + "장 수집 완료")
        return images
    except Exception as e:
        print("[이미지 오류] " + str(e))
        return []


def body_to_html(body, images):
    paragraphs = body.split("\n")
    html = ""
    mid = len(paragraphs) // 2
    img_index = 0

    if images:
        img = images[0]
        html += '<div style="text-align:center;margin-bottom:30px;">'
        html += '<img src="' + img["url"] + '" alt="' + str(img["alt"]) + '" style="max-width:100%;border-radius:8px;"/>'
        html += '<p style="font-size:12px;color:#888;margin-top:6px;">Photo by <a href="' + img["author_url"] + '">' + img["author"] + '</a> on Unsplash</p>'
        html += "</div>\n"
        img_index = 1

    for i, para in enumerate(paragraphs):
        if not para.strip():
            html += '<p style="margin:14px 0;">&nbsp;</p>\n'
            continue
        if para.startswith("[") and "]" in para:
            heading = para.strip("[]").strip()
            html += '<h2 style="margin-top:40px;margin-bottom:14px;font-size:22px;border-left:4px solid #1565c0;padding-left:14px;color:#1a1a1a;">' + heading + "</h2>\n"
        elif len(para.strip()) > 1 and para.strip()[0].isdigit() and para.strip()[1] in [".", ")"]:
            html += '<p style="margin:8px 0 8px 24px;line-height:2.0;color:#333;">' + para + "</p>\n"
        else:
            html += '<p style="margin:12px 0;line-height:2.0;font-size:16px;color:#222;">' + para + "</p>\n"

        if i == mid and img_index < len(images):
            img = images[img_index]
            html += '<div style="text-align:center;margin:30px 0;">'
            html += '<img src="' + img["url"] + '" alt="' + str(img["alt"]) + '" style="max-width:100%;border-radius:8px;"/>'
            html += '<p style="font-size:12px;color:#888;margin-top:6px;">Photo by <a href="' + img["author_url"] + '">' + img["author"] + '</a> on Unsplash</p>'
            html += "</div>\n"
            img_index += 1

    return html


def post_to_blogger(post_data, images):
    print("\n[Blogger] 포스팅 시작...")
    access_token = get_access_token()
    body_html = body_to_html(post_data["body"], images)
    url = "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts?isDraft=false"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    payload = {
        "kind": "blogger#post",
        "title": post_data["title"],
        "content": body_html,
        "status": "LIVE"
    }
    print("[제목] " + post_data["title"])
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print("[응답] 상태코드: " + str(response.status_code))
    if response.status_code == 200:
        result = response.json()
        print("\n발행 완료!")
        print("   링크: " + result.get("url", ""))
        return True
    else:
        print("실패: " + response.text[:300])
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("AutoBlog Sports Publisher - Claude Edition")
    print("실행 시각: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)
    try:
        post = generate_post()
        images = get_images(post["topic"]["keyword"], count=2)
        post_to_blogger(post, images)
        print("\n모든 작업 완료!")
    except Exception as e:
        print("\n오류 발생: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
