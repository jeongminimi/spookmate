// ============================================================================
// 1. 전역 설정 및 날짜 초기화
// ============================================================================
const API_BASE = "http://127.0.0.1:8000/api";

// 시스템 기준 현재 실제 날짜 객체
const now = new Date();
let currentYear = now.getFullYear();
let currentMonth = now.getMonth() + 1; // getMonth()는 0부터 시작하므로 +1

// 페이지 최초 로드 시 실행되는 초기화 이벤트
window.addEventListener("DOMContentLoaded", () => {
  // [일기 탭] 기본 기록 날짜를 오늘 날짜(YYYY-MM-DD)로 자동 세팅
  const dateInput = document.getElementById("diaryDate");
  if (dateInput) {
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    dateInput.value = `${year}-${month}-${day}`;
  }

  // [달력 탭] 이번 달 달력 최초 렌더링
  loadCalendar(currentYear, currentMonth);
});

// ============================================================================
// 2. UI 조작 함수 (탭 전환 및 모달 닫기)
// ============================================================================
// 탭 전환 (방구석 넋두리 / Stemp 달력 / Spook 도감)
function switchTab(tabName) {
  // 상단 탭 버튼 활성화 스타일 동기화
  document.querySelectorAll(".tab-btn").forEach((btn, idx) => {
    btn.classList.toggle(
      "active",
      ["write", "calendar", "compendium"][idx] === tabName,
    );
  });

  // 모든 탭 본문 숨김 처리 후 선택된 탭만 노출
  document
    .querySelectorAll(".tab-content")
    .forEach((content) => content.classList.remove("active"));

  const targetTab = document.getElementById(`tab-${tabName}`);
  if (targetTab) targetTab.classList.add("active");

  // 탭 전환 시 필요한 데이터 즉시 갱신
  const userId = document.getElementById("userIdInput")?.value || "user_01";
  if (tabName === "calendar") loadCalendar(currentYear, currentMonth);
  if (tabName === "compendium") loadCompendium(userId);
}

// 팝업 모달 닫기
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove("active");
}

// ============================================================================
// 3. 일기 작성 및 제출 처리
// ============================================================================
async function handleDiarySubmit(e) {
  e.preventDefault();
  const userId = document.getElementById("userIdInput").value.trim();
  const diaryDate = document.getElementById("diaryDate").value;
  const rawEntry = document.getElementById("rawEntry").value.trim();
  const submitBtn = document.getElementById("submitBtn");

  // 중복 클릭 방지를 위한 버튼 비활성화
  submitBtn.disabled = true;
  submitBtn.innerText = "스푹이 흔들어 깨우는 중...";

  try {
    // 백엔드 API로 감정 분석 요청
    const res = await fetch(`${API_BASE}/diary/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        diary_date: diaryDate,
        raw_entry: rawEntry,
      }),
    });

    if (!res.ok) throw new Error("서버 응답 오류");
    const data = await res.json();

    // 텍스트 흡입 애니메이션 및 결과 모달 출력
    playEatingSequence(rawEntry, data);
    document.getElementById("rawEntry").value = "";
  } catch (err) {
    alert(
      "스푹이 소환에 실패했습니다. 백엔드 서버(uvicorn) 상태를 확인해 주세요.",
    );
    console.error(err);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerText = "SpookMate에게 하소연 폭격하기";
  }
}

// ============================================================================
// 4. 요괴 하소연 흡입 애니메이션 연출 및 모달 데이터 렌더링
// ============================================================================
function playEatingSequence(rawText, serverData) {
  const modal = document.getElementById("resultModal");
  const particleField = document.getElementById("particleField");
  const yokaiMouth = document.getElementById("yokaiMouth");
  const shockwave = document.getElementById("shockwave");
  const gulpBadge = document.getElementById("gulpBadge");
  const modalDetails = document.getElementById("modalDetails");

  // ★ [수정] 감정의 긍정/부정 판단 (쾌락가 valence 5.0 이상이면 긍정 정서)
  const valence = serverData.analysis?.valence ?? 3.0;
  const isPositive = serverData.analysis.valence >= 5.0;

  // 애니메이션 요소 초기화
  particleField.innerHTML = "";
  modalDetails.classList.remove("reveal");
  gulpBadge.classList.remove("pop");
  shockwave.classList.remove("fire");
  yokaiMouth.className = "yokai-mouth suction";
  modal.classList.add("active");

  // 사용자가 입력한 문장을 파편(샤드) 단어로 분해
  const words = rawText.split(/\s+/).filter((w) => w.length > 0);
  let shards = [];
  words.forEach((w) => {
    if (w.length <= 3) shards.push(w);
    else shards.push(w.slice(0, 2), w.slice(2));
  });

  // ★ [수정] 입력 텍스트가 짧을 때 채워 넣는 기본 파편도 감정 상태에 맞게 분기
  if (shards.length < 8) {
    const fallbackShards = isPositive
      ? ["기쁨", "행복", "신남", "짜릿", "보람", "설렘"]
      : ["불안", "화남", "답답함", "스트레스", "자책", "서러움"];
    shards = shards.concat(fallbackShards);
  }

  // 텍스트 파편 회전 및 흡입 좌표 계산
  const totalCount = Math.min(shards.length, 18);
  for (let i = 0; i < totalCount; i++) {
    const span = document.createElement("span");
    span.className = "text-shard";
    span.innerText = shards[i % shards.length];

    const angle = ((Math.PI * 2) / totalCount) * i + Math.random() * 0.3;
    const radius = 120 + Math.random() * 60;
    const startX = Math.cos(angle) * radius;
    const startY = Math.sin(angle) * (radius * 0.7) + 20;

    const midAngle = angle + Math.PI / 2.5;
    const midR = radius * 0.45;
    const midX = Math.cos(midAngle) * midR;
    const midY = Math.sin(midAngle) * (midR * 0.7);

    span.style.setProperty("--start-x", `${startX}px`);
    span.style.setProperty("--start-y", `${startY}px`);
    span.style.setProperty("--mid-x", `${midX}px`);
    span.style.setProperty("--mid-y", `${midY}px`);
    span.style.setProperty("--rot-start", `${(Math.random() - 0.5) * 45}deg`);
    span.style.setProperty("--rot-mid", `${(Math.random() - 0.5) * 180}deg`);
    span.style.setProperty("--speed", `${0.85 + Math.random() * 0.35}s`);
    span.style.setProperty("--delay", `${Math.random() * 0.2}s`);

    particleField.appendChild(span);
  }

  // 삼키는 순간(1.25초 뒤) 효과 및 분석 결과 데이터 바인딩
  setTimeout(() => {
    particleField.innerHTML = "";
    yokaiMouth.className = "yokai-mouth chomp";
    shockwave.classList.add("fire");
    gulpBadge.classList.add("pop");

    // ★ [수정] 긍정/부정에 따른 배지 텍스트 분기
    gulpBadge.innerText = isPositive
      ? "기운 듬뿍 충전 완료! ✨"
      : "과자 씹듯 와작와작! 소화 완료 💨";

    document.getElementById("modalYokaiName").innerText =
      `${serverData.eaten_by_yokai.name} (${serverData.eaten_by_yokai.country})`;

    // ★ [수정] 긍정/부정에 따른 정화/충전 안내 태그 문구 분기
    document.getElementById("modalEmotionTag").innerText = isPositive
      ? `#${serverData.analysis.emotion_tag} 에너지를 받아 요괴가 각성했습니다!`
      : `#${serverData.analysis.emotion_tag} 감정을 삼켜 정화했습니다!`;

    document.getElementById("modalDialogue").innerText =
      `"${serverData.eaten_by_yokai.comfort_quote}"`;
    document.getElementById("modalAlternative").innerText =
      serverData.analysis.alternative_thought;
    document.getElementById("modalAction").innerText =
      serverData.eaten_by_yokai.micro_action;

    setTimeout(() => modalDetails.classList.add("reveal"), 400);
  }, 1250);
}

// ============================================================================
// 5. 달력 렌더링 (오늘 날짜 강조 로직 포함)
// ============================================================================
async function loadCalendar(year, month) {
  const userId =
    document.getElementById("userIdInput")?.value.trim() || "user_01";
  const title = document.getElementById("calendarTitle");
  if (title) title.innerText = `${year}년 ${month}월`;
  const grid = document.getElementById("calendarGrid");
  if (!grid) return;
  grid.innerHTML = "";

  // 요일 헤더 생성 (일 ~ 토)
  const dayNames = ["일", "월", "화", "수", "목", "금", "토"];
  dayNames.forEach((d) => {
    const el = document.createElement("div");
    el.className = "day-name";
    el.innerText = d;
    grid.appendChild(el);
  });

  try {
    // 월별 스탬프(일기 기록) 데이터 수신
    const res = await fetch(
      `${API_BASE}/calendar?user_id=${userId}&year=${year}&month=${month}`,
    );
    const data = await res.json();
    const stampMap = {};
    data.stamps.forEach((s) => {
      stampMap[s.diary_date] = s;
    });

    // 시작 요일 및 해당 월의 마지막 날짜 계산
    const firstDay = new Date(year, month - 1, 1).getDay();
    const lastDate = new Date(year, month, 0).getDate();

    // 1일 시작 전 빈 칸 채우기
    for (let i = 0; i < firstDay; i++) {
      const emptyCell = document.createElement("div");
      emptyCell.className = "day-cell empty";
      grid.appendChild(emptyCell);
    }

    // 오늘 날짜 문자열 계산 (YYYY-MM-DD)
    const realToday = new Date();
    const todayStr = `${realToday.getFullYear()}-${String(realToday.getMonth() + 1).padStart(2, "0")}-${String(realToday.getDate()).padStart(2, "0")}`;

    // 1일부터 마지막 날까지 날짜 셀 생성
    for (let date = 1; date <= lastDate; date++) {
      const dateStr = `${year}-${String(month).padStart(2, "0")}-${String(date).padStart(2, "0")}`;
      const cell = document.createElement("div");
      cell.className = "day-cell";

      // 오늘 날짜 셀 강조 표시
      const isToday = dateStr === todayStr;
      if (isToday) {
        cell.classList.add("today");
      }

      // 날짜 숫자 및 오늘 뱃지 렌더링
      cell.innerHTML = `
        <div class="date-header">
          <span class="day-number">${date}</span>
          ${isToday ? '<span class="today-badge">오늘</span>' : ""}
        </div>
      `;

      // 해당 날짜에 요괴 스탬프가 존재하는 경우 바인딩
      if (stampMap[dateStr]) {
        const s = stampMap[dateStr];
        cell.innerHTML += `
          <div class="stamp-badge">👹 ${s.yokai_name.split(" ")[0]}</div>
          <div class="stamp-tag">${s.emotion_tag}</div>
        `;
        cell.title = `[일기] ${s.raw_entry}`;
      }

      grid.appendChild(cell);
    }
  } catch (err) {
    console.error("캘린더 로드 오류:", err);
  }
}

// 이전 달 / 다음 달 이동
function changeMonth(delta) {
  currentMonth += delta;
  if (currentMonth < 1) {
    currentMonth = 12;
    currentYear--;
  }
  if (currentMonth > 12) {
    currentMonth = 1;
    currentYear++;
  }
  loadCalendar(currentYear, currentMonth);
}

// ============================================================================
// 6. 요괴 도감 렌더링 및 모달 상세 정보
// ============================================================================
async function loadCompendium(userId) {
  try {
    const res = await fetch(`${API_BASE}/compendium?user_id=${userId}`);
    const data = await res.json();

    // 수집 현황 게이지 및 텍스트 갱신
    document.getElementById("unlockCount").innerText = data.unlocked_count;
    document.getElementById("collectPercent").innerText =
      `${data.collection_rate}%`;
    document.getElementById("progressBar").style.width =
      `${data.collection_rate}%`;

    const grid = document.getElementById("compendiumGrid");
    if (!grid) return;
    grid.innerHTML = "";

    // 요괴 카드 리스트 렌더링
    data.compendium.forEach((y) => {
      const card = document.createElement("div");
      card.className = `yokai-card ${y.is_unlocked ? "" : "locked"}`;

      const avatar = y.is_unlocked ? "👹" : "❓";
      const name = y.is_unlocked ? y.name.split(" ")[0] : "미확인 요괴";
      const elem = y.is_unlocked ? `${y.saju_element} · ${y.country}` : "잠김";

      card.innerHTML = `
        <div class="yokai-avatar">${avatar}</div>
        <div class="yokai-name">${name}</div>
        <div class="yokai-element">${elem}</div>
      `;

      // 해금된 요괴만 클릭 시 상세 모달 오픈
      if (y.is_unlocked) {
        card.onclick = () => openYokaiDetail(y);
      }
      grid.appendChild(card);
    });
  } catch (err) {
    console.error("도감 로드 오류:", err);
  }
}

// 요괴 상세 모달 데이터 채우기 및 열기
function openYokaiDetail(y) {
  document.getElementById("detName").innerText = y.name;
  document.getElementById("detOrigin").innerText = `${y.country} 전설 및 민담`;
  document.getElementById("detElement").innerText = `속성: ${y.saju_element}`;
  document.getElementById("detEmotion").innerText =
    `상징 정서: ${y.plutchik_ko}`;
  document.getElementById("detStory").innerText =
    y.story || "전해 내려오는 상세 설화 내용이 기록되어 있습니다.";
  document.getElementById("detDialogue").innerText =
    `"${y.narrative_dialogue}"`;
  document.getElementById("detAction").innerText = y.micro_action;

  document.getElementById("detailModal").classList.add("active");
}