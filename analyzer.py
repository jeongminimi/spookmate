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
        "keywords": ["대박", "환희", "기쁘", "기뻤", "기뻐", "짜릿", "미쳤다", "횡재", "당첨", "선물", "축제", "감격", "신세계"]
    },
    "LOVE": {
        "tag": "사랑/유대",
        "ko": "사랑 (기쁨 + 신뢰)",
        "valence": 6.10,
        "arousal": 4.20,
        "keywords": ["사랑", "감사", "고마", "따뜻", "다정", "친절", "의지", "든든", "감동", "화목"]
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
        "keywords": ["화나", "화가", "열받", "짜증", "억울", "빡치", "무시", "부당", "천불", "꼭지", "개판", "개빡"]
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
        "keywords": ["무기력", "지쳐", "지쳤", "지치", "피곤", "피로", "포기", "끝났", "우울", "비가와서", "힘들", "탈진", "번아웃", "슬픔", "슬프", "슬펐", "울었", "눈물", "이별", "헤어", "외롭", "외로", "소외", "고립", "따돌", "버겁"]
    },
    "REMORSE": {
        "tag": "후회/자책",
        "ko": "후회/자책 (슬픔 + 혐오)",
        "valence": 1.95,
        "arousal": 4.60,
        "keywords": ["후회", "자책", "내탓", "바보", "자괴감", "자조"]
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
    },
    "HOPE": {"tag": "희망/안도", "ko": "희망 (기대 + 신뢰)", "valence": 5.10, "arousal": 2.63,
             "keywords": ["안심", "안도", "괜찮아질", "기대돼", "희망이 생", "숨통", "마음 놓", "다행"]},
    "CURIOSITY": {"tag": "호기심/탐색", "ko": "호기심 (기대 + 놀람)", "valence": 5.13, "arousal": 4.50,
                  "keywords": ["궁금", "호기심", "알아보고", "신기", "탐색", "새로운 걸", "어떻게 될까"]},
    "AWE": {"tag": "경외/감탄", "ko": "경외 (공포 + 놀람)", "valence": 3.30, "arousal": 5.20,
            "keywords": ["경외", "압도", "장엄", "소름", "경이롭", "입이 떡", "믿기지 않"]},
    "SUBMISSION": {"tag": "순응/의존", "ko": "순응 (신뢰 + 공포)", "valence": 2.40, "arousal": 3.10,
                   "keywords": ["거절 못", "따를 수밖", "눈치 보", "복종", "시키는 대로", "순응", "의존"]},
    "SENTIMENTALITY": {"tag": "그리움/감상", "ko": "감상 (신뢰 + 슬픔)", "valence": 4.27, "arousal": 3.50,
                       "keywords": ["그리워", "그립", "추억", "옛날 생각", "보고 싶", "향수", "아련"]},
    "SHAME": {"tag": "수치/창피", "ko": "수치 (공포 + 혐오)", "valence": 1.97, "arousal": 4.67,
              "keywords": ["창피", "부끄럽", "수치", "쥐구멍", "망신", "얼굴 들", "민망"]},
    "GUILT": {"tag": "죄책/미안", "ko": "죄책 (기쁨 + 공포)", "valence": 2.05, "arousal": 4.10,
              "keywords": ["죄책감", "미안해", "내 잘못", "죄 지은", "죄송", "피해 줬"]},
    "CYNICISM": {"tag": "냉소/불신", "ko": "냉소 (기대 + 혐오)", "valence": 2.70, "arousal": 3.20,
                 "keywords": ["냉소", "시큰둥", "어차피 다", "비꼬", "믿을 수 없", "가식"]},
    "UNBELIEF": {"tag": "불신/의심", "ko": "불신 (놀람 + 혐오)", "valence": 2.40, "arousal": 3.95,
                 "keywords": ["못 믿", "의심", "배신", "거짓말", "수상", "진짜라고", "말이 안 돼"]},
    "PESSIMISM": {"tag": "비관/체념", "ko": "비관 (기대 + 슬픔)", "valence": 2.43, "arousal": 3.13,
                  "keywords": ["비관", "체념", "소용없", "어차피 안", "가망없", "기대 안", "안 될 거"]},
    "AGGRESSIVENESS": {"tag": "공격/대항", "ko": "공격성 (기대 + 분노)", "valence": 2.40, "arousal": 5.45,
                       "keywords": ["맞서", "들이받", "대항", "따지고", "되갚", "복수하고", "공격"]},
    "DOMINANCE": {"tag": "주도/통제", "ko": "지배 (신뢰 + 분노)", "valence": 5.20, "arousal": 4.10,
                  "keywords": ["주도권", "통제", "내가 결정", "이끌", "주도", "장악", "리드"]},
    "MORBIDNESS": {"tag": "섬뜩/기괴", "ko": "섬뜩함 (기쁨 + 혐오)", "valence": 2.40, "arousal": 5.10,
                   "keywords": ["기괴", "섬뜩", "소름끼", "오싹", "으스스", "잔혹", "흉측"]},
    "DISAPPROVAL": {"tag": "실망/거부", "ko": "실망 (놀람 + 슬픔)", "valence": 2.45, "arousal": 3.05,
                    "keywords": ["실망", "기대했는데", "서운", "속상", "허탈", "배신감", "맥 빠", "못마땅"]}
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
    "ENVY": "남들의 하이라이트와 나의 비하인드를 비교할 필요는 없다. 내 속도대로 내 길을 가면 된다.",
    "HOPE": "지금 느끼는 안도에는 이유가 있다. 아직 모르는 미래와 이미 확인한 좋은 신호를 구분해 보자.",
    "CURIOSITY": "궁금한 마음은 새로운 것을 배우려는 신호다. 확인할 수 있는 한 가지부터 살펴보자.",
    "AWE": "압도되는 느낌을 서둘러 해석하지 않아도 된다. 지금 실제로 본 것과 떠오른 생각을 나눠 보자.",
    "SUBMISSION": "상대의 기대를 살피는 마음과 내 선택권은 함께 존재할 수 있다. 내 뜻을 한 문장으로 적어 보자.",
    "SENTIMENTALITY": "그리움은 소중했던 관계와 시간을 떠올리게 한다. 지금 필요한 위로를 스스로에게도 건네 보자.",
    "SHAME": "창피한 순간 하나가 나 전체를 설명하지는 않는다. 사건과 나 자신을 구분해 보자.",
    "GUILT": "미안한 마음이 있다면 확인된 내 몫만 살펴보자. 필요한 사과와 과한 자책은 다르다.",
    "CYNICISM": "실망한 경험이 모든 다음 일의 결론은 아니다. 지금 확인된 사실부터 다시 살펴보자.",
    "UNBELIEF": "의심이 들 때는 단정하기 전에 확인할 수 있는 근거 하나를 찾아보자.",
    "PESSIMISM": "어려운 가능성을 보는 눈도 도움이 된다. 아직 결정되지 않은 결과까지 확정하지는 말자.",
    "AGGRESSIVENESS": "맞서고 싶은 마음 뒤의 중요한 가치를 살펴보자. 안전하게 내 입장을 전할 방법을 고를 수 있다.",
    "DOMINANCE": "주도하고 싶은 마음에는 책임감이 있을 수 있다. 내가 통제할 수 있는 범위를 구분해 보자.",
    "MORBIDNESS": "섬뜩한 느낌이 남았다면 실제 위험과 떠오른 이미지를 나눠 보자.",
    "DISAPPROVAL": "기대와 달랐던 점이 무엇인지 짚어 보자. 실망한 마음을 축소할 필요는 없다."
}

def analyze_entry(raw_entry: str):
    POSITIVE_HINTS = ["좋", "즐", "행복", "신나", "재미", "웃", "뿌듯", "대박", "감사", "최고"]
    
    matched_dyad = None
    max_hits = 0

    for dyad, info in PLUTCHIK_24_DYADS.items():
        hits = sum(2 if len(kw) >= 4 else 1 for kw in info["keywords"] if kw in raw_entry)
        if hits > max_hits:
            max_hits = hits
            matched_dyad = dyad

    if not matched_dyad and any(h in raw_entry for h in POSITIVE_HINTS):
        matched_dyad = "OPTIMISM"

    # An entry without an emotion cue is not evidence of anxiety. Let the
    # matcher use its content and a neutral coordinate instead of always
    # assigning the same anxiety yokai.
    if not matched_dyad:
        clean_text = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', raw_entry)
        return {
            "emotion_tag": "감정 탐색",
            "plutchik_dyad": None,
            "plutchik_ko": None,
            "valence": 3.5,
            "arousal": 3.5,
            "situation": raw_entry.strip(),
            "automatic_thought": "아직 감정 단서를 특정하기 어려운 기록",
            "alternative_thought": "이야기 속에서 실제로 있었던 일과 지금의 마음을 천천히 살펴보자.",
            "tokens": [w for w in clean_text.split() if len(w) >= 2],
        }

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
