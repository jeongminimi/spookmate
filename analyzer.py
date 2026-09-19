import re

# 플루치크 24대 혼합정서 사전
PLUTCHIK_24_DYADS = {
    "OPTIMISM": {
        "tag": "낙관/희망",
        "ko": "낙관 (기대 + 기쁨)",
        "valence": 5.72,
        "arousal": 5.16,
        "keywords": [
            "낙관", "잘될", "희망", "기대", "뿌듯", "보람", "해냈", "신나", "기분좋", 
            "설레", "즐겁", "즐거", "행복", "좋았", "좋아", "만족", "최고", "힐링", 
            "재밌", "존잼", "웃김", "웃었", "웃는", "개운", "홀가분", "성공"
        ]
    },
    "DELIGHT": {
        "tag": "환희/도취",
        "ko": "환희 (기쁨 + 놀람)",
        "valence": 5.85,
        "arousal": 6.10,
        "keywords": ["대박", "환희", "짜릿", "미쳤다", "횡재", "당첨", "선물", "축제", "감격", "신세계"]
    },
    "LOVE": {
        "tag": "사랑/유대",
        "ko": "사랑 (기쁨 + 신뢰)",
        "valence": 6.10,
        "arousal": 4.20,
        "keywords": ["사랑", "감사", "고마", "따뜻", "다정", "친절", "의지", "든든", "감동", "화목", "안도"]
    },
    "PRIDE": {
        "tag": "자부심/긍지",
        "ko": "자부심 (기쁨 + 분노)",
        "valence": 5.45,
        "arousal": 5.80,
        "keywords": ["자부심", "해냈다", "이겼다", "자랑", "당당", "극복", "뿌듯함", "인정받", "증명"]
    },
    "OUTRAGE": {
        "tag": "격분/억울",
        "ko": "격분 (놀람 + 분노)",
        "valence": 1.84,
        "arousal": 6.17,
        "keywords": ["화나", "열받", "짜증", "억울", "빡치", "무시", "부당", "천불", "꼭지", "개판", "개빡"]
    },
    "ANXIETY": {
        "tag": "불안/초조",
        "ko": "불안/초조 (기대 + 공포)",
        "valence": 2.51,
        "arousal": 4.88,
        "keywords": ["불안", "걱정", "망하", "초조", "어쩌지", "무서", "두려", "큰일", "시험", "면접"]
    },
    "DESPAIR": {
        "tag": "절망/무기력",
        "ko": "절망 (공포 + 슬픔)",
        "valence": 1.45,
        "arousal": 4.10,
        "keywords": ["무기력", "지쳐", "포기", "끝났", "우울", "비가와서", "힘들어", "탈진", "번아웃"]
    },
    "REMORSE": {
        "tag": "후회/자책",
        "ko": "후회/자책 (슬픔 + 혐오)",
        "valence": 1.95,
        "arousal": 4.60,
        "keywords": ["후회", "자책", "내탓", "바보", "자괴감", "자조", "죄책감", "부끄럽", "쥐구멍"]
    },
    "CONTEMPT": {
        "tag": "경멸/냉소",
        "ko": "경멸/냉소 (혐오 + 분노)",
        "valence": 1.70,
        "arousal": 5.40,
        "keywords": ["한심", "꼴값", "역겹", "재수", "극혐", "경멸", "싸가지", "인성"]
    },
    "ENVY": {
        "tag": "질투/열등감",
        "ko": "질투 (슬픔 + 분노)",
        "valence": 1.80,
        "arousal": 5.60,
        "keywords": ["질투", "부러", "배아파", "비교", "박탈감", "왜나만"]
    }
}

CBT_RESTRUCTURING = {
    "OPTIMISM": "오늘의 긍정적인 기운은 내가 일궈낸 노력의 결실이다. 이 뿌듯함을 온전히 만끽하자.",
    "DELIGHT": "뜻밖의 기쁨도 인생의 소중한 선물이다. 오늘 느낀 짜릿한 환희를 마음껏 축하하자.",
    "LOVE": "나는 주변 사람들과 따뜻한 온기를 나눌 자격이 있다. 이 유대감을 소중히 기억하자.",
    "PRIDE": "스스로를 증명해 낸 내 자신이 자랑스럽다. 나의 가치와 잠재력을 신뢰하자.",
    "ANXIETY": "머릿속의 최악의 시나리오는 상상일 뿐이며, 나는 닥쳐올 상황을 차분히 해결할 힘이 있다.",
    "OUTRAGE": "상대방의 무례함은 그 사람의 문제일 뿐, 내 인격과 가치를 깎아내릴 수 없다.",
    "DESPAIR": "지금의 방전된 상태는 영원하지 않다. 오늘은 그저 충분히 쉬어야 할 휴식의 시간이다.",
    "REMORSE": "실수는 누구나 한다. 지나간 일에 매몰되지 않고 배움으로 삼아 털어내자.",
    "CONTEMPT": "타인의 부정적인 태도에 내 평정심을 내어주지 말자. 거리를 두고 내 페이스를 지키자.",
    "ENVY": "남들의 하이라이트와 나의 비하인드를 비교할 필요는 없다. 내 속도대로 내 길을 가면 된다."
}

def analyze_entry(raw_entry: str):
    POSITIVE_HINTS = ["좋", "즐", "행복", "신나", "재미", "웃", "뿌듯", "대박", "감사", "최고"]
    
    matched_dyad = None
    max_hits = 0

    for dyad, info in PLUTCHIK_24_DYADS.items():
        hits = sum(1 for kw in info["keywords"] if kw in raw_entry)
        if hits > max_hits:
            max_hits = hits
            matched_dyad = dyad

    if not matched_dyad:
        if any(h in raw_entry for h in POSITIVE_HINTS):
            matched_dyad = "OPTIMISM"
        else:
            matched_dyad = "ANXIETY"

    dyad_data = PLUTCHIK_24_DYADS[matched_dyad]
    
    situation = raw_entry.strip()
    if "때" in raw_entry:
        situation = raw_entry.split("때")[0] + " 때 발생한 사건"
    elif "했는데" in raw_entry:
        situation = raw_entry.split("했는데")[0] + " 상황"

    automatic_thought = f"'{raw_entry}' 상황에 직면하여 #{dyad_data['tag']} 정서가 활성화됨"
    alternative_thought = CBT_RESTRUCTURING.get(
        matched_dyad,
        "감정은 일시적인 기상 현상과 같아서 지나간다. 사건과 나 자신을 분리해 바라보자."
    )

    clean_text = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', raw_entry)
    tokens = [w for w in clean_text.split() if len(w) >= 2]

    return {
        "emotion_tag": dyad_data["tag"],
        "plutchik_dyad": matched_dyad,
        "plutchik_ko": dyad_data["ko"],
        "valence": dyad_data["valence"],
        "arousal": dyad_data["arousal"],
        "situation": situation,
        "automatic_thought": automatic_thought,
        "alternative_thought": alternative_thought,
        "tokens": tokens
    }