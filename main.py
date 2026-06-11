import os
import requests
import random
from datetime import datetime
import json
import re

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
FACEBOOK_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "")
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN", "")
BLOG_ID = "4393162034375416055"

SPORT_EMOJI = {
    "축구": "⚽", "농구": "🏀", "야구": "⚾", "공통": "🏆",
    "근육학": "💪", "재활": "🩺", "영양": "🥗", "심리": "🧠",
    "체력": "🔥", "유연성": "🤸", "생리학": "🫀", "물리치료": "🏥",
    "역학": "⚙️", "해부학": "🦴", "신체균형": "⚖️", "스포츠의학": "🩻",
}

TOPICS = [
    # 축구
    {"title": "발목이 굳으면 드리블 속도가 떨어지는 진짜 이유... 아무도 말 안 해줍니다", "keyword": "soccer dribbling ankle mobility", "img_keyword": "soccer dribbling", "sport": "축구", "series": "드리블 마스터", "episode": 1},
    {"title": "100m 달리기 선수도 못 따라오는 축구 선수들의 순간 가속 비밀", "keyword": "soccer acceleration sprint training", "img_keyword": "soccer sprint", "sport": "축구", "series": "스피드 혁명", "episode": 1},
    {"title": "슛을 아무리 세게 차도 골이 안 들어간다면... 고관절을 확인하세요", "keyword": "soccer shooting hip rotation power", "img_keyword": "soccer shooting", "sport": "축구", "series": "슈팅 마스터", "episode": 1},
    {"title": "후반 30분에도 스프린트하는 선수들이 숨기고 있는 체력 훈련법", "keyword": "soccer endurance 90 minutes stamina", "img_keyword": "soccer endurance", "sport": "축구", "series": "체력 마스터", "episode": 1},
    {"title": "축구하다 무릎 다치는 선수들이 공통적으로 빠뜨리는 훈련 한 가지", "keyword": "soccer knee injury prevention squat", "img_keyword": "knee injury soccer", "sport": "축구", "series": "부상 예방", "episode": 1},
    # 농구
    {"title": "점프력은 타고나는 게 아닙니다... 3개월 만에 10cm 높인 훈련법", "keyword": "basketball jump plyometric training", "img_keyword": "basketball jump", "sport": "농구", "series": "점프력 혁명", "episode": 1},
    {"title": "농구 드리블이 늘지 않는 이유는 손이 아니라 뇌에 있었습니다", "keyword": "basketball dribbling brain hand coordination", "img_keyword": "basketball dribbling", "sport": "농구", "series": "핸들링 마스터", "episode": 1},
    {"title": "프로선수들이 숨기고 싶어하는 3점슛 성공률의 비밀", "keyword": "basketball three point wrist snap shooting", "img_keyword": "basketball shooting", "sport": "농구", "series": "슈팅 마스터", "episode": 1},
    # 야구
    {"title": "배트 스피드가 안 나온다면... 상체가 아니라 하체를 먼저 보세요", "keyword": "baseball bat speed hip rotation", "img_keyword": "baseball batting", "sport": "야구", "series": "타격의 과학", "episode": 1},
    {"title": "투수 어깨가 망가지기 전에 반드시 나타나는 신호 4가지", "keyword": "baseball pitcher rotator cuff injury prevention", "img_keyword": "baseball pitcher shoulder", "sport": "야구", "series": "투구의 과학", "episode": 1},
    # 근육학
    {"title": "스쿼트만 해도 허벅지 앞이 안 커진다면... 이 변형 동작을 모르는 겁니다", "keyword": "quadriceps squat variation muscle building", "img_keyword": "quadriceps squat", "sport": "근육학", "series": "근육 해부학", "episode": 1},
    {"title": "전력 질주 중에 왜 허벅지 뒤만 터질까... 아무도 말 안 해준 이유", "keyword": "hamstring eccentric training injury prevention", "img_keyword": "hamstring exercise", "sport": "근육학", "series": "근육 해부학", "episode": 2},
    {"title": "허리 통증의 진짜 원인은 허리가 아닙니다... 이 근육을 아세요?", "keyword": "transverse abdominis core activation back pain", "img_keyword": "core training", "sport": "근육학", "series": "코어 과학", "episode": 1},
    {"title": "어깨 운동 열심히 했는데 한쪽만 커지는 이유", "keyword": "deltoid three heads shoulder training", "img_keyword": "shoulder deltoid workout", "sport": "근육학", "series": "상체 해부학", "episode": 1},
    {"title": "발목을 자주 삐는 사람들이 공통적으로 약한 근육이 있습니다", "keyword": "calf muscle ankle stability injury prevention", "img_keyword": "calf muscle", "sport": "근육학", "series": "하체 해부학", "episode": 1},
    {"title": "헬스장에서 아무리 열심히 해도 근육이 안 크는 진짜 이유", "keyword": "muscle protein synthesis hypertrophy", "img_keyword": "muscle growth", "sport": "근육학", "series": "근육 성장 과학", "episode": 1},
    {"title": "어깨 통증의 80%는 이 근육 때문입니다... 처음 들어보셨죠?", "keyword": "serratus anterior weakness shoulder pain", "img_keyword": "shoulder pain", "sport": "근육학", "series": "상체 해부학", "episode": 2},
    {"title": "무릎이 아픈데 엉덩이 운동을 하라고요? 이유가 있습니다", "keyword": "gluteus medius knee pain pelvic balance", "img_keyword": "gluteus medius hip", "sport": "근육학", "series": "하체 해부학", "episode": 2},
    # 재활
    {"title": "무릎 연골이 닳기 전에 반드시 해야 할 운동... 병원에서 안 알려줍니다", "keyword": "patellar tendinitis rehabilitation exercise", "img_keyword": "knee rehabilitation", "sport": "재활", "series": "부상 재활", "episode": 1},
    {"title": "허리 디스크 진단받은 후 절대 하면 안 되는 운동 3가지", "keyword": "lumbar disc stabilization exercise", "img_keyword": "lower back pain", "sport": "재활", "series": "부상 재활", "episode": 2},
    {"title": "발목 삐끗한 후 바로 냉찜질했다면... 잘못된 겁니다", "keyword": "ankle sprain rehabilitation return to sport", "img_keyword": "ankle sprain", "sport": "재활", "series": "부상 재활", "episode": 3},
    {"title": "어깨 충돌 증후군... 병원 가기 전 집에서 먼저 해볼 수 있는 것들", "keyword": "shoulder impingement home rehabilitation", "img_keyword": "shoulder impingement", "sport": "재활", "series": "부상 재활", "episode": 4},
    {"title": "아킬레스건이 아플 때 스트레칭하면 안 된다는 걸 아는 사람이 없습니다", "keyword": "achilles tendinopathy exercise avoid", "img_keyword": "achilles tendon", "sport": "재활", "series": "부상 재활", "episode": 5},
    # 영양
    {"title": "운동 전에 뭘 먹느냐가 운동 효과를 50% 이상 바꿉니다", "keyword": "pre workout meal carbohydrate timing", "img_keyword": "pre workout meal", "sport": "영양", "series": "스포츠 영양학", "episode": 1},
    {"title": "탄수화물을 끊었더니 오히려 운동 실력이 떨어진 이유", "keyword": "carbohydrate glycogen sports performance", "img_keyword": "carbohydrate food", "sport": "영양", "series": "스포츠 영양학", "episode": 2},
    {"title": "크레아틴 먹는 사람들이 가장 많이 하는 실수", "keyword": "creatine dosage timing supplement", "img_keyword": "creatine supplement", "sport": "영양", "series": "보충제 과학", "episode": 1},
    {"title": "운동 중 물만 마시면 오히려 쥐가 나는 이유", "keyword": "hydration during exercise timing amount", "img_keyword": "hydration water sports", "sport": "영양", "series": "스포츠 영양학", "episode": 3},
    {"title": "단백질 얼마나 먹어야 할까... 헬스 유튜버들이 다 틀린 이유", "keyword": "protein daily intake calculation body weight", "img_keyword": "protein food", "sport": "영양", "series": "스포츠 영양학", "episode": 4},
    {"title": "운동 후 닭가슴살만 먹으면 오히려 회복이 느린 이유", "keyword": "post workout recovery nutrition combination", "img_keyword": "post workout nutrition", "sport": "영양", "series": "스포츠 영양학", "episode": 5},
    # 심리
    {"title": "경기 전 긴장되면 잘하는 선수, 망하는 선수... 차이가 뭘까요", "keyword": "pre game routine anxiety control athletes", "img_keyword": "athlete focus", "sport": "심리", "series": "스포츠 심리학", "episode": 1},
    {"title": "압박 상황에서 집중력이 무너지는 사람들의 공통점", "keyword": "focus under pressure mental training sports", "img_keyword": "mental training", "sport": "심리", "series": "스포츠 심리학", "episode": 2},
    {"title": "열심히 하는데 실력이 안 늘 때... 슬럼프의 진짜 원인", "keyword": "sports slump recovery psychology steps", "img_keyword": "athlete motivation", "sport": "심리", "series": "스포츠 심리학", "episode": 3},
    {"title": "머릿속으로 연습해도 실력이 는다는 게 사실일까요?", "keyword": "mental imagery visualization sports performance", "img_keyword": "visualization meditation", "sport": "심리", "series": "스포츠 심리학", "episode": 4},
    # 체력
    {"title": "숨이 빨리 차는 사람들이 모르는 폐활량 vs 심폐기능의 차이", "keyword": "VO2max interval training intensity", "img_keyword": "interval running", "sport": "체력", "series": "체력 과학", "episode": 1},
    {"title": "마라톤 선수들이 절대 안 지치는 이유... 젖산의 오해와 진실", "keyword": "lactate threshold training endurance", "img_keyword": "endurance running", "sport": "체력", "series": "체력 과학", "episode": 2},
    {"title": "HIIT 30분 했는데 왜 살이 안 빠질까... 휴식 시간이 문제였습니다", "keyword": "HIIT rest interval optimization fat loss", "img_keyword": "HIIT workout", "sport": "체력", "series": "유산소 과학", "episode": 1},
    {"title": "심박수 보고 운동하면 왜 살이 더 잘 빠질까", "keyword": "heart rate zone exercise intensity training", "img_keyword": "heart rate monitor", "sport": "체력", "series": "체력 과학", "episode": 3},
    # 유연성
    {"title": "운동 전 스트레칭이 오히려 부상을 유발한다는 게 사실일까요", "keyword": "dynamic stretching warm up injury prevention", "img_keyword": "dynamic stretching", "sport": "유연성", "series": "유연성 과학", "episode": 1},
    {"title": "고관절이 굳으면 허리 무릎 어깨까지 망가지는 이유", "keyword": "hip flexor mobility stretching exercises", "img_keyword": "hip stretching", "sport": "유연성", "series": "가동성 혁명", "episode": 1},
    {"title": "폼롤러 잘못 쓰면 오히려 근육이 더 굳습니다", "keyword": "foam rolling myofascial release technique", "img_keyword": "foam roller", "sport": "유연성", "series": "회복 과학", "episode": 1},
    {"title": "어깨 통증 있는 사람들이 등을 먼저 풀어야 하는 이유", "keyword": "thoracic spine mobility shoulder pain", "img_keyword": "spine mobility", "sport": "유연성", "series": "가동성 혁명", "episode": 2},
    # 생리학
    {"title": "운동할 때 근육에서 실제로 일어나는 일... 교과서엔 없는 이야기", "keyword": "muscle physiology exercise ATP energy", "img_keyword": "muscle exercise", "sport": "생리학", "series": "운동 생리학", "episode": 1},
    {"title": "유산소 운동 30분 해도 지방이 안 타는 사람들의 공통점", "keyword": "fat oxidation aerobic exercise physiology", "img_keyword": "aerobic exercise", "sport": "생리학", "series": "운동 생리학", "episode": 2},
    {"title": "잠자는 동안 근육이 큰다는 게 진짜입니까?", "keyword": "growth hormone sleep muscle recovery", "img_keyword": "sleep recovery", "sport": "생리학", "series": "운동 생리학", "episode": 3},
    {"title": "운동 후 근육통이 심할수록 성장이 빠르다는 믿음의 진실", "keyword": "DOMS delayed onset muscle soreness cause", "img_keyword": "muscle soreness", "sport": "생리학", "series": "운동 생리학", "episode": 4},
    {"title": "운동선수의 심장이 일반인보다 50% 더 큰 이유", "keyword": "cardiac adaptation exercise athlete heart", "img_keyword": "heart cardio", "sport": "생리학", "series": "운동 생리학", "episode": 5},
    {"title": "스트레스를 많이 받으면 왜 살이 찌고 근육이 빠질까", "keyword": "cortisol muscle loss stress hormone", "img_keyword": "stress cortisol", "sport": "생리학", "series": "운동 생리학", "episode": 6},
    # 물리치료
    {"title": "어깨가 아프다고 하면 물리치료사가 왜 목부터 만져볼까요", "keyword": "shoulder pain physical therapy assessment", "img_keyword": "shoulder physical therapy", "sport": "물리치료", "series": "물리치료 가이드", "episode": 1},
    {"title": "무릎 통증... 병원 가야 할 신호 vs 집에서 해결 가능한 신호", "keyword": "knee pain self diagnosis when to see doctor", "img_keyword": "knee pain", "sport": "물리치료", "series": "물리치료 가이드", "episode": 2},
    {"title": "테니스 안 치는데 테니스 엘보가 생겼다면... 이것 때문입니다", "keyword": "tennis elbow treatment home exercise", "img_keyword": "tennis elbow", "sport": "물리치료", "series": "물리치료 가이드", "episode": 3},
    {"title": "아침마다 발바닥이 찌릿한 사람들이 놓치고 있는 것", "keyword": "plantar fasciitis morning stretching routine", "img_keyword": "plantar fasciitis foot", "sport": "물리치료", "series": "물리치료 가이드", "episode": 4},
    {"title": "거북목 교정 운동... 하루 5분으로 정말 효과가 있을까요", "keyword": "forward head posture correction exercise", "img_keyword": "neck posture", "sport": "물리치료", "series": "물리치료 가이드", "episode": 5},
    # 역학
    {"title": "달리기할 때 무릎이 아픈 사람들이 공통적으로 틀린 자세", "keyword": "running biomechanics knee impact reduction", "img_keyword": "running form", "sport": "역학", "series": "스포츠 역학", "episode": 1},
    {"title": "스쿼트할 때 무릎이 안쪽으로 무너지는 이유... 무릎 문제가 아닙니다", "keyword": "squat knee valgus cause biomechanics", "img_keyword": "squat form", "sport": "역학", "series": "스포츠 역학", "episode": 2},
    {"title": "데드리프트로 허리 다치는 사람들이 몰랐던 척추 중립의 진실", "keyword": "deadlift spine neutral position injury prevention", "img_keyword": "deadlift", "sport": "역학", "series": "스포츠 역학", "episode": 3},
    {"title": "착지하는 0.1초가 무릎 십자인대를 결정합니다", "keyword": "landing mechanics ACL injury prevention", "img_keyword": "jump landing", "sport": "역학", "series": "스포츠 역학", "episode": 4},
    # 해부학
    {"title": "무릎이 왜 이렇게 자주 다칠까... 구조를 보면 당연합니다", "keyword": "knee joint anatomy structure injury", "img_keyword": "knee joint", "sport": "해부학", "series": "스포츠 해부학", "episode": 1},
    {"title": "어깨가 360도 돌아가는 건 축복이자 저주입니다", "keyword": "shoulder joint anatomy mobility instability", "img_keyword": "shoulder joint", "sport": "해부학", "series": "스포츠 해부학", "episode": 2},
    {"title": "발 아치가 무너지면 무릎 허리 목까지 망가지는 연결고리", "keyword": "foot arch structure running performance", "img_keyword": "foot arch", "sport": "해부학", "series": "스포츠 해부학", "episode": 3},
    {"title": "앉을 때 자세 하나가 허리 디스크 압력을 3배 높입니다", "keyword": "spinal disc anatomy pressure posture", "img_keyword": "spine disc", "sport": "해부학", "series": "스포츠 해부학", "episode": 4},
    # 신체균형
    {"title": "거울 앞에 서면 한쪽 어깨가 낮은 이유... 방치하면 생기는 일", "keyword": "pelvic tilt imbalance lower back knee pain", "img_keyword": "pelvic posture", "sport": "신체균형", "series": "체형 교정", "episode": 1},
    {"title": "척추측만증... 집에서 5분이면 자가 진단 가능합니다", "keyword": "shoulder uneven scoliosis self check", "img_keyword": "scoliosis posture", "sport": "신체균형", "series": "체형 교정", "episode": 2},
    {"title": "평발인 사람이 운동할 때 반드시 알아야 하는 것들", "keyword": "flat feet sports performance correction", "img_keyword": "flat feet", "sport": "신체균형", "series": "체형 교정", "episode": 3},
    {"title": "X자 다리 때문에 무릎이 아픈데 스쿼트만 하고 있다면...", "keyword": "knock knees correction gluteus medius", "img_keyword": "knock knees legs", "sport": "신체균형", "series": "체형 교정", "episode": 4},
    # 스포츠의학
    {"title": "성장기 아이가 운동 많이 하면 키가 안 큰다는 게 사실일까요", "keyword": "youth athlete growth plate safe training", "img_keyword": "youth sports training", "sport": "스포츠의학", "series": "스포츠의학 가이드", "episode": 1},
    {"title": "여름 운동 중 갑자기 쓰러지기 전에 반드시 나타나는 신호들", "keyword": "heat stroke warning signs summer exercise", "img_keyword": "heat stroke summer", "sport": "스포츠의학", "series": "스포츠의학 가이드", "episode": 2},
    {"title": "운동 중 갑자기 쥐가 나는 이유... 물 부족이 아닙니다", "keyword": "exercise cramp cause prevention electrolyte", "img_keyword": "muscle cramp", "sport": "스포츠의학", "series": "스포츠의학 가이드", "episode": 3},
    {"title": "열심히 운동하는데 왜 몸이 더 안 좋아질까... 과훈련의 징후들", "keyword": "overtraining syndrome self check recovery", "img_keyword": "overtraining fatigue", "sport": "스포츠의학", "series": "스포츠의학 가이드", "episode": 4},
    # 공통
    {"title": "7시간 자면 근육이 더 잘 큰다는 게 진짜입니까?", "keyword": "sleep 7 hours muscle growth performance", "img_keyword": "sleep recovery", "sport": "공통", "series": "회복 과학", "episode": 1},
    {"title": "나이 들면서 근육이 빠지는 건 막을 수 없을까요", "keyword": "sarcopenia aging muscle loss prevention", "img_keyword": "aging fitness", "sport": "공통", "series": "시니어 스포츠", "episode": 1},
    {"title": "아이 운동 시작 나이... 너무 일찍 시작하면 생기는 일", "keyword": "youth sports age appropriate training", "img_keyword": "kids sports", "sport": "공통", "series": "스포츠 발달", "episode": 1},
    {"title": "운동 처음 시작했다가 한 달 만에 포기하는 사람들의 공통점", "keyword": "beginner exercise first month principles", "img_keyword": "beginner workout", "sport": "공통", "series": "운동 입문", "episode": 1},
    {"title": "다이어트와 근육 증가를 동시에 한다는 게 가능한 일일까요", "keyword": "body recomposition fat loss muscle gain", "img_keyword": "body recomposition", "sport": "공통", "series": "운동 입문", "episode": 2},
    # 가동성 사슬
    {"title": "발목이 굳으면 무릎까지 망가지는 이유... 연결고리를 아세요?", "keyword": "soccer ankle mobility knee injury prevention", "img_keyword": "ankle mobility", "sport": "축구", "series": "가동성 사슬", "episode": 1},
    {"title": "골반이 틀어지면 허리 운동이 왜 소용없는지 아시나요", "keyword": "pelvic tilt lumbar stabilization biomechanics", "img_keyword": "pelvic balance", "sport": "신체균형", "series": "가동성 사슬", "episode": 2},
    {"title": "벤치프레스할 때 어깨가 아픈 이유... 등이 굳어있기 때문입니다", "keyword": "thoracic mobility shoulder impingement bench press", "img_keyword": "bench press shoulder", "sport": "유연성", "series": "가동성 사슬", "episode": 3},
    {"title": "고관절이 막힌 투수들이 구속을 잃는 해부학적 이유", "keyword": "hip rotation baseball pitching velocity anatomy", "img_keyword": "hip rotation pitcher", "sport": "야구", "series": "가동성 사슬", "episode": 4},
    {"title": "발 아치가 무너지면 상체 밸런스까지 무너지는 도미노 원리", "keyword": "foot arch collapse upper body balance chain", "img_keyword": "foot arch balance", "sport": "해부학", "series": "가동성 사슬", "episode": 5},
    # 에너지 과학
    {"title": "HIIT 할 때 왜 처음 1분이 제일 힘든지 아세요?", "keyword": "ATP-PC system lactate threshold HIIT physiology", "img_keyword": "HIIT training", "sport": "생리학", "series": "에너지 과학", "episode": 1},
    {"title": "경기 전날 밥을 많이 먹으면 정말 더 잘 뛸 수 있을까요", "keyword": "carbohydrate loading glycogen VO2max performance", "img_keyword": "carbohydrate loading", "sport": "영양", "series": "에너지 과학", "episode": 2},
    {"title": "근육통이 심할수록 잠을 더 자야 하는 과학적 이유", "keyword": "DOMS growth hormone sleep muscle protein synthesis", "img_keyword": "muscle recovery sleep", "sport": "생리학", "series": "에너지 과학", "episode": 3},
    {"title": "지방이 잘 타는 심박수가 따로 있다는 게 사실일까요", "keyword": "fat oxidation aerobic heart rate zone science", "img_keyword": "fat burning cardio", "sport": "체력", "series": "에너지 과학", "episode": 4},
    {"title": "스트레스받으면 운동해도 소용없다는 말이 사실인 이유", "keyword": "cortisol muscle loss exercise slump physiology", "img_keyword": "stress hormone", "sport": "생리학", "series": "에너지 과학", "episode": 5},
    # 부상 잔혹사
    {"title": "왜 달리기 중에만 허벅지 뒤가 터질까... 충격적인 진실", "keyword": "hamstring eccentric contraction running biomechanics", "img_keyword": "hamstring running", "sport": "재활", "series": "부상 잔혹사", "episode": 1},
    {"title": "점프 착지 0.1초가 무릎 십자인대를 끊는 메커니즘", "keyword": "ACL injury landing mechanics gluteus medius", "img_keyword": "ACL knee injury", "sport": "역학", "series": "부상 잔혹사", "episode": 2},
    {"title": "족저근막염 아침 통증... 발바닥이 아니라 종아리가 원인입니다", "keyword": "plantar fasciitis achilles tendinopathy connection", "img_keyword": "plantar fasciitis", "sport": "물리치료", "series": "부상 잔혹사", "episode": 3},
    {"title": "테니스 엘보 치료... 손목이 아니라 어깨를 봐야 하는 이유", "keyword": "tennis elbow scapular stability physical therapy", "img_keyword": "tennis elbow", "sport": "물리치료", "series": "부상 잔혹사", "episode": 4},
    {"title": "허리 디스크 재활 중 절대로 하면 안 되는 운동들", "keyword": "lumbar disc rehabilitation avoid movements", "img_keyword": "lumbar disc", "sport": "재활", "series": "부상 잔혹사", "episode": 5},
    # 오피스 애슬리트
    {"title": "하루 8시간 앉아있으면 운동선수도 부상 위험이 높아지는 이유", "keyword": "forward head posture rotator cuff injury pitcher", "img_keyword": "neck posture office", "sport": "신체균형", "series": "오피스 애슬리트", "episode": 1},
    {"title": "하루 종일 앉아있는 직장인이 스쿼트하면 허리를 다치는 이유", "keyword": "transverse abdominis core squat back pain", "img_keyword": "core squat", "sport": "근육학", "series": "오피스 애슬리트", "episode": 2},
    {"title": "의자에 오래 앉으면 엉덩이 근육이 까먹어버린다는 게 사실입니다", "keyword": "psoas muscle gluteal amnesia reciprocal inhibition", "img_keyword": "hip flexor psoas", "sport": "근육학", "series": "오피스 애슬리트", "episode": 3},
    {"title": "하루 8시간 앉아있으면 햄스트링이 단단해지는 진짜 이유", "keyword": "sitting posture hamstring flexibility physiology", "img_keyword": "sitting hamstring", "sport": "유연성", "series": "오피스 애슬리트", "episode": 4},
    # 엘리트 마인드
    {"title": "압박 상황에서 집중력이 올라가는 사람과 무너지는 사람의 차이", "keyword": "focus under pressure attentional focus brain waves", "img_keyword": "athlete concentration", "sport": "심리", "series": "엘리트 마인드", "episode": 1},
    {"title": "머릿속으로만 연습해도 근육이 반응한다는 게 사실일까요", "keyword": "mental imagery mirror neurons neuromuscular activation", "img_keyword": "mental visualization", "sport": "심리", "series": "엘리트 마인드", "episode": 2},
    {"title": "경기 전 긴장감... 없애려 하면 더 떨리는 이유가 있습니다", "keyword": "pre-game anxiety cognitive reappraisal sports", "img_keyword": "athlete pregame", "sport": "심리", "series": "엘리트 마인드", "episode": 3},
    {"title": "슬럼프에서 빠져나오지 못하는 사람들이 공통적으로 하는 실수", "keyword": "sports slump recovery 3 steps psychology", "img_keyword": "sports motivation", "sport": "심리", "series": "엘리트 마인드", "episode": 4},
    {"title": "운동 중독자들이 놓치는 치명적 신호... 도파민이 당신을 배신할 때", "keyword": "exercise intensity dopamine overtraining mental", "img_keyword": "overtraining fatigue", "sport": "스포츠의학", "series": "엘리트 마인드", "episode": 5},
    # 통증 케어
    {"title": "물리치료사들이 절대 먼저 말 안 해주는 어깨 통증의 진짜 원인", "keyword": "shoulder pain serratus anterior weakness", "img_keyword": "shoulder pain relief", "sport": "물리치료", "series": "통증 케어", "episode": 1},
    {"title": "계단 내려갈 때 무릎 앞쪽이 찌릿하다면... 이것을 확인하세요", "keyword": "knee pain stairs patellar tendinitis", "img_keyword": "knee pain", "sport": "물리치료", "series": "통증 케어", "episode": 2},
    {"title": "발목을 자주 삐는 사람들이 공통적으로 훈련하지 않는 감각", "keyword": "ankle sprain proprioception training", "img_keyword": "ankle stability", "sport": "물리치료", "series": "통증 케어", "episode": 3},
    {"title": "목 디스크 없는데 팔이 저리다면... 이 증후군을 아시나요", "keyword": "thoracic outlet syndrome arm numbness", "img_keyword": "neck shoulder pain", "sport": "물리치료", "series": "통증 케어", "episode": 4},
    {"title": "허리 아픈 사람이 하면 오히려 더 나빠지는 스트레칭들", "keyword": "lower back pain stretching avoid", "img_keyword": "lower back pain", "sport": "물리치료", "series": "통증 케어", "episode": 5},
    # 사무직 자세
    {"title": "하루 8시간 앉아있는 사람의 고관절이 굳는 이유와 결과", "keyword": "hip flexor tightness sitting office worker", "img_keyword": "office posture hip", "sport": "신체균형", "series": "사무직 자세", "episode": 1},
    {"title": "모니터 위치 하나가 목 통증을 만든다는 걸 아는 사람이 없습니다", "keyword": "monitor height neck pain desk setup ergonomics", "img_keyword": "desk ergonomics monitor", "sport": "신체균형", "series": "사무직 자세", "episode": 2},
    {"title": "의자에 앉는 자세 하나로 허리 통증 50%가 줄어드는 이유", "keyword": "sitting posture lower back pain office chair", "img_keyword": "sitting posture office", "sport": "신체균형", "series": "사무직 자세", "episode": 3},
    {"title": "재택근무 이후 목 어깨가 더 나빠진 사람들의 공통된 실수", "keyword": "work from home neck shoulder stretch routine", "img_keyword": "neck stretch office", "sport": "신체균형", "series": "사무직 자세", "episode": 4},
    {"title": "하루 종일 타이핑해도 손목이 안 아픈 사람들이 하는 것", "keyword": "wrist pain typing keyboard ergonomics", "img_keyword": "wrist pain keyboard", "sport": "물리치료", "series": "사무직 자세", "episode": 5},
    # 코어 강화
    {"title": "플랭크를 매일 해도 허리가 아픈 이유... 호흡이 문제였습니다", "keyword": "core weakness back pain transverse abdominis multifidus", "img_keyword": "core strength back", "sport": "근육학", "series": "코어 강화", "episode": 1},
    {"title": "코어 운동 열심히 해도 효과 없는 사람들이 놓친 것", "keyword": "plank core activation breathing technique", "img_keyword": "plank exercise core", "sport": "근육학", "series": "코어 강화", "episode": 2},
    {"title": "뱃살 있는 사람이 코어 운동을 어디서부터 시작해야 할까요", "keyword": "belly fat core training beginner progression", "img_keyword": "core workout beginner", "sport": "근육학", "series": "코어 강화", "episode": 3},
    {"title": "허리 재활에 데드버그가 좋다는 이유... 해본 사람은 압니다", "keyword": "dead bug exercise lumbar rehabilitation core", "img_keyword": "dead bug core exercise", "sport": "재활", "series": "코어 강화", "episode": 4},
    {"title": "코어 없이 스쿼트 하면 생기는 일들... 경험담이 있습니다", "keyword": "core stability squat lower back knee pain", "img_keyword": "squat core stability", "sport": "근육학", "series": "코어 강화", "episode": 5},
    # 밸런스 소도구
    {"title": "밸런스 패드 위에서 10초를 못 서면... 지금 당장 시작해야 합니다", "keyword": "balance pad ankle knee hip stability training", "img_keyword": "balance pad training", "sport": "체력", "series": "밸런스 소도구", "episode": 1},
    {"title": "폼롤러 아무 데나 굴리면 안 되는 이유... 이 부위는 절대 금지", "keyword": "foam roller technique correct usage avoid areas", "img_keyword": "foam roller technique", "sport": "유연성", "series": "밸런스 소도구", "episode": 2},
    {"title": "보수볼 운동이 단순히 균형 잡기가 아닌 이유", "keyword": "bosu ball core balance science effectiveness", "img_keyword": "bosu ball exercise", "sport": "체력", "series": "밸런스 소도구", "episode": 3},
    {"title": "짐볼 하나로 허리 재활부터 근력까지 되는 운동 5가지", "keyword": "stability ball back strengthening exercise rehabilitation", "img_keyword": "stability ball back exercise", "sport": "재활", "series": "밸런스 소도구", "episode": 4},
    {"title": "슬라이딩 디스크로 코어와 하체를 동시에 잡는 루틴", "keyword": "sliding disc core lower body exercise routine", "img_keyword": "sliding disc exercise", "sport": "체력", "series": "밸런스 소도구", "episode": 5},
    # 관절 보호
    {"title": "무릎 보호대... 잘못 고르면 오히려 근육이 약해집니다", "keyword": "knee brace selection pain type guide", "img_keyword": "knee brace support", "sport": "스포츠의학", "series": "관절 보호", "episode": 1},
    {"title": "발목 보호대가 오히려 독이 되는 사람이 있습니다", "keyword": "ankle brace when to use avoid muscle weakness", "img_keyword": "ankle brace support", "sport": "스포츠의학", "series": "관절 보호", "episode": 2},
    {"title": "손목 보호대만 차면 손목이 더 약해지는 이유", "keyword": "wrist support brace strengthening exercise", "img_keyword": "wrist support exercise", "sport": "스포츠의학", "series": "관절 보호", "episode": 3},
    {"title": "테이핑 vs 보호대... 상황에 따라 다르게 써야 하는 이유", "keyword": "taping vs brace difference when to use sports", "img_keyword": "sports taping", "sport": "스포츠의학", "series": "관절 보호", "episode": 4},
    # 홈트 솔루션
    {"title": "기구 없이 집에서 30분... 헬스장보다 효과 있는 루틴이 있습니다", "keyword": "home workout no equipment full body strength routine", "img_keyword": "home workout", "sport": "공통", "series": "홈트 솔루션", "episode": 1},
    {"title": "요가 매트 하나로 허리 통증을 잡은 사람들의 루틴", "keyword": "yoga mat lower back pain relief routine", "img_keyword": "yoga mat back exercise", "sport": "재활", "series": "홈트 솔루션", "episode": 2},
    {"title": "밴드 하나로 어깨부터 등까지... 헬스장 가기 싫을 때 쓰는 루틴", "keyword": "resistance band upper body shoulder back exercise", "img_keyword": "resistance band exercise", "sport": "근육학", "series": "홈트 솔루션", "episode": 3},
    {"title": "아침 10분이 하루 종일 자세를 바꾸는 이유", "keyword": "morning routine posture improvement daily habit", "img_keyword": "morning stretch routine", "sport": "신체균형", "series": "홈트 솔루션", "episode": 4},
    {"title": "퇴근 후 15분... 굳어있는 몸을 푸는 가장 효율적인 방법", "keyword": "foam roller massage ball recovery evening routine", "img_keyword": "foam roller recovery", "sport": "유연성", "series": "홈트 솔루션", "episode": 5},
    # 체형 교정 심화
    {"title": "O자 다리를 만드는 진짜 원인... 다리가 아니라 엉덩이입니다", "keyword": "bow legs hip external rotation correction cause", "img_keyword": "bow legs correction", "sport": "신체균형", "series": "체형 교정 심화", "episode": 1},
    {"title": "새우등 교정... 등을 펴려고 하면 오히려 더 나빠지는 이유", "keyword": "kyphosis correction thoracic spine pectoral stretch", "img_keyword": "posture correction back", "sport": "신체균형", "series": "체형 교정 심화", "episode": 2},
    {"title": "짝다리 짚는 습관... 10년 후 몸에 어떤 일이 생길까요", "keyword": "weight shifting habit pelvic imbalance spine", "img_keyword": "posture balance standing", "sport": "신체균형", "series": "체형 교정 심화", "episode": 3},
    {"title": "발 모양이 온몸의 체형을 결정한다는 게 사실입니까?", "keyword": "overpronation supination foot correction posture", "img_keyword": "foot pronation correction", "sport": "신체균형", "series": "체형 교정 심화", "episode": 4},
    {"title": "골반이 앞으로 기울어진 사람들이 배가 나오는 진짜 이유", "keyword": "anterior pelvic tilt correction psoas abdominal", "img_keyword": "pelvic tilt exercise", "sport": "신체균형", "series": "체형 교정 심화", "episode": 5},
]

USED_TOPICS_FILE = "used_topics.json"
SERIES_LINKS_FILE = "series_links.json"


def load_series_links():
    try:
        with open(SERIES_LINKS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_series_link(series, episode, title, url):
    links = load_series_links()
    if series not in links:
        links[series] = {}
    links[series][str(episode)] = {"title": title, "url": url}
    try:
        with open(SERIES_LINKS_FILE, "w") as f:
            json.dump(links, f, ensure_ascii=False)
        print("[시리즈링크] 저장 완료: " + series + " " + str(episode) + "편")
    except Exception as e:
        print("[시리즈링크] 저장 실패: " + str(e))


def get_series_nav_html(topic):
    series = topic.get("series", "")
    episode = topic.get("episode", 1)
    if not series:
        return ""
    links = load_series_links()
    series_data = links.get(series, {})
    prev_html = ""
    next_html = ""
    prev_ep = str(episode - 1)
    if prev_ep in series_data:
        prev = series_data[prev_ep]
        prev_html = (
            '<a href="' + prev["url"] + '" style="display:flex;align-items:center;'
            'text-decoration:none;color:#1565c0;font-size:14px;font-weight:600;">'
            '◀ 이전편: ' + prev["title"] + '</a>'
        )
    next_ep = str(episode + 1)
    if next_ep in series_data:
        nxt = series_data[next_ep]
        next_html = (
            '<a href="' + nxt["url"] + '" style="display:flex;align-items:center;'
            'text-decoration:none;color:#1565c0;font-size:14px;font-weight:600;">'
            '다음편: ' + nxt["title"] + ' ▶</a>'
        )
    if not prev_html and not next_html:
        return ""
    html = (
        '<div style="background:#f0f4ff;border:2px solid #1565c0;border-radius:12px;'
        'padding:20px 24px;margin:40px 0;">'
        '<p style="font-weight:700;font-size:15px;color:#1565c0;margin-bottom:14px;">'
        '📚 ' + series + ' 시리즈 더 보기</p>'
        '<div style="display:flex;flex-direction:column;gap:10px;">'
    )
    if prev_html:
        html += '<div>' + prev_html + '</div>'
    if next_html:
        html += '<div>' + next_html + '</div>'
    html += '</div></div>\n'
    return html


def load_used_topics():
    try:
        with open(USED_TOPICS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_used_topic(title):
    used = load_used_topics()
    used.append(title)
    if len(used) > 80:
        used = used[-80:]
    try:
        with open(USED_TOPICS_FILE, "w") as f:
            json.dump(used, f, ensure_ascii=False)
    except Exception as e:
        print("[중복방지] 저장 실패: " + str(e))


def pick_topic():
    used = load_used_topics()
    available = [t for t in TOPICS if t["title"] not in used]
    if not available:
        print("[중복방지] 모든 주제 사용 완료, 초기화합니다.")
        available = TOPICS
        try:
            with open(USED_TOPICS_FILE, "w") as f:
                json.dump([], f)
        except Exception:
            pass
    topic = random.choice(available)
    save_used_topic(topic["title"])
    return topic


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
            "max_tokens": 6000,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=300
    )
    if response.status_code != 200:
        raise Exception("Claude 오류: " + str(response.status_code) + " " + response.text[:200])
    return response.json()["content"][0]["text"]


def generate_post():
    topic = pick_topic()
    print("[글 생성] 주제: " + topic["title"])

    series_info = ""
    if topic["episode"] > 1:
        series_info = (
            "이 글은 " + topic["series"] + " 시리즈 " + str(topic["episode"]) + "편입니다. "
            + "이전 편보다 심화된 내용을 다루세요.\n\n"
        )

    prompt = (
        "당신은 10년 경력의 스포츠 트레이너이자 블로거예요.\n"
        "운동 현장에서 직접 보고 경험한 것들을 글로 풀어내는 스타일이고,\n"
        "어려운 스포츠 과학 지식을 누구나 이해할 수 있게 전달하는 게 특기예요.\n"
        "한국어만 사용하세요. 외국 문자 절대 금지.\n\n"
        + series_info
        + "## 제목 활용 방법\n"
        "주어진 제목은 독자의 궁금증을 자극하는 후킹 문장입니다.\n"
        "글 내용은 반드시 이 제목의 궁금증을 완벽하게 해소해주어야 해요.\n"
        "제목에서 던진 질문이나 주장을 글 안에서 명확히 답해주세요.\n\n"
        "## 글쓰기 핵심 원칙\n"
        "1. 현장 사례로 시작하세요. 실제 트레이너가 겪은 에피소드로 자연스럽게 끌어들이세요.\n"
        "2. '나도 몰랐던 사실'을 밝혀주는 구성으로 쓰세요. 독자가 '어, 이거 나도 오해했는데'라고 느끼게.\n"
        "3. 전문 지식은 반드시 일상 비유로 풀어주세요. 예: '근막은 몸을 감싸는 비닐랩 같은 것'\n"
        "4. 각 소제목 아래는 배경 → 과학적 설명 → 실제 사례 → 해결책 순으로 전개하세요.\n"
        "5. 마지막에 독자가 내일 당장 해볼 수 있는 구체적인 행동 하나를 제시하세요.\n\n"
        "## 문단 작성 규칙\n"
        "각 문단은 4~6문장 이상 하나의 덩어리로 묶어 작성하세요.\n"
        "한두 문장 쓰고 줄바꿈 금지.\n\n"
        "## 소제목 규칙\n"
        "소제목은 [이모지 소제목내용] 형식, 이모지는 앞에만 1개.\n"
        "소제목에 반드시 구체적 수치나 데이터 포함.\n"
        "예시 (좋음): [🦴 골반이 1도 틀어지면 허리 압력이 3배 증가합니다]\n"
        "예시 (나쁨): [🦴 골반의 과학 🦴]\n\n"
        "## 반드시 포함할 요소\n"
        "핵심 키워드: ##키워드## 형식으로 글의 핵심 개념 하나를 크게 던지고 풀어쓰세요.\n"
        "소제목: 위 규칙대로 최소 4개 이상.\n"
        "훈련 표: [TABLE_START]와 [TABLE_END] 사이에 작성.\n"
        "형식: 훈련명|세트|횟수|휴식|작용 근육|효과\n"
        "[TABLE_START]\n"
        "훈련명|세트|횟수|휴식|작용 근육|효과\n"
        "예시|3|12회|60초|대퇴사두근|하체 강화\n"
        "[TABLE_END]\n"
        "핵심 요약: [SUMMARY_START]와 [SUMMARY_END] 사이에 3줄 (수치 포함).\n\n"
        "분량: 4000자~6000자. 깊이 있게 충분히 써주세요.\n"
        "AI 티 나는 나열식 표현 금지. 친근한 존댓말 필수.\n\n"
        "카테고리: " + topic["sport"] + "\n"
        "주제 제목: " + topic["title"] + "\n\n"
        "출력 형식:\n"
        "제목: (주어진 주제 제목을 더욱 흡입력 있게 다듬은 제목)\n"
        "---\n"
        "(본문)"
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


def get_images_unsplash(keyword, count=3):
    if not UNSPLASH_ACCESS_KEY:
        return []
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query": keyword,
                "per_page": 10,
                "page": random.randint(1, 3),
                "orientation": "landscape",
                "client_id": UNSPLASH_ACCESS_KEY
            },
            timeout=10
        )
        if response.status_code == 200:
            images = []
            for photo in response.json().get("results", []):
                images.append({
                    "url": photo["urls"]["regular"],
                    "alt": photo.get("alt_description", keyword) or keyword,
                    "author": photo["user"]["name"],
                    "author_url": photo["user"]["links"]["html"],
                    "source": "Unsplash"
                })
            random.shuffle(images)
            return images[:count]
    except Exception as e:
        print("[Unsplash 오류] " + str(e))
    return []


def get_images_pexels(keyword, count=3):
    pexels_key = os.environ.get("PEXELS_API_KEY", "")
    if not pexels_key:
        return []
    try:
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": pexels_key},
            params={"query": keyword, "per_page": count, "orientation": "landscape"},
            timeout=10
        )
        if response.status_code == 200:
            images = []
            for photo in response.json().get("photos", []):
                images.append({
                    "url": photo["src"]["large"],
                    "alt": photo.get("alt", keyword) or keyword,
                    "author": photo["photographer"],
                    "author_url": photo["photographer_url"],
                    "source": "Pexels"
                })
            return images
    except Exception as e:
        print("[Pexels 오류] " + str(e))
    return []


def get_images_pixabay(keyword, count=3):
    pixabay_key = os.environ.get("PIXABAY_API_KEY", "")
    if not pixabay_key:
        return []
    try:
        response = requests.get(
            "https://pixabay.com/api/",
            params={
                "key": pixabay_key,
                "q": keyword,
                "image_type": "photo",
                "orientation": "horizontal",
                "per_page": count,
                "safesearch": "true"
            },
            timeout=10
        )
        if response.status_code == 200:
            images = []
            for hit in response.json().get("hits", []):
                images.append({
                    "url": hit["webformatURL"],
                    "alt": keyword,
                    "author": hit["user"],
                    "author_url": "https://pixabay.com/users/" + hit["user"] + "-" + str(hit["user_id"]),
                    "source": "Pixabay"
                })
            return images
    except Exception as e:
        print("[Pixabay 오류] " + str(e))
    return []


def get_images(keyword, count=3):
    print("[이미지 검색] 키워드: " + keyword)
    images = get_images_unsplash(keyword, count)
    if images:
        print("[이미지] Unsplash " + str(len(images)) + "장")
        return images
    images = get_images_pexels(keyword, count)
    if images:
        print("[이미지] Pexels " + str(len(images)) + "장")
        return images
    images = get_images_pixabay(keyword, count)
    if images:
        print("[이미지] Pixabay " + str(len(images)) + "장")
        return images
    print("[이미지] 모든 소스 실패")
    return []


def make_table_html(table_text):
    rows = [r.strip() for r in table_text.strip().split("\n") if r.strip()]
    if not rows:
        return ""
    html = '<div style="overflow-x:auto;margin:24px 0;">'
    html += '<table style="width:100%;border-collapse:collapse;font-size:15px;">'
    for i, row in enumerate(rows):
        cols = row.split("|")
        html += "<tr>"
        for col in cols:
            if i == 0:
                html += '<th style="background:#1565c0;color:#fff;padding:10px 14px;text-align:center;border:1px solid #1565c0;">' + col.strip() + "</th>"
            else:
                bg = "#f5f8ff" if i % 2 == 0 else "#ffffff"
                html += '<td style="padding:9px 14px;text-align:center;border:1px solid #dde3f0;background:' + bg + ';">' + col.strip() + "</td>"
        html += "</tr>"
    html += "</table></div>\n"
    return html


def make_summary_html(summary_text):
    lines = [l.strip() for l in summary_text.strip().split("\n") if l.strip()]
    html = '<div style="background:#e8f4fd;border-left:5px solid #1565c0;border-radius:8px;padding:20px 24px;margin:28px 0;">'
    html += '<p style="font-weight:700;font-size:17px;color:#1565c0;margin-bottom:12px;">📌 핵심 요약</p>'
    for line in lines:
        html += '<p style="margin:6px 0;font-size:15px;color:#333;">✅ ' + line + "</p>"
    html += "</div>\n"
    return html


def make_image_html(img, margin_top="0"):
    source = img.get("source", "Unsplash")
    html = '<div style="text-align:center;margin:30px 0;margin-top:' + margin_top + ';">'
    html += '<img src="' + img["url"] + '" alt="' + img["alt"] + '" style="max-width:100%;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.12);"/>'
    html += '<p style="font-size:12px;color:#999;margin-top:8px;">Photo by <a href="' + img["author_url"] + '" style="color:#999;">' + img["author"] + '</a> on ' + source + '</p>'
    html += "</div>\n"
    return html


def body_to_html(body, images, topic):
    sport_emoji = SPORT_EMOJI.get(topic["sport"], "🏆")

    series_badge = ""
    if topic.get("series"):
        series_badge = (
            '<div style="display:inline-block;background:#1565c0;color:#fff;'
            'font-size:13px;padding:5px 14px;border-radius:20px;margin-bottom:20px;font-weight:600;">'
            + sport_emoji + " " + topic["series"] + " " + str(topic["episode"]) + "편</div>\n"
        )

    html = series_badge

    if len(images) >= 1:
        html += make_image_html(images[0])

    table_pattern = re.compile(r'\[TABLE_START\](.*?)\[TABLE_END\]', re.DOTALL)
    summary_pattern = re.compile(r'\[SUMMARY_START\](.*?)\[SUMMARY_END\]', re.DOTALL)

    table_match = table_pattern.search(body)
    summary_match = summary_pattern.search(body)

    table_html = make_table_html(table_match.group(1)) if table_match else ""
    summary_html = make_summary_html(summary_match.group(1)) if summary_match else ""

    clean_body = table_pattern.sub("[TABLE_PLACEHOLDER]", body)
    clean_body = summary_pattern.sub("[SUMMARY_PLACEHOLDER]", clean_body)

    headings = re.findall(r'\[([^\]]+)\]', clean_body)
    headings = [h for h in headings if h not in ["TABLE_PLACEHOLDER", "SUMMARY_PLACEHOLDER"]]
    if headings:
        toc = '<div style="background:#f8f9ff;border:1px solid #dde3f0;border-radius:10px;padding:20px 24px;margin:24px 0;">'
        toc += '<p style="font-weight:700;font-size:15px;color:#1565c0;margin-bottom:12px;">📋 목차</p>'
        toc += '<ol style="margin:0;padding-left:20px;">'
        for h in headings:
            clean_h = re.sub(r'^[^\w가-힣]+', '', h).strip()
            toc += '<li style="margin:6px 0;font-size:15px;color:#444;line-height:1.6;">' + clean_h + '</li>'
        toc += '</ol></div>\n'
        html += toc

    keyword_pattern = re.compile(r'##(.+?)##')
    def replace_keyword(m):
        return (
            '<span style="display:inline-block;font-size:28px;font-weight:900;'
            'color:#1565c0;letter-spacing:-0.5px;margin:20px 0 8px 0;'
            'border-bottom:3px solid #1565c0;padding-bottom:4px;">'
            + m.group(1) + '</span>'
        )

    paragraphs = clean_body.split("\n")
    mid = len(paragraphs) // 2
    image2_inserted = False
    para_count = 0

    for i, para in enumerate(paragraphs):
        if not para.strip():
            continue
        if para.strip() == "[TABLE_PLACEHOLDER]":
            html += table_html
            continue
        if para.strip() == "[SUMMARY_PLACEHOLDER]":
            html += summary_html
            continue
        if para.startswith("[") and "]" in para:
            heading = para.strip("[]").strip()
            html += (
                '<h2 style="margin-top:48px;margin-bottom:16px;font-size:22px;font-weight:700;'
                'background:linear-gradient(90deg,#1565c0,#1976d2);'
                'color:#fff;padding:12px 20px;border-radius:8px;">'
                + heading + "</h2>\n"
            )
            continue
        if len(para.strip()) > 1 and para.strip()[0].isdigit() and para.strip()[1] in [".", ")"]:
            html += (
                '<div style="display:flex;align-items:flex-start;margin:10px 0;padding:12px 16px;'
                'background:#f5f8ff;border-radius:8px;">'
                '<span style="color:#1565c0;font-weight:700;margin-right:12px;font-size:16px;">'
                + para.strip()[0] + '.</span>'
                '<span style="color:#333;font-size:16px;line-height:1.8;">'
                + para.strip()[2:].strip() + '</span></div>\n'
            )
            continue
        para_count += 1
        processed = keyword_pattern.sub(replace_keyword, para.strip())
        if processed != para.strip():
            html += '<div style="margin:28px 0 12px 0;">' + processed + '</div>\n'
        elif para_count % 4 == 0 and len(para.strip()) > 30:
            html += (
                '<div style="border-left:4px solid #1565c0;padding:14px 20px;margin:20px 0;'
                'background:#f0f4ff;border-radius:0 8px 8px 0;">'
                '<p style="margin:0;font-size:16px;line-height:1.9;color:#1a1a2e;font-weight:500;">'
                + para.strip() + '</p></div>\n'
            )
        else:
            html += (
                '<p style="margin:0 0 20px 0;line-height:2.0;font-size:16px;color:#333;text-align:justify;">'
                + para.strip() + '</p>\n'
            )
        if i >= mid and not image2_inserted and len(images) >= 2:
            html += make_image_html(images[1], margin_top="20px")
            image2_inserted = True

    if len(images) >= 3:
        html += make_image_html(images[2], margin_top="20px")

    html += get_series_nav_html(topic)
    return html


def request_google_indexing(post_url):
    import json as json_lib, time, base64
    service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if not service_account_json:
        print("[색인] GOOGLE_SERVICE_ACCOUNT_JSON 없음 - 건너뜀")
        return
    try:
        sa_info = json_lib.loads(service_account_json)
        now = int(time.time())
        header = base64.urlsafe_b64encode(
            json_lib.dumps({"alg": "RS256", "typ": "JWT"}).encode()
        ).rstrip(b"=").decode()
        payload_data = {
            "iss": sa_info["client_email"],
            "scope": "https://www.googleapis.com/auth/indexing",
            "aud": "https://oauth2.googleapis.com/token",
            "exp": now + 3600,
            "iat": now
        }
        payload_b64 = base64.urlsafe_b64encode(
            json_lib.dumps(payload_data).encode()
        ).rstrip(b"=").decode()
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
        private_key = serialization.load_pem_private_key(
            sa_info["private_key"].encode(), password=None
        )
        sign_input = (header + "." + payload_b64).encode()
        signature = private_key.sign(sign_input, padding.PKCS1v15(), hashes.SHA256())
        jwt_token = header + "." + payload_b64 + "." + base64.urlsafe_b64encode(signature).rstrip(b"=").decode()
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt_token},
            timeout=10
        )
        if token_response.status_code != 200:
            print("[색인] 토큰 발급 실패: " + token_response.text[:200])
            return
        access_token = token_response.json().get("access_token", "")
        index_response = requests.post(
            "https://indexing.googleapis.com/v3/urlNotifications:publish",
            headers={"Authorization": "Bearer " + access_token, "Content-Type": "application/json"},
            json={"url": post_url, "type": "URL_UPDATED"},
            timeout=10
        )
        if index_response.status_code == 200:
            print("[색인] 구글 색인 요청 완료! ✅ " + post_url)
        else:
            print("[색인] 색인 요청 실패: " + index_response.text[:200])
    except Exception as e:
        print("[색인 오류] " + str(e))


def send_telegram(title, post_url, topic):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    sport_emoji = SPORT_EMOJI.get(topic["sport"], "🏆")
    message = sport_emoji + " 새 포스팅\n\n📌 " + title + "\n\n🔗 " + post_url
    try:
        response = requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
            timeout=10
        )
        if response.status_code == 200:
            print("[텔레그램] 공유 성공!")
        else:
            print("[텔레그램] 실패: " + response.text[:200])
    except Exception as e:
        print("[텔레그램 오류] " + str(e))


def send_facebook(title, post_url, topic):
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        return
    sport_emoji = SPORT_EMOJI.get(topic["sport"], "🏆")
    message = sport_emoji + " " + title + "\n\n자세히 읽기 👉 " + post_url
    try:
        response = requests.post(
            "https://graph.facebook.com/v19.0/" + FACEBOOK_PAGE_ID + "/feed",
            data={"message": message, "link": post_url, "access_token": FACEBOOK_ACCESS_TOKEN},
            timeout=10
        )
        if response.status_code == 200:
            print("[페이스북] 공유 성공!")
        else:
            print("[페이스북] 실패: " + response.text[:200])
    except Exception as e:
        print("[페이스북 오류] " + str(e))


def post_to_blogger(post_data, images, retry=2):
    print("\n[Blogger] 포스팅 시작...")
    topic = post_data["topic"]
    labels = [topic["sport"], topic["series"]]

    for attempt in range(1, retry + 2):
        try:
            access_token = get_access_token()
            body_html = body_to_html(post_data["body"], images, topic)
            url = "https://www.googleapis.com/blogger/v3/blogs/" + BLOG_ID + "/posts?isDraft=false"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-Type": "application/json"
            }
            payload = {
                "kind": "blogger#post",
                "title": post_data["title"],
                "content": body_html,
                "labels": labels,
                "status": "LIVE"
            }
            print("[시도 " + str(attempt) + "] 제목: " + post_data["title"])
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            print("[응답] 상태코드: " + str(response.status_code))
            if response.status_code == 200:
                result = response.json()
                post_url = result.get("url", "")
                print("\n발행 완료!")
                print("   링크: " + post_url)
                save_series_link(
                    topic.get("series", ""),
                    topic.get("episode", 1),
                    post_data["title"],
                    post_url
                )
                request_google_indexing(post_url)
                send_telegram(post_data["title"], post_url, topic)
                send_facebook(post_data["title"], post_url, topic)
                return True
            else:
                print("실패: " + response.text[:300])
                if attempt <= retry:
                    print("[재시도] " + str(attempt) + "번째 재시도 중...")
        except Exception as e:
            print("[오류] " + str(e))
            if attempt <= retry:
                print("[재시도] " + str(attempt) + "번째 재시도 중...")
    return False


if __name__ == "__main__":
    print("=" * 50)
    print("AutoBlog Sports Publisher - Claude Edition")
    print("실행 시각: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)
    try:
        post = generate_post()
        images = get_images(post["topic"].get("img_keyword", post["topic"]["keyword"]), count=3)
        post_to_blogger(post, images)
        print("\n모든 작업 완료!")
    except Exception as e:
        print("\n오류 발생: " + str(e))
        import traceback
        traceback.print_exc()
        exit(1)
