from datetime import date
import math
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from pydantic import BaseModel, Field
from analyzer import analyze_entry

app = FastAPI(title="SpookMate API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1234",  # 본인 패스워드
    "database": "yokai_diary_db",
    "charset": "utf8mb4"
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

SPOOKMATE_RESPONSES = {
    "OUTRAGE": [
        "야 인간아, 네 속에서 시커먼 연기 난다! 널 긁은 인간은 인성에 하자 있는 거니까 걔 때문에 네 속 태우지 마라. 그 끓어넘치는 분노는 내가 남김없이 씹어먹었으니 주먹 풀고 라면이나 끓여와.",
        "우걱우걱... 캬! 오늘 네 하소연은 아주 매콤한 불닭맛 특식이네. 널 화나게 한 놈 면상 대신 내가 네 분노 찌꺼기를 잘근잘근 씹어줬으니 넌 발 닦고 푹 자라."
    ],
    "ANXIETY": [
        "인간아, 일어나지도 않은 일 가지고 머릿속에서 SF 공포 영화 좀 그만 찍어라! 네 뇌 속 망상 회로는 내가 다 뜯어먹었으니까 걱정 끄고 대자로 뻗어 자.",
        "덜덜 떨지 마라, 구경하는 스푹메이트가 다 멀미 난다. '망하면 어쩌지' 하던 최악의 시나리오 내가 꿀꺽 삼켰거든? 그냥 부딪혀 봐, 별거 아냐."
    ],
    "DESPAIR": [
        "축 처져 있지 말고 고개 들어봐. 오늘은 그냥 방전된 배터리일 뿐이야. 네 무거운 한숨이랑 무기력은 내가 다 퍼먹었으니까 내일 일은 내일 생각해라.",
        "방바닥 꺼지겠다! 세상 끝난 표정 짓지 마. 썩어가는 멘탈 찌꺼기는 스푹메이트가 다 청소했으니까 아무 생각 말고 넷플릭스나 보다 자."
    ],
    "REMORSE": [
        "자책 좀 그만해라, 듣는 스푹메이트 귀에서 피 난다! 지나간 일 후회해 봤자 타임머신도 없는데 뭐 어쩌겠냐? 넌 최선을 다했으니 자책은 내가 꿀꺽 삼킬게."
    ],
    "OPTIMISM": [
        "오호라? 오늘따라 멘탈 상태가 꽤 맑고 바삭하네? 이런 날은 나도 덩달아 배부르지. 이 좋은 텐션 잘 챙겨서 내일도 달려봐라!",
        "스푹메이트 밥 굶길 작정으로 기분 좋게 썼네? 아주 바람직하다. 오늘 같은 뿌듯함은 침대 머리맡에 잘 쟁여두고 편안하게 자라."
    ]
}

DEFAULT_SPOOKMATE = [
    "오늘도 인간 세상에서 구르느라 고생 많았다. 속 썩어 문드러진 감정 찌꺼기는 내 배 속에 다 버렸으니, 속 시원하게 비우고 푹 쉬어라.",
    "꺼-억! 오늘 네 넋두리는 제법 든든한 야식이었다. 시커먼 생각은 내가 다 소화시킬 테니까 넌 걱정 말고 꿀잠이나 자라."
]

def get_clean_spookmate_dialogue(dyad: str, yokai_name: str) -> str:
    candidates = SPOOKMATE_RESPONSES.get(dyad, DEFAULT_SPOOKMATE)
    selected = random.choice(candidates)
    short_name = yokai_name.split(" ")[0]
    return f"[{short_name}] {selected}"

class DiaryInput(BaseModel):
    user_id: str = Field(..., examples=["user_01"])
    diary_date: date = Field(..., examples=["2026-09-18"])
    raw_entry: str = Field(..., examples=["즐거워"])

@app.post("/api/diary/submit")
def submit_diary(data: DiaryInput):
    analysis = analyze_entry(data.raw_entry)
    target_dyad = analysis["plutchik_dyad"]
    target_v = analysis["valence"]
    target_a = analysis["arousal"]
    user_tokens = analysis["tokens"]

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # 당월 중복 요괴 배제
        query_month_yokais = """
            SELECT matched_yokai_id FROM emotion_diary 
            WHERE user_id = %s AND YEAR(diary_date) = %s AND MONTH(diary_date) = %s AND diary_date != %s
        """
        cursor.execute(query_month_yokais, (data.user_id, data.diary_date.year, data.diary_date.month, data.diary_date))
        encountered_ids = {row["matched_yokai_id"] for row in cursor.fetchall()}

        # 69종 요괴 조회
        cursor.execute("""
            SELECT id, name, country, saju_element, plutchik_dyad, plutchik_ko,
                   valence, arousal, narrative_dialogue, micro_action, story
            FROM yokai_compendium
        """)
        all_yokai = cursor.fetchall()
        if not all_yokai:
            raise HTTPException(status_code=500, detail="요괴 도감 데이터가 비어 있습니다.")

        # 매칭 스코어 계산
        scored_yokai = []
        for y in all_yokai:
            score = 0.0
            if y["plutchik_dyad"] == target_dyad:
                score += 50.0
            story_text = (y["story"] or "") + " " + (y["narrative_dialogue"] or "")
            kw_matches = sum(1 for t in user_tokens if t in story_text)
            score += min(kw_matches * 6.0, 30.0)

            dist = math.sqrt((float(target_v) - float(y["valence"])) ** 2 + (float(target_a) - float(y["arousal"])) ** 2)
            score += max(0.0, 20.0 - (dist * 3.5))
            scored_yokai.append((score, y))

        scored_yokai.sort(key=lambda x: x[0], reverse=True)
        fresh_candidates = [y for (sc, y) in scored_yokai if y["id"] not in encountered_ids]
        matched_yokai = fresh_candidates[0] if fresh_candidates else scored_yokai[0][1]

        insert_sql = """
            INSERT INTO emotion_diary (
                user_id, diary_date, raw_entry,
                cbt_situation, cbt_automatic_thought, cbt_alternative_thought,
                emotion_tag, plutchik_dyad, analyzed_valence, analyzed_arousal,
                matched_yokai_id, is_stamped
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            ON DUPLICATE KEY UPDATE
                raw_entry = VALUES(raw_entry),
                cbt_situation = VALUES(cbt_situation),
                cbt_automatic_thought = VALUES(cbt_automatic_thought),
                cbt_alternative_thought = VALUES(cbt_alternative_thought),
                emotion_tag = VALUES(emotion_tag),
                plutchik_dyad = VALUES(plutchik_dyad),
                analyzed_valence = VALUES(analyzed_valence),
                analyzed_arousal = VALUES(analyzed_arousal),
                matched_yokai_id = VALUES(matched_yokai_id),
                is_stamped = 1,
                created_at = CURRENT_TIMESTAMP
        """
        cursor.execute(insert_sql, (
            data.user_id, data.diary_date, data.raw_entry,
            analysis["situation"], analysis["automatic_thought"], analysis["alternative_thought"],
            analysis["emotion_tag"], analysis["plutchik_dyad"], analysis["valence"], analysis["arousal"],
            matched_yokai["id"]
        ))
        conn.commit()

        return {
            "status": "success",
            "date": data.diary_date,
            "analysis": analysis,
            "eaten_by_yokai": {
                "id": matched_yokai["id"],
                "name": matched_yokai["name"],
                "country": matched_yokai["country"],
                "saju_element": matched_yokai["saju_element"],
                "comfort_quote": get_clean_spookmate_dialogue(analysis["plutchik_dyad"], matched_yokai["name"]),
                "micro_action": matched_yokai["micro_action"],
                "story": matched_yokai["story"]
            }
        }
    finally:
        cursor.close()
        conn.close()

# 캘린더 엔드포인트 복구 (404 방지)
@app.get("/api/calendar")
def get_calendar(user_id: str, year: int, month: int):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = """
            SELECT d.diary_date, d.raw_entry, d.emotion_tag,
                   y.id AS yokai_id, y.name AS yokai_name
            FROM emotion_diary d
            JOIN yokai_compendium y ON d.matched_yokai_id = y.id
            WHERE d.user_id = %s AND YEAR(d.diary_date) = %s AND MONTH(d.diary_date) = %s
            ORDER BY d.diary_date ASC
        """
        cursor.execute(sql, (user_id, year, month))
        return {
            "user_id": user_id,
            "year": year,
            "month": month,
            "stamps": cursor.fetchall()
        }
    finally:
        cursor.close()
        conn.close()

# 도감 엔드포인트 복구
@app.get("/api/compendium")
def get_compendium(user_id: str):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = """
            SELECT y.id, y.name, y.country, y.saju_element, y.plutchik_ko,
                   y.narrative_dialogue, y.micro_action, y.story,
                   CASE WHEN d.matched_yokai_id IS NOT NULL THEN TRUE ELSE FALSE END AS is_unlocked
            FROM yokai_compendium y
            LEFT JOIN (
                SELECT DISTINCT matched_yokai_id FROM emotion_diary WHERE user_id = %s
            ) d ON y.id = d.matched_yokai_id
            ORDER BY y.id ASC
        """
        cursor.execute(sql, (user_id,))
        compendium = cursor.fetchall()
        unlocked_count = sum(1 for item in compendium if item["is_unlocked"])
        return {
            "user_id": user_id,
            "unlocked_count": unlocked_count,
            "total_count": len(compendium),
            "collection_rate": round((unlocked_count / len(compendium)) * 100, 1),
            "compendium": compendium
        }
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)