USE yokai_diary_db;

DROP TABLE IF EXISTS emotion_diary;

CREATE TABLE emotion_diary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL COMMENT '사용자 식별자',
    diary_date DATE NOT NULL COMMENT '일기 작성 일자 (스탬프 기준일)',
    
    -- 사용자 인풋
    raw_entry TEXT NOT NULL COMMENT '한 줄 일기 원문',
    
    -- 3단계 인지치료 분석 (CBT)
    cbt_situation TEXT COMMENT '상황 (Situation)',
    cbt_automatic_thought TEXT COMMENT '자동적 사고 (Automatic Thought)',
    cbt_alternative_thought TEXT COMMENT '대안적 사고 (Alternative Thought)',
    
    -- 정서 분석 지표
    emotion_tag VARCHAR(50) NOT NULL COMMENT '도출된 대표 감정 태그',
    plutchik_dyad VARCHAR(50) NOT NULL COMMENT '플루치크 24대 혼합정서 코드',
    analyzed_valence FLOAT COMMENT '유쾌도 (1.0 ~ 7.0)',
    analyzed_arousal FLOAT COMMENT '각성도 (1.0 ~ 7.0)',
    
    -- 매칭 요괴 및 스탬프 (BOOLEAN 적용으로 경고 1681 제거)
    matched_yokai_id INT NOT NULL COMMENT '매칭된 요괴 ID',
    is_stamped BOOLEAN DEFAULT TRUE COMMENT '스탬프 날인 여부',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_user_date (user_id, diary_date),
    INDEX idx_user_calendar (user_id, diary_date),
    CONSTRAINT fk_diary_yokai FOREIGN KEY (matched_yokai_id) 
        REFERENCES yokai_compendium(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DESCRIBE yokai_diary_db.emotion_diary;

SELECT * FROM emotion_diary;




USE yokai_diary_db;

-- 1. 실제 테이블인 yokai_compendium에 컬럼 추가
ALTER TABLE yokai_compendium ADD COLUMN celebration_quote TEXT;

-- (참고) 워크벤치 안전 업데이트 모드(Safe Updates) 임시 해제
SET SQL_SAFE_UPDATES = 0;

-- 2. 요괴별 긍정 맞장구 대사 업데이트
UPDATE yokai_compendium 
SET celebration_quote = '[삼신할미] 아가, 오늘 아주 신명나게 웃었구나! 네 웃음소리가 마당을 울리니 내 마음도 덩실덩실 춤을 춘다. 오늘 밤엔 더 달콤한 꿈만 꾸거라.'
WHERE name LIKE '%삼신할미%';

UPDATE yokai_compendium 
SET celebration_quote = '[장산범] 크르르... 오늘은 제법 흡족한 하루였나 보군! 네 녀석의 그 펄펄 끓는 생기와 활기찬 기운이 내 털끝까지 솟구치게 만든다!'
WHERE name LIKE '%장산범%';

UPDATE yokai_compendium 
SET celebration_quote = '[설녀] 얼어붙었던 심장이 스르르 녹아내릴 만큼 눈부신 온기군요. 이 따스하고 유쾌한 기쁨을 가슴속에 고이 얼려 영원히 간직하세요.'
WHERE name LIKE '%설녀%';

UPDATE yokai_compendium 
SET celebration_quote = '[퇵발랑] 캬! 오늘 제대로 날아다녔네! 방구석에 누워있기 아까운 날이야. 그 신나는 텐션 그대로 내일까지 쭉 밀고 가자고!'
WHERE name LIKE '%퇵발랑%';

-- 안전 업데이트 모드 다시 활성화
SET SQL_SAFE_UPDATES = 1;

-- 3. 컬럼 추가 및 데이터 반영 확인
SELECT id, name, celebration_quote FROM yokai_compendium LIMIT 10;