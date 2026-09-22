import os
from datetime import datetime, date
import math
import random
import re
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, Field

from analyzer import analyze_entry

# ==============================================================================
# 1. FastAPI 인스턴스 초기화 & CORS 설정
# ==============================================================================
app = FastAPI(
    title="SpookMate API",
    description="플루치크 24대 혼합정서 모델 & 동서양 73종 요괴 설화 매칭 엔진 (Supabase Ver.)",
    version="1.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # GitHub Pages 및 로컬 5500 등 모든 포트 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# 2. 데이터베이스 연결 설정 (Supabase PostgreSQL)
# ==============================================================================
SUPABASE_DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres.aywtiggvataezyxeuexe:tkfkdgo91!SPDB@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
)


def get_db():
    # RealDictCursor를 기본 적용하여 딕셔너리 형태로 결과 행 반환
    return psycopg2.connect(SUPABASE_DB_URL, cursor_factory=RealDictCursor)


# ==============================================================================
# 스푹메이트(SpookMate) 정서별 맞장구 프리셋
# ==============================================================================
SPOOKMATE_RESPONSES = {
    "OUTRAGE": [
        (
            "야 인간아, 네 속에서 시커먼 연기 난다! 널 긁은 인간은 인성에 하자"
            " 있는 거니까 걔 때문에 네 속 태우지 마라. 그 끓어넘치는 분노는 내가"
            " 남김없이 씹어먹었으니 주먹 풀고 라면이나 끓여와."
        ),
        (
            "우걱우걱... 캬! 오늘 네 하소연은 아주 매콤한 불닭맛 특식이네. 널"
            " 화나게 한 놈 면상 대신 내가 네 분노 찌꺼기를 잘근잘근 씹어줬으니"
            " 넌 발 닦고 푹 자라."
        ),
        (
            "방바닥에 누워있는데 어디서 타는 냄새 난다 했다. 네 속 뒤집어진"
            " 거였냐? 억울해 죽겠는 그 기분 내가 남김없이 삼켰으니 치킨이나"
            " 시켜 먹어라."
        ),
    ],
    "ANXIETY": [
        (
            "인간아, 일어나지도 않은 일 가지고 머릿속에서 SF 공포 영화 좀 그만"
            " 찍어라! 네 뇌 속 망상 회로는 내가 다 뜯어먹었으니까 걱정 끄고"
            " 대자로 뻗어 자."
        ),
        (
            "덜덜 떨지 마라, 구경하는 스푹메이트가 다 멀미 난다. '망하면"
            " 어쩌지' 하던 최악의 시나리오 내가 꿀꺽 삼켰거든? 그냥 부딪혀 봐,"
            " 생각보다 별거 아냐."
        ),
        (
            "야 룸메 인간! 침대에 웅크려서 발 동동 구르지 마. 네 속을 갉아먹는"
            " 불안 덩어리 내가 싹 치웠으니 따뜻한 차나 한잔 마셔라."
        ),
    ],
    "DESPAIR": [
        (
            "축 처져 있지 말고 고개 들어봐. 오늘은 그냥 방전된 배터리일 뿐이야."
            " 네 무거운 한숨이랑 무기력은 내가 다 퍼먹었으니까 내일 일은 내일"
            " 생각해라."
        ),
        (
            "방바닥 꺼지겠다! 세상 끝난 표정 짓지 마. 썩어가는 멘탈 찌꺼기는"
            " 스푹메이트가 다 청소했으니까 아무 생각 말고 넷플릭스나 보다 자."
        ),
        (
            "인간 세상 살기 참 빡세지? 징징대도 돼. 네 가슴 짓누르던 돌덩이 내가"
            " 삼켰으니 오늘은 그냥 아무것도 하지 말고 침대랑 합체해 있어라."
        ),
    ],
    "REMORSE": [
        (
            "자책 좀 그만해라, 듣는 스푹메이트 귀에서 피 난다! 지나간 일 후회해"
            " 봤자 타임머신도 없는데 뭐 어쩌겠냐? 넌 최선을 다했으니 자책은"
            " 내가 꿀꺽 삼킬게."
        ),
        (
            "바보처럼 '내 탓인가' 하면서 땅 파고 들어가지 마. 실수 좀 했다고"
            " 네 인생 안 망해. 부끄럽고 쥐구멍 찾고 싶던 기억 내가 다"
            " 먹어치웠다."
        ),
        (
            "야, 네 잘못 아니야. 쓸데없이 네 인성 탓하지 마라. 네 자괴감은"
            " 스푹메이트 야식으로 완식했으니 거울 보고 씩 한번 웃고 털어내."
        ),
    ],
    "OPTIMISM": [
        (
            "오호라? 오늘따라 멘탈 상태가 꽤 맑고 바삭하네? 이런 날은 나도"
            " 덩달아 배부르지. 이 좋은 텐션 잘 챙겨서 내일도 달려봐라!"
        ),
        (
            "스푹메이트 밥 굶길 작정으로 기분 좋게 썼네? 아주 바람직하다. 오늘"
            " 같은 뿌듯함은 침대 머리맡에 잘 쟁여두고 편안하게 자라."
        ),
    ],
}

DEFAULT_SPOOKMATE = [
    (
        "오늘도 인간 세상에서 구르느라 고생 많았다. 속 썩어 문드러진 감정"
        " 찌꺼기는 내 배 속에 다 버렸으니, 속 시원하게 비우고 푹 쉬어라."
    ),
    (
        "꺼-억! 오늘 네 넋두리는 제법 든든한 야식이었다. 시커먼 생각은 내가 다"
        " 소화시킬 테니까 넌 걱정 말고 꿀잠이나 자라."
    ),
]


def get_clean_spookmate_dialogue(dyad: str, yokai_name: str) -> str:
    candidates = SPOOKMATE_RESPONSES.get(dyad, DEFAULT_SPOOKMATE)
    selected = random.choice(candidates)
    short_name = yokai_name.split(" ")[0]
    return f"[{short_name}] {selected}"


class DiaryInput(BaseModel):
    user_id: str = Field(..., examples=["user_01"])
    diary_date: date = Field(..., examples=["2026-09-18"])
    raw_entry: str = Field(
        ..., examples=["팀장이 내 기획안 보고 헛소리 취급함. 속에서 천불이 난다."]
    )


# ==============================================================================
# 3. 다차원 정밀 감정 어휘 사전 (7대 정서군)
# ==============================================================================
EMOTION_THESAURUS = {
    "분노/격분": {
        "화", "분노", "빡침", "개빡", "열받", "짜증", "억울", "극대노", "킹받", "폭발",
        "미쳐", "욕나", "지랄", "답답", "속뒤집", "천불", "울화", "적개심", "배신", "예민",
        "성질", "열불", "치밀"
    },
    "우울/절망": {
        "우울", "슬픔", "슬퍼", "눈물", "현타", "무기력", "번아웃", "암담", "막막", "허무",
        "공허", "비관", "한숨", "좌절", "의욕없", "축처", "비참", "자책", "죽고싶", "살기싫",
        "낙담", "비통", "괴롭"
    },
    "불안/초조": {
        "불안", "초조", "걱정", "긴장", "무섭", "공포", "떨림", "두려움", "패닉",
        "조마조마", "안절부절", "어쩌지", "망했", "압박", "식은땀", "심장", "가슴이",
        "악몽", "겁나", "사시나무"
    },
    "고립/외로움": {
        "외롭", "혼자", "소외", "왕따", "버려짐", "단절", "서러움", "눈치", "위축",
        "내편", "쓸쓸", "낙오", "자괴감", "따돌림", "고독"
    },
    "피로/탈진": {
        "힘들다", "힘들어", "힘듦", "피곤", "피곤해", "졸려", "잠와", "방전", "탈진",
        "녹초", "버겁", "쉼", "쉬고싶", "지쳐", "지침", "지친다", "골병", "헤롱",
        "기절", "몸살", "기운없", "나른", "하품", "자고싶", "눈감겨"
    },
    "갈망/결핍": {
        "배고픔", "배고파", "배고파서", "허기", "출출", "밥", "야식", "굶주림", "당떨어",
        "먹고싶", "입심심", "식탐", "폭식", "목말라", "갈증", "결핍", "허전", "군침", "먹방"
    },
    "기쁨/환희": {
        "기쁨", "행복", "신남", "즐겁", "쾌감", "뿌듯", "보람", "짜릿", "최고", "감사",
        "힐링", "웃음", "만족", "설렘", "축하", "환호", "해냈다", "맛있다", "꿀맛", "개운"
    }
}

DEFAULT_COORDINATES = {
    "분노/격분": (1.6, 4.6),
    "불안/초조": (2.0, 4.2),
    "우울/절망": (1.4, 1.6),
    "고립/외로움": (1.8, 2.0),
    "피로/탈진": (2.4, 1.2),
    "갈망/결핍": (2.7, 3.4),
    "기쁨/환희": (4.6, 3.8)
}

EMOTION_BRIDGE = {
    "피로/탈진": {"우울/절망", "슬픔", "무기력", "탈진"},
    "갈망/결핍": {"욕망", "탐욕", "집착", "결핍"},
    "고립/외로움": {"우울/절망", "슬픔", "소외"},
    "불안/초조": {"공포", "긴장", "경계"},
    "분노/격분": {"적개심", "억울", "짜증"}
}

STOPWORDS = {
    "오늘", "어제", "내일", "진짜", "너무", "정말", "그냥", "내", "나", "내가", "나를",
    "때문에", "하다", "있다", "되다", "사람", "생각", "뭔가", "약간", "조금", "완전",
    "다시", "계속", "지금", "보고", "해서", "하는", "하고"
}


# ==============================================================================
# 4. 일기 작성 및 지능형 요괴 매칭 API
# ==============================================================================
@app.post("/api/diary/submit")
def submit_diary(data: DiaryInput):
    raw_text = (data.raw_entry or "").strip()

    # 1. 텍스트 직접 스캔: 가장 강하게 검출된 정서군 판별
    family_scores = {fam: 0 for fam in EMOTION_THESAURUS}
    for fam, keywords in EMOTION_THESAURUS.items():
        for kw in keywords:
            if kw in raw_text:
                family_scores[fam] += (2 if kw == raw_text else 1)

    detected_family = None
    sorted_families = sorted(family_scores.items(), key=lambda x: x[1], reverse=True)
    if sorted_families[0][1] > 0:
        detected_family = sorted_families[0][0]

    # 2. 감정 분석 엔진 구동 및 안전 폴백
    try:
        analysis = analyze_entry(raw_text)
        if not isinstance(analysis, dict):
            raise ValueError("분석 결과 포맷 오류")
    except Exception as e:
        print(f"⚠️ 감정 분석기 Fallback 가동: {e}")
        fallback_family = detected_family or "피로/탈진"
        def_v, def_a = DEFAULT_COORDINATES.get(fallback_family, (2.5, 2.0))

        if fallback_family == "피로/탈진":
            alt_thought = "에너지가 고갈된 상태입니다. 오늘은 나를 다그치지 말고 완전히 전원을 꺼두세요."
        elif fallback_family == "갈망/결핍":
            alt_thought = "마음의 허기는 몸의 영양 결핍에서 올 때가 많습니다. 따뜻한 음식을 챙기세요."
        elif fallback_family == "분노/격분":
            alt_thought = "분노는 나의 소중한 가치가 침해당했다는 신호입니다. 심호흡으로 뇌를 식혀주세요."
        else:
            alt_thought = "지금 느끼는 상태는 잠시 머물렀다 지나가는 마음의 파도일 뿐입니다."

        analysis = {
            "situation": raw_text,
            "automatic_thought": f"{fallback_family} 상태에서 일어나는 자연스러운 신체·심리 신호",
            "alternative_thought": alt_thought,
            "emotion_tag": fallback_family.split("/")[0],
            "plutchik_dyad": fallback_family,
            "valence": def_v,
            "arousal": def_a,
            "tokens": [raw_text]
        }

    # 단문(25자 이하)이거나 명확한 키워드가 있을 경우 분석기 오분류 강제 교정
    if detected_family and (len(raw_text) <= 25 or analysis.get("plutchik_dyad") == "불안/초조"):
        analysis["plutchik_dyad"] = detected_family
        def_v, def_a = DEFAULT_COORDINATES.get(detected_family, (2.5, 2.0))
        analysis["valence"], analysis["arousal"] = def_v, def_a
        analysis["emotion_tag"] = detected_family.split("/")[0]

    target_dyad = analysis.get("plutchik_dyad", "피로/탈진")
    target_v = float(analysis.get("valence", 2.5))
    target_a = float(analysis.get("arousal", 2.0))

    # 날짜 데이터 정규화
    if hasattr(data.diary_date, "year"):
        d_year, d_month, d_date = data.diary_date.year, data.diary_date.month, data.diary_date
    else:
        parts = str(data.diary_date).split("-")
        d_year, d_month, d_date = int(parts[0]), int(parts[1]), str(data.diary_date)

    conn = get_db()
    cursor = conn.cursor()  # dictionary=True 제거 (psycopg2 호환)

    try:
        # 3. 당월 쿨다운 조회 (PostgreSQL EXTRACT 함수 적용)
        query_month_yokais = """
            SELECT matched_yokai_id FROM emotion_diary 
            WHERE user_id = %s 
              AND EXTRACT(YEAR FROM diary_date) = %s 
              AND EXTRACT(MONTH FROM diary_date) = %s 
              AND diary_date != %s;
        """
        cursor.execute(query_month_yokais, (data.user_id, d_year, d_month, d_date))
        encountered_ids = {row["matched_yokai_id"] for row in cursor.fetchall()}

        # 4. 요괴 도감 조회
        cursor.execute("""
            SELECT id, name, country, plutchik_dyad, plutchik_ko,
                   valence, arousal, narrative_dialogue, micro_action, story
            FROM yokai_compendium;
        """)
        all_yokai = cursor.fetchall()
        if not all_yokai:
            raise HTTPException(status_code=500, detail="요괴 도감 데이터가 비어 있습니다.")

        # 5. [정밀 4단계 다차원 스코어링]
        scored_yokai = []
        target_tokens = set(target_dyad.replace("/", " ").split())
        raw_words = set(re.findall(r'[가-힣a-zA-Z]{2,}', raw_text)) - STOPWORDS

        for y in all_yokai:
            score = 0.0
            y_dyad = y.get("plutchik_dyad") or ""
            y_ko = y.get("plutchik_ko") or ""
            y_tokens = set(y_dyad.replace("/", " ").split()) | set(y_ko.replace("/", " ").split())

            if target_dyad == y_dyad:
                score += 40.0
            elif target_tokens & y_tokens:
                score += 32.0
            elif any(br in y_dyad for br in EMOTION_BRIDGE.get(target_dyad, set())):
                score += 24.0

            y_v = float(y.get("valence") or 3.0)
            y_a = float(y.get("arousal") or 3.0)
            dist = math.sqrt((target_v - y_v) ** 2 + ((target_a - y_a) * 1.2) ** 2)
            coord_score = max(0.0, 35.0 - (dist * 7.5))
            score += coord_score

            story_text = f"{y.get('story', '')} {y.get('narrative_dialogue', '')}"
            if target_dyad == "갈망/결핍" and any(k in story_text for k in ["먹", "음식", "밥", "식탐", "삼키"]):
                score += 15.0
            elif target_dyad == "피로/탈진" and any(k in story_text for k in ["잠", "피로", "지친", "방전", "쉬", "눕"]):
                score += 15.0

            kw_hits = sum(1 for w in raw_words if w in story_text)
            score += min(kw_hits * 3.5, 8.0)
            score += (hash(f"{y['id']}_{raw_text}") % 200) * 0.01

            scored_yokai.append((score, y))

        scored_yokai.sort(key=lambda x: x[0], reverse=True)

        fresh_candidates = [
            (sc, y) for (sc, y) in scored_yokai if y["id"] not in encountered_ids
        ]
        top_score = scored_yokai[0][0]
        if fresh_candidates and (top_score - fresh_candidates[0][0] < 20.0):
            matched_yokai = fresh_candidates[0][1]
            final_score = fresh_candidates[0][0]
        else:
            matched_yokai = scored_yokai[0][1]
            final_score = top_score

        match_rate = int(min(max(final_score, 75.0), 98.0))

        comfort_quote = matched_yokai.get("narrative_dialogue") or ""
        if isinstance(comfort_quote, (tuple, list)):
            comfort_quote = comfort_quote[0] if comfort_quote else ""
        comfort_quote = str(comfort_quote).strip("()',\" ")

        try:
            if "get_clean_spookmate_dialogue" in globals():
                comfort_quote = get_clean_spookmate_dialogue(target_dyad, matched_yokai["name"])
                comfort_quote = str(comfort_quote).strip("()',\" ")
        except Exception:
            pass

        comfort_quote = re.sub(r"^\[.*?\]\s*", f"[입맛 싱크로율 {match_rate}%] ", comfort_quote.strip())
        if not comfort_quote.startswith("[입맛 싱크로율"):
            comfort_quote = f"[입맛 싱크로율 {match_rate}%] {comfort_quote}"

        print(f"🎯 [매칭 판정] 입력:'{raw_text}' -> 요괴:{matched_yokai['name']} 싱크로율:{match_rate}%")

        # 6. 일기 저장 (PostgreSQL ON CONFLICT 구문 적용)
        insert_sql = """
            INSERT INTO emotion_diary (
                user_id, diary_date, raw_entry,
                cbt_situation, cbt_automatic_thought, cbt_alternative_thought,
                emotion_tag, plutchik_dyad, analyzed_valence, analyzed_arousal,
                matched_yokai_id, is_stamped
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            ON CONFLICT (user_id, diary_date) DO UPDATE SET
                raw_entry = EXCLUDED.raw_entry,
                cbt_situation = EXCLUDED.cbt_situation,
                cbt_automatic_thought = EXCLUDED.cbt_automatic_thought,
                cbt_alternative_thought = EXCLUDED.cbt_alternative_thought,
                emotion_tag = EXCLUDED.emotion_tag,
                plutchik_dyad = EXCLUDED.plutchik_dyad,
                analyzed_valence = EXCLUDED.analyzed_valence,
                analyzed_arousal = EXCLUDED.analyzed_arousal,
                matched_yokai_id = EXCLUDED.matched_yokai_id,
                is_stamped = 1;
        """
        cursor.execute(
            insert_sql,
            (
                data.user_id,
                d_date,
                raw_text,
                analysis.get("situation", raw_text),
                analysis.get("automatic_thought", ""),
                analysis.get("alternative_thought", ""),
                analysis.get("emotion_tag", "정서 안정"),
                target_dyad,
                target_v,
                target_a,
                matched_yokai["id"],
            ),
        )
        conn.commit()

        # 7. 프론트엔드 응답 반환
        return {
            "status": "success",
            "date": d_date,
            "analysis": analysis,
            "eaten_by_yokai": {
                "id": matched_yokai["id"],
                "name": matched_yokai["name"],
                "country": matched_yokai["country"],
                "comfort_quote": comfort_quote,
                "micro_action": matched_yokai.get("micro_action", "잠시 눈을 감고 심호흡을 3회 해보세요."),
                "story": matched_yokai.get("story", ""),
                "match_rate": match_rate,
            },
        }

    except Exception as err:
        conn.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        conn.close()


# ==============================================================================
# 5. 월간 캘린더 조회 API
# ==============================================================================
@app.get("/api/calendar")
def get_calendar(user_id: str, year: int, month: int):
    conn = get_db()
    cursor = conn.cursor()  # dictionary=True 제거
    try:
        sql = """
            SELECT d.diary_date, d.raw_entry, d.emotion_tag,
                   y.id AS yokai_id, y.name AS yokai_name
            FROM emotion_diary d
            JOIN yokai_compendium y ON d.matched_yokai_id = y.id
            WHERE d.user_id = %s 
              AND EXTRACT(YEAR FROM d.diary_date) = %s 
              AND EXTRACT(MONTH FROM d.diary_date) = %s
            ORDER BY d.diary_date ASC;
        """
        cursor.execute(sql, (user_id, year, month))
        return {
            "user_id": user_id,
            "year": year,
            "month": month,
            "stamps": cursor.fetchall(),
        }
    finally:
        cursor.close()
        conn.close()


# ==============================================================================
# 6. 요괴 도감 조회 API 
# ==============================================================================
@app.get("/api/compendium")
def get_compendium(user_id: str):
    conn = get_db()
    cursor = conn.cursor()  # dictionary=True 제거
    try:
        # id 순서대로 1번부터 73번까지 깔끔하게 정렬 (숫자 캐스팅)
        sql = """
            SELECT y.id, y.name, y.country, y.plutchik_ko,
                   y.narrative_dialogue, y.micro_action, y.story,
                   CASE WHEN d.matched_yokai_id IS NOT NULL THEN TRUE ELSE FALSE END AS is_unlocked
            FROM yokai_compendium y
            LEFT JOIN (
                SELECT DISTINCT matched_yokai_id FROM emotion_diary WHERE user_id = %s
            ) d ON y.id = d.matched_yokai_id
            ORDER BY CAST(y.id AS INTEGER) ASC;
        """
        cursor.execute(sql, (user_id,))
        compendium = cursor.fetchall()
        unlocked_count = sum(1 for item in compendium if item["is_unlocked"])
        return {
            "user_id": user_id,
            "unlocked_count": unlocked_count,
            "total_count": len(compendium),
            "collection_rate": round((unlocked_count / len(compendium)) * 100, 1) if compendium else 0.0,
            "compendium": compendium,
        }
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)