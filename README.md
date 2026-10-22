# 👻 SpookMate (스푹메이트)

> **"혼자 끙끙 앓으면 체합니다. 오늘 나를 팍팍하게 만든 멘탈 찌꺼기, 방구석 괴물 룸메이트에게 야식 사료로 던져주세요."**
>
> 로버트 플루치크(Robert Plutchik)의 24대 혼합정서 모델과 인지행동치료(CBT) 프레임워크를 결합한 **다크코미디 감정 외재화 & 73종 요괴 수집 웹 서비스**

<p align="center">
<img src="img/01_main_calendar.png" width="100%" alt="SpookMate Main View" />
</p>

## 📌 1. 프로젝트 개요 (Overview)

현대인은 일상에서 분노, 불안, 자책, 무기력 등 복합적인 부정 정서를 마주하지만, 이를 억누르거나 자책으로 내면화하여 심리적 탈진(Burnout)을 겪습니다.

**SpookMate**는 심리학의 **서사치료(Narrative Therapy) 정서 외재화(Externalization)** 기법에 착안하여, 사용자가 배출한 거친 감정을 '내 탓'이 아닌 '방구석 괴물 룸메이트의 야식 먹잇감'으로 시각화하여 분리·해소하도록 돕는 멘탈케어 게이미피케이션 플랫폼입니다.

단순 텍스트 생성 기반 챗봇의 상투적인 위로를 탈피하고, 사용자의 감정 상태와 의미적으로 가장 유사한 **아시아 8개국 73종의 전승 요괴**를 정밀 매칭하여 뼈 때리는 츤데레 맞장구와 1분 소매틱(신체 활성화) 처방을 제공합니다.

## 🧠 2. 학술적 배경 및 심리학 모델 (Theoretical Framework)

본 프로젝트는 사주·명리학적 요소를 배제하고, 심리학 이론(서사치료·CBT·플루치크·러셀)과 비교민속학(동서양 요괴 전승 설화)이라는 두 학문적 축을 교차 분석하여 설계되었습니다.

### ① 서사치료(Narrative Therapy)의 '문제 외재화(Externalization)'

* **핵심 명제**: *"사람이 문제가 아니라 문제가 문제이다."* (Michael White & David Epston)

* 문제를 개인의 내적 결함으로 귀인하지 않고 독립된 외부 실체인 '요괴'로 분리·명명합니다.

* 사용자의 부정 정서를 방바닥에 누워 있는 룸메이트 요괴에게 던져줄 '야식 사료'로 치환하여 객관화합니다.

  * **억울함 / 분노** $\rightarrow$ 쇠를 씹어 먹으며 울화를 흡수하는 **'불가사리'**

  * **불안 / 악몽 / 잡념** $\rightarrow$ 나쁜 꿈과 헛된 망상을 먹어치우는 **'맥(Baku)'**

  * **무기력 / 방전** $\rightarrow$ 묵묵히 제자리를 지키며 기댈 곳이 되어주는 **'누리카베'**

  * **외로움 / 자책** $\rightarrow$ 시선을 받을수록 덩치가 커지는 그림자 요괴 **'어둑시니'**

### ② 로버트 플루치크(Robert Plutchik)의 24대 혼합정서(Dyads) 체계

* 8대 기본 정서의 결합 원형을 기반으로 사용자의 복합 감정을 3단계로 정밀 분류합니다.

  * **1차 혼합(Primary Dyads)**: 낙관(기쁨+기대), 사랑(기쁨+신뢰), 공격성(분노+기대), 경외(공포+놀람) 등

  * **2차·3차 혼합(Secondary/Tertiary Dyads)**: 질투/선망(슬픔+분노), 비관(슬픔+기대), 불안/염려(공포+기대), 수치심(공포+혐오), 냉소(혐오+기대) 등

### ③ 제임스 러셀(James Russell)의 원형 정동 모델 (Valence-Arousal 좌표계)

* 이산적(Discrete) 정서 코드를 유쾌도($Valence$, 불쾌 1 $\leftrightarrow$ 쾌 7)와 각성도($Arousal$, 비활성 1 $\leftrightarrow$ 활성 7)의 2차원 공간 좌표계로 정량화합니다.

* 박인조·민경환(2005) 연구의 한국어 감정 단어 434개 정량 척도 데이터를 기준으로 유저 입력과 요괴 설화 간의 유클리드 거리를 측정합니다.

### ④ 인지행동치료(CBT) 및 소매틱 신체 활성화

* **\[찌든 멘탈 강제 세척\]**: 인지 왜곡(파국화, 과재책감)의 회로를 끊어내는 CBT 표준 3단계 생각 점검(상황 $\rightarrow$ 자동적 사고 $\rightarrow$ 대안적 사고) 도출

* **\[인간 재부팅 1분 처방\]**: Jacobson 7단계 점진적 근육이완법(PMR, 레몬짜기 5초 기법), 5-4-3-2-1 감각 착지 기법(Grounding), 생리적 한숨(Physiological Sigh) 등 즉각적 신체 감각 회복 미션 부여

## ✨ 3. 핵심 기능 및 구현 화면 (Key Features & UI)

### ① 룸메이트 동거 계약서 캘린더 팝업 & 메인 홈 대시보드

* **동거 계약서 모달**: 최초 접속 시 입주자 닉네임을 설정하고 인터랙티브 캘린더 그리드를 통해 입주 기준 일자를 선택합니다. (LocalStorage + Supabase DB 실시간 동기화)

* **글로벌 UX**: 마우스 좌표를 추적하는 손전등(후레쉬) 래디얼 비네팅 효과 (배터리 방전 콘셉트로 8초 후 자동 소등 타이머 작동)

<p align="center">
<img src="img/01_contract_modal.png" width="48%" alt="동거 계약서 모달" />
<img src="img/01_main_calendar.png" width="48%" alt="메인 캘린더 화면" />
</p>

### ② 감정 일기 작성 & 먹방 애니메이션 (WHO EATS SINS)

* **감정 외재화 제출**: 오늘 겪은 일이나 억울함/불안 텍스트를 입력창에 자유롭게 작성합니다.

* **텍스트 분쇄 물리 연출**: 제출 시 삼각함수($\sin, \cos$) 기반의 궤적 연산을 통해 글자가 파편화(Text Shards)되어 요괴 입속으로 빨려 들어가는 애니메이션을 순수 CSS/JS로 렌더링합니다.

<p align="center">
<img src="img/02_diary_input.png" width="80%" alt="감정 일기 작성창" />
</p>

### ③ 3단계 요괴 소환 시퀀스 & CBT·신체 처방 모달

* **글리치 소환 시퀀스**: 중앙 글리치 진동(`animate-summon-glitch`) ➔ 1.3초 후 좌측 3:4 포스터 비율 이동 및 안착 ➔ 우측 츤데레 맞장구 대사 및 1분 신체 미션 표출

* **소매틱 처방**: 레몬짜기 PMR 이완법, 착지 호흡법 등 즉각 실행 가능한 `[SOMATIC MISSION]` 안내

* **라이트박스 뷰어**: 고증 일러스트 클릭 시 전체 화면 확대 모달 제공

<p align="center">
<img src="img/03_summon_result.png" width="80%" alt="요괴 소환 결과 및 처방" />
</p>

### ④ 73종 월간 요괴도감 (Monthly Spook Compendium)

* **도감 수집 게이미피케이션**: 해금된 컬러 카드와 미해금 흑백 실루엣 자물쇠 카드가 격자형으로 배치된 그리드 뷰

* **월간 리셋 엔진**: 상단 실시간 수집 진행도(%) 및 매월 1일 자정(00:00) 자동 리셋 로직(`spookmate_compendium_cycle`) 및 D-Day 카운트다운

<p align="center">
<img src="img/04_compendium_archive.png" width="80%" alt="월간 요괴도감 아카이브" />
</p>

### ⑤ 실시간 룸메캠 SPOOK-CAM & SPOOK OF FEELINGS

* **SPOOK-CAM**: CAM 1(주방), CAM 2(거실), CAM 3(현관) 3채널 실시간 GIF 피드 스위칭, 화면 색상 반전 글리치 연출, 마이크 호통치기 및 위로 사탕 간식 주기 인터랙션

* **SPOOK OF FEELINGS**: 4대 상극 정서 요괴(호려정-분노, 유키온나-불안, 삼신할미-환희, 좌식와라시-안도)와의 1:1 몰입형 티키타카 대화 모듈

<p align="center">
<img src="img/05_spook_cam.png" width="48%" alt="실시간 룸메캠" />
<img src="img/06_spook_feelings.png" width="48%" alt="상극 요괴 대화" />
</p>

## 🏗️ 4. 시스템 아키텍처 및 데이터 파이프라인

```
[데이터 파이프라인 (n8n 자동화)]
 Google Sheets (기존 데이터 조회) ➔ JS Code (중복 제외 목록 생성) ➔ AI Agent (OpenAI + Tavily) ➔ JS Code (JSON 안전 파싱) ➔ Google Sheets (신규 요괴 데이터 적재)
       │
       ▼
[런타임 서비스 파이프라인]
[사용자 일기 입력 (Frontend)]
 "오늘 팀 회의 때 내 의견 다 무시당함. 내가 무능해서 그런가 싶고 다 때려치우고 싶다."
       │
       ▼
[백엔드 분석 엔진 (FastAPI / analyzer.py)]
 ├─ 3단계 CBT 분해:
 │   ├─ 상황 (cbt_situation): "팀 회의 중 본인의 제안이 수용되지 않음"
 │   ├─ 자동적 사고 (cbt_automatic_thought): "내가 무능해서 무시당한 것 (개인화/과일반화 오류)"
 │   └─ 대안적 사고 (cbt_alternative_thought): "의견 우선순위 문제일 뿐, 내 존재 가치와는 무관함"
 ├─ 정서 좌표 추출: 플루치크 'OUTRAGE(격분)' / Valence 1.84, Arousal 6.17
       │
       ▼
[다차원 요괴 매칭 엔진 (app.py)]
 ├─ 3중 복합 스코어링:
 │   ├─ 1순위: 플루치크 24대 Dyad 코드 일치도 (최대 50점)
 │   ├─ 2순위: 일기 토큰과 73종 설화(story) 텍스트 간 의미 유사도 (최대 30점)
 │   └─ 3순위: 2차원 V-A 유클리드 거리 감점 (가까울수록 최대 20점)
 ├─ 월간 쿨다운 필터: 당월(Same Month) 이미 소환된 요괴 ID를 제외하여 중복 방지
 └─ 최종 매칭: '불가사리(Bulgasari)' 선정
       │
       ▼
[데이터베이스 영속화 (Supabase PostgreSQL)]
 ├─ emotion_diary: 원문 일기, CBT 결과, 감정 좌표, 매칭 요괴 ID 적재 (멱등성 유지)
 └─ yokai_collection: 월별 요괴 도감 해금 상태 갱신
       │
       ▼
[사용자 화면 렌더링 (Frontend)]
 ├─ 텍스트 분쇄 먹방 애니메이션 (sin/cos 물리 궤적 연산)
 ├─ 3단계 글리치 소환 시퀀스 (1.3초 후 좌측 3:4 카드 고정)
 ├─ 요괴 룸메 맞장구: "속을 까맣게 태우는 쇠붙이 같은 화는 내가 삼켰다. 주먹부터 펴라."
 ├─ 1분 신체 처방: 레몬짜기 이완법 (양손 5초 수축 후 이완)
 └─ 월간 캘린더 스탬프 날인 및 73종 도감 해금

```

### 3중 복합 매칭 점수식

$$
Score = Score_{dyad} + Score_{story} + Score_{distance}
$$

$$
Distance = \sqrt{(V_{user} - V_{yokai})^2 + (A_{user} - A_{yokai})^2}
$$

## 🤖 5. 데이터 엔지니어링 & 생성형 AI 제어

### ① n8n 기반 요괴 문헌 자동 수집 파이프라인 (`Spookn8n.json`)

* **동적 중복 배제 (Deduplication)**: Google Sheets의 기존 적재 목록을 읽어 AI 프롬프트의 `[중복 제외 목록]`에 동적으로 주입하여 중복 수집 100% 방지

* **고신뢰 출처 필터링**: Tavily Search 노드의 `Exclude Domains`에 `wikipedia.org`, `namu.wiki`를 등록하여 일반 백과사전을 배제하고, 전문 민담 도감·박물관 아카이브·신화 포털 URL만 수집

* **무중단 파싱 엔진**: AI 응답에 서술형 텍스트가 혼입되더라도 정규식 추출 Code 노드를 거쳐 정형 JSON 배열만 안전하게 추출하여 파이프라인 중단 방지

<p align="center">
<img src="img/07_n8n_pipeline.png" width="85%" alt="n8n 자동화 파이프라인 캔버스" />
</p>

### ② 국가별 전통 화풍 고증 프롬프트 엔지니어링 (73종 에셋)

원작 설화의 문화적 고증과 시각적 몰입감을 확보하기 위해 각 국가의 전통 예술 양식을 분석하고 전용 프롬프트를 직접 설계하여 73종 요괴 이미지를 생성했습니다.

* **일본 (우키요에 목판화 & 어둠의 동화)**: 가는 먹선, 크로스해칭/점묘법 텍스처, 낡은 와시(Washi) 종이, 세피아 및 핏빛 레드 포인트

* **한국 (조선 후기 민화 & 채색화)**: 묵선 기법, 전통 바림(번짐) 기법, 오방색 안료, 닥나무 한지 섬유 질감, 차/흙탕물 배접 고색(Patina)

* **중국 (농민화, Peasant Art)**: 굵고 진한 윤곽선, 그라데이션 없는 평면 컬러 블록, 적층 구도(Stacked perspective), 여백 없는 밀집 배치

* **동남아 전통 양식**: 태국 라마끼안 벽화(금박 Lai Rod Nam), 필리핀 19세기 미니아투리스모(피냐 파인애플 섬유 자수 질감), 인도네시아 바틱 툴리스(와양 쿨릿 실루엣, 왁스 균열선)

* **에셋 검증 도구**: `build_yokai_review.py` 및 `yokai_visual_review.html`을 구축하여 생성된 73종 이미지 에셋의 해상도 및 렌더링 무결성을 사전 검토

## 🛠️ 6. 기술 스택 (Tech Stack)

| 구분 | 기술 스택 | 도입 사유 및 핵심 역할 | 
| ----- | ----- | ----- | 
| **Frontend** | Vanilla JavaScript (ES6+), HTML5, CSS3, Tailwind CSS | 프레임워크 오버헤드 없는 초경량 SPA 구축, 삼각함수 기반 파티클 연산, PWA 지원 (`manifest.json`) | 
| **Backend** | Python 3.10+, FastAPI, Uvicorn, Pydantic | 비동기 고성능 REST API 처리, Swagger 자동 문서화, Pydantic 스키마 검증 | 
| **Database** | Supabase (PostgreSQL), `psycopg2-binary` | 관계형 데이터 무결성 보장, 닉네임 레지스트리 및 월별 요괴 도감 수집 상태 관리 | 
| **AI & Automation** | Google Gemini API, OpenAI `gpt-4o-mini`, n8n, Tavily API | 룸메이트 페르소나 실시간 대화 생성, 문헌 데이터 자동 수집 및 정제 | 
| **Deployment** | Render Cloud Hosting | 백엔드 API 호스팅 (`https://spookmate-backend.onrender.com/api`) | 

## 🗄️ 7. 데이터베이스 스키마 (Database Schema)

### `yokai_compendium` (요괴 마스터 테이블 - 73종)

* `id` (INT, PK): 요괴 고유 식별 번호 (1\~73)

* `name` (VARCHAR), `country` (VARCHAR): 요괴 명칭 및 기원 국가

* `plutchik_dyad` (VARCHAR), `plutchik_ko` (VARCHAR): 상징 혼합 정서 코드 및 국문 명칭

* `valence` (FLOAT), `arousal` (FLOAT): 2차원 정서 좌표값 (1.0 \~ 7.0)

* `story` (TEXT): 전승 설화 요약 코퍼스

* `narrative_dialogue` (TEXT): 서사치료 외재화 대사

* `micro_action` (VARCHAR): 1\~3분 신체 행동 미션

### `emotion_diary` (감정 일기 트랜잭션 테이블)

* `id` (INT, PK, Auto Increment)

* `user_id` (VARCHAR), `diary_date` (DATE, Unique Composite)

* `raw_entry` (TEXT): 사용자가 작성한 원문 일기

* `cbt_situation`, `cbt_automatic_thought`, `cbt_alternative_thought` (TEXT): CBT 3단계 분석 결과

* `emotion_tag` (VARCHAR), `plutchik_dyad` (VARCHAR): 판별된 감정 태그

* `analyzed_valence` (FLOAT), `analyzed_arousal` (FLOAT): 분석된 2D 정서 좌표

* `matched_yokai_id` (INT, FK): 매칭 및 해금된 요괴 ID

* `is_stamped` (BOOLEAN): 달력 스탬프 각인 여부

## 📊 8. 사용자 분석 및 정량적 성과 (User Analytics)

실제 배포 후 GA4 추적 데이터 및 Supabase DB 적재 트랜잭션을 분석한 결과입니다.

| 핵심 지표 | 수치 | 성과 및 어필 포인트 | 
| ----- | ----- | ----- | 
| **누적 퍼널 최종 전환율** | **36.8%** (153건 / 415명) | 전체 누적 방문자 415명 중 153건의 다이어리 제출 완료. 일반 웹 랜딩페이지 전환율(5\~10%)을 훌쩍 상회 | 
| **자발적 기능 개시율 (Activation)** | **73.3%** (22명 / 30명) | GA4 기간 방문자 30명 중 22명이 `form_start` 이벤트 발생. 텍스트 입력 허들을 성공적으로 낮춘 진입 경험 설계 | 
| **오가닉 유저 평균 체류 시간** | **5분 23초** (Direct 기준) | 전체 평균 4분 32초, 직접 유입 19명 기준 5분 23초 달성. 리테일 매장 관리 경험을 이식한 고관여 체류형 UX 검증 | 
| **랜딩 페이지 이탈률** | **26.7%** | 웹 서비스 초기 랜딩페이지 이탈률(보통 40% 이상) 대비 극히 안정적인 수준 유지 | 
| **코어 유저 리텐션 (재방문)** | **최소 4회 이상 반복 제출** | DB 분석 결과 '마포구 보안관', '임자', '양평퇴마사' 등 동일 닉네임 유저가 약 한 달간 지속적으로 다이어리 작성 | 

## 📁 9. 프로젝트 디렉토리 구조 (Directory Structure)

```
spookmate/
├── backend/
│   └── requirements.txt            # 백엔드 의존성 패키지 명세
├── img/                            # 73종 요괴 일러스트, UI 에셋 및 구현 화면 캡처
│   ├── 01_contract_modal.png       # 동거 계약서 모달 캡처
│   ├── 01_main_calendar.png        # 메인 홈 & 캘린더 캡처
│   ├── 02_diary_input.png          # 감정 일기 작성 폼 캡처
│   ├── 03_summon_result.png        # 요괴 소환 및 처방 결과 캡처
│   ├── 04_compendium_archive.png   # 73종 요괴도감 아카이브 캡처
│   ├── 05_spook_cam.png            # 실시간 룸메캠 캡처
│   ├── 06_spook_feelings.png       # 상극 요괴 1:1 대화 캡처
│   ├── 07_n8n_pipeline.png         # n8n 자동화 파이프라인 캡처
│   ├── 1.png ~ 73.png              # 73종 요괴 원본 캐릭터 일러스트
│   └── ...
├── media/                          # 펫캠용 GIF (1.gif~3.gif) 및 동영상 에셋
├── migrations/                     # Supabase PostgreSQL 마이그레이션 SQL
│   ├── 2026_10_16_nickname_registry.sql
│   └── 2026_10_19_yokai_collection.sql
├── 데이터원본/                      # 원본 데이터셋 (Spooksheet.csv, 아시아 요괴 도감.xlsx)
├── 심리학 문헌/                     # CBT, 플루치크, 서사치료, 한국어 감정어휘 학술 논문
├── 요괴문헌/                       # 곽재식 작가 연구 자료 및 동서양 괴물 문헌
├── .env.example                    # 환경변수 템플릿 (Supabase URL/Key, Gemini API Key)
├── Spookn8n.json                   # n8n 요괴 수집 자동화 워크플로우
├── admin.html                      # 관리자 모니터링 대시보드
├── analyzer.py                     # 플루치크 24 Dyads & CBT 분석 엔진
├── app.js                          # 프론트엔드 메인 로직 (애니메이션, 소환, 달력, API)
├── app.py                          # FastAPI 백엔드 메인 서버 (v1.2.0)
├── build_yokai_review.py           # 요괴 에셋 렌더링 검토 데이터 생성 스크립트
├── index.html                      # 메인 사용자 인터페이스 (PWA 지원)
├── manifest.json                   # PWA 매니페스트 파일
├── requirements.txt                # Python 패키지 의존성 목록
├── start.bat                       # 로컬 원클릭 실행 배치 스크립트
├── test_db.py                      # DB 연결 테스트 스크립트
├── test_diary_regression.py        # 다이어리 회귀 테스트 스크립트
├── verify_yokai_assets.py          # 요괴 에셋 무결성 검증 스크립트
├── yokai_chat.py                   # 4대 룸메이트 대화 엔진 & Gemini Fallback
├── yokai_image_map.json            # 73종 요괴 이미지 매핑 테이블
└── yokai_visual_review.html        # 요괴 비주얼 검토 전용 웹 뷰어

```

## 🚀 10. 시작하기 (Getting Started)

### 1. 저장소 클론 및 가상환경 설정

```
git clone https://github.com/jeongminimi/spookmate.git
cd spookmate

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

### 2. 환경변수 설정 (`.env`)

`.env.example`을 복사하여 `.env`를 생성하고 관련 키값을 입력합니다.

```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
GEMINI_API_KEY=your_gemini_api_key

```

### 3. 백엔드 API 서버 실행

```
uvicorn app:app --reload --port 8000

```

* 서버 가동 후 `http://localhost:8000/docs`에서 Swagger API 문서를 확인할 수 있습니다.

### 4. 프론트엔드 접속

* VS Code의 `Live Server` 확장을 사용하거나 브라우저에서 `index.html`을 직접 열어 접속합니다.