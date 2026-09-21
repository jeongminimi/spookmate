// ============================================================================
// 전역 변수 및 안전 날짜 초기화 (로컬 / 웹 배포 환경 자동 분기)
// ============================================================================
// 현재 접속 환경이 로컬(내 컴퓨터)인지 확인
const isLocal =
  window.location.hostname === "127.0.0.1" ||
  window.location.hostname === "localhost";

// 로컬 환경이면 8000 포트 호출, 배포된 웹사이트면 Render 클라우드 백엔드 호출
const API_BASE = isLocal
  ? "http://127.0.0.1:8000/api"
  : "https://spookmate-backend.onrender.com/api"; // ★ 나중에 Render 배포 후 생성된 실제 주소로 교체할 자리

const todayObj = new Date();
let currentYear = todayObj.getFullYear();
let currentMonth = todayObj.getMonth() + 1;

// ============================================================================
// 1. 앱 시작 시 닉네임 체크 및 사용자 기록 동기화
// ============================================================================
window.addEventListener("DOMContentLoaded", () => {
  const savedUserId = localStorage.getItem("spookmate_user_id");
  const userInput = document.getElementById("userIdInput");
  const modalInput = document.getElementById("modalNicknameInput");

  // 1) 오늘 날짜를 일기 작성 기본값으로 자동 세팅 (YYYY-MM-DD)
  const dateInput = document.getElementById("diaryDate");
  if (dateInput) {
    const yyyy = todayObj.getFullYear();
    const mm = String(todayObj.getMonth() + 1).padStart(2, "0");
    const dd = String(todayObj.getDate()).padStart(2, "0");
    dateInput.value = `${yyyy}-${mm}-${dd}`;
  }

  // 2) 닉네임 모달 인풋창에서 엔터(Enter) 키 입력 시 확인 처리
  if (modalInput) {
    modalInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") confirmNickname();
    });
  }

  // 3) 브라우저에 저장된 닉네임이 없으면 모달 띄우기, 있으면 데이터 로드
  if (!savedUserId) {
    openLoginModal();
  } else {
    if (userInput) userInput.value = savedUserId;
    loadCalendar(currentYear, currentMonth);
    if (typeof loadCompendium === "function") {
      loadCompendium(savedUserId);
    }
  }
});

/**
 * 닉네임 등록 모달 열기
 */
function openLoginModal() {
  const modal = document.getElementById("loginModal");
  const modalInput = document.getElementById("modalNicknameInput");
  const savedUserId = localStorage.getItem("spookmate_user_id") || "";

  if (modalInput) {
    modalInput.value = savedUserId;
    setTimeout(() => modalInput.focus(), 150);
  }
  if (modal) modal.classList.add("active");
}

/**
 * 닉네임 등록 확인 및 데이터 즉시 동기화
 */
function confirmNickname() {
  const modalInput = document.getElementById("modalNicknameInput");
  const userInput = document.getElementById("userIdInput");
  const modal = document.getElementById("loginModal");

  const newId = modalInput?.value.trim() || "방구석요괴";

  // 로컬 스토리지 및 상단 인풋에 저장
  localStorage.setItem("spookmate_user_id", newId);
  if (userInput) userInput.value = newId;

  // 모달 닫기
  if (modal) modal.classList.remove("active");

  // 해당 닉네임 기준 달력 및 도감 기록 새로고침
  loadCalendar(currentYear, currentMonth);
  if (typeof loadCompendium === "function") {
    loadCompendium(newId);
  }
}

// ============================================================================
// 2. UI 제어 함수 (탭 전환 및 모달 제어)
// ============================================================================
/**
 * 상단 탭 전환 함수
 * @param {'write' | 'calendar' | 'compendium'} tabName
 */
function switchTab(tabName) {
  // 1. 상단 탭 버튼 active 클래스 동기화
  document.querySelectorAll(".tab-btn").forEach((btn, idx) => {
    btn.classList.toggle(
      "active",
      ["write", "calendar", "compendium"][idx] === tabName,
    );
  });

  // 2. 모든 탭 섹션 숨김 후 대상 탭만 활성화
  document.querySelectorAll(".tab-content").forEach((content) => {
    content.classList.remove("active");
  });

  const targetTab = document.getElementById(`tab-${tabName}`);
  if (targetTab) targetTab.classList.add("active");

  // 3. 탭 진입 시 최신 데이터 실시간 패치
  const userId =
    document.getElementById("userIdInput")?.value.trim() || "user_01";
  if (tabName === "calendar") loadCalendar(currentYear, currentMonth);
  if (tabName === "compendium") loadCompendium(userId);
}

/**
 * 팝업 모달 닫기
 * @param {string} modalId
 */
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove("active");
}

// ============================================================================
// 3. 일기 작성 및 비동기 API 통신
// ============================================================================
/**
 * 하소연 제출 처리 이벤트 핸들러
 */
async function handleDiarySubmit(e) {
  e.preventDefault();

  const userId = document.getElementById("userIdInput").value.trim();
  const diaryDate = document.getElementById("diaryDate").value;
  const rawEntry = document.getElementById("rawEntry").value.trim();
  const submitBtn = document.getElementById("submitBtn");

  // 중복 제출 방지 처리
  submitBtn.disabled = true;
  submitBtn.innerText = "스푹이 흔들어 깨우는 중...";

  try {
    // 백엔드 FastAPI 매칭 엔진 호출
    const res = await fetch(`${API_BASE}/diary/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        diary_date: diaryDate,
        raw_entry: rawEntry,
      }),
    });

    if (!res.ok) throw new Error(`HTTP Error: ${res.status}`);
    const data = await res.json();

    // 요괴 이미지 선(先)강조 확대 -> 축소 안착 -> 글씨 생성 시퀀스 실행
    showYokaiHeroReveal(data);

    // 입력창 초기화
    document.getElementById("rawEntry").value = "";
  } catch (err) {
    alert(
      "스푹이 소환에 실패했습니다. 백엔드 서버(uvicorn) 상태를 확인해 주세요.",
    );
    console.error("Diary Submit Error:", err);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerText = "SpookMate에게 하소연 폭격하기";
  }
}

// ============================================================================
// 4. 요괴 차원 균열 소환 & 클릭 시 확대/축소 시퀀스
// ============================================================================
function showYokaiHeroReveal(serverData) {
  const modal = document.getElementById("resultModal");
  const yokaiImg = document.getElementById("modalYokaiImg");
  const fallbackEmoji = document.getElementById("modalFallbackEmoji");
  const modalDetails = document.getElementById("modalDetails");

  const matched = serverData.eaten_by_yokai;
  const isPositive = (serverData.analysis?.valence ?? 3.0) >= 5.0;

  // 1. 모달 초기화 (확대 상태 및 텍스트 리셋)
  modalDetails.classList.remove("reveal");
  if (fallbackEmoji) fallbackEmoji.style.display = "none";

  if (yokaiImg) {
    yokaiImg.classList.remove("zoomed"); // 이전 확대 상태 해제
    yokaiImg.style.display = "inline-block";
    yokaiImg.className = "modal-yokai-img glitch-summon"; // 1.4배 확대 + 고주파 진동 소환
    yokaiImg.src = `img/${matched.id}.png`;
    yokaiImg.alt = matched.name;

    // 요괴 이미지 클릭 시 확대/축소 토글 이벤트
    yokaiImg.onclick = function () {
      if (this.classList.contains("glitch-summon")) return; // 소환 중엔 클릭 방지
      this.classList.toggle("zoomed");
    };
  }

  // 2. 텍스트 데이터 바인딩
  document.getElementById("modalYokaiName").innerText =
    `${matched.name} (${matched.country})`;
  document.getElementById("modalEmotionTag").innerText = isPositive
    ? `#${serverData.analysis.emotion_tag} 에너지를 흡수해 요괴가 힘을 얻었습니다!`
    : `#${serverData.analysis.emotion_tag} 감정을 시원하게 먹어치웠습니다!`;

  // [입맛 싱크로율 XX%] 대사 접두사 처리 및 튜플 괄호 찌꺼기 정제
  const matchRate = matched.match_rate || 92;
  let quote = (matched.comfort_quote || "").trim();
  quote = quote
    .replace(/^(\(\s*['"]?\vert{}['"]?\s*\))/g, "")
    .replace(/['"],?\s*\)$/, "");

  if (/^\[.*?\]/.test(quote)) {
    quote = quote.replace(/^\[.*?\]\s*/, `[입맛 싱크로율 ${matchRate}%] `);
  } else if (!quote.startsWith("[입맛 싱크로율")) {
    quote = `[입맛 싱크로율 ${matchRate}%] ${quote}`;
  }

  document.getElementById("modalDialogue").innerText = `"${quote}"`;
  document.getElementById("modalAlternative").innerText =
    serverData.analysis.alternative_thought;
  document.getElementById("modalAction").innerText = matched.micro_action;

  // 3. 모달 오픈
  modal.classList.add("active");

  // 4. [0.7초 뒤] 고주파 진동 멈추고 1배율(215px) 기본 크기로 안착
  setTimeout(() => {
    if (yokaiImg) {
      yokaiImg.className = "modal-yokai-img glitch-settled";
    }
  }, 700);

  // 5. [1.05초 뒤] 말풍선 및 처방전 등장
  setTimeout(() => {
    modalDetails.classList.add("reveal");
  }, 1050);
}

// ============================================================================
// 5. 월간 캘린더 렌더링 (오늘 날짜 강조 & 감정 스탬프 표시)
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
    // 월별 스탬프(일기 기록) 목록 수신
    const res = await fetch(
      `${API_BASE}/calendar?user_id=${userId}&year=${year}&month=${month}`,
    );
    const data = await res.json();
    const stampMap = {};
    if (data.stamps) {
      data.stamps.forEach((s) => {
        stampMap[s.diary_date] = s;
      });
    }

    // 해당 월의 첫 날 요일 및 총 일수 계산
    const firstDay = new Date(year, month - 1, 1).getDay();
    const lastDate = new Date(year, month, 0).getDate();

    // 1일 시작 전 빈 칸 생성
    for (let i = 0; i < firstDay; i++) {
      const emptyCell = document.createElement("div");
      emptyCell.className = "day-cell empty";
      grid.appendChild(emptyCell);
    }

    // 시스템 실제 오늘 날짜(YYYY-MM-DD)
    const todayStr = `${todayObj.getFullYear()}-${String(todayObj.getMonth() + 1).padStart(2, "0")}-${String(todayObj.getDate()).padStart(2, "0")}`;

    // 1일부터 마지막 날까지 날짜 셀 생성
    for (let date = 1; date <= lastDate; date++) {
      const dateStr = `${year}-${String(month).padStart(2, "0")}-${String(date).padStart(2, "0")}`;
      const cell = document.createElement("div");
      cell.className = "day-cell";

      const isToday = dateStr === todayStr;
      if (isToday) cell.classList.add("today");

      cell.innerHTML = `
        <div class="date-header">
          <span class="day-number">${date}</span>
          ${isToday ? '<span class="today-badge">오늘</span>' : ""}
        </div>
      `;

      // 작성된 일기가 있는 날은 요괴 뱃지 및 감정 태그 각인
      if (stampMap[dateStr]) {
        const s = stampMap[dateStr];
        cell.innerHTML += `
          <div class="stamp-badge">👹 ${s.yokai_name.split(" ")[0]}</div>
          <div class="stamp-tag">${s.emotion_tag}</div>
        `;
        cell.title = `[일기 내용] ${s.raw_entry}`;
      }

      grid.appendChild(cell);
    }
  } catch (err) {
    console.error("Calendar Load Error:", err);
  }
}

/**
 * 캘린더 월 이동
 * @param {number} delta -1(이전 달) 또는 1(다음 달)
 */
function changeMonth(delta) {
  currentMonth += delta;
  if (currentMonth < 1) {
    currentMonth = 12;
    currentYear--;
  } else if (currentMonth > 12) {
    currentMonth = 1;
    currentYear++;
  }
  loadCalendar(currentYear, currentMonth);
}

// ============================================================================
// 6. 요괴 도감 렌더링 & 상세 정보 모달 바인딩
// ============================================================================
async function loadCompendium(userId) {
  try {
    const res = await fetch(`${API_BASE}/compendium?user_id=${userId}`);
    const data = await res.json();

    // 1. 도감 게이지 및 수집률 카운트 업데이트
    const unlockCountEl = document.getElementById("unlockCount");
    const totalCountEl = document.getElementById("totalCount");
    const collectPercentEl = document.getElementById("collectPercent");
    const progressBar = document.getElementById("progressBar");

    if (unlockCountEl) unlockCountEl.innerText = data.unlocked_count;
    if (totalCountEl) totalCountEl.innerText = data.total_count;
    if (collectPercentEl)
      collectPercentEl.innerText = `${data.collection_rate}%`;
    if (progressBar) progressBar.style.width = `${data.collection_rate}%`;

    const grid = document.getElementById("compendiumGrid");
    if (!grid) return;
    grid.innerHTML = "";

    // 2. 도감 카드 목록 렌더링 (img/ 폴더의 이미지 바인딩)
    data.compendium.forEach((y) => {
      const card = document.createElement("div");
      card.className = `yokai-card ${y.is_unlocked ? "" : "locked"}`;

      const avatarHtml = y.is_unlocked
        ? `<img src="img/${y.id}.png" alt="${y.name}" onerror="this.style.display='none'; this.parentElement.innerText='👹';">`
        : `<span style="font-size: 1.4rem;">❓</span>`;

      const displayName = y.is_unlocked ? y.name.split(" ")[0] : "미확인 요괴";
      const displaySub = y.is_unlocked ? `${y.country} 전설` : "잠김";

      card.innerHTML = `
        <div class="yokai-avatar">${avatarHtml}</div>
        <div class="yokai-name">${displayName}</div>
        <div class="yokai-element" style="color: var(--accent-gold); font-size: 0.72rem;">${displaySub}</div>
      `;

      if (y.is_unlocked) {
        card.onclick = () => openYokaiDetail(y);
      }
      grid.appendChild(card);
    });
  } catch (err) {
    console.error("Compendium Load Error:", err);
  }
}

/**
 * 도감 카드 클릭 시 상세 정보 모달 채우기
 * @param {object} y 선택된 요괴 도감 객체
 */
function openYokaiDetail(y) {
  const detImg = document.getElementById("detAvatarImg");
  const detFallback = document.getElementById("detFallbackEmoji");
  if (detImg) {
    detImg.style.display = "block";
    if (detFallback) detFallback.style.display = "none";
    detImg.src = `img/${y.id}.png`;
    detImg.alt = y.name;
  }

  document.getElementById("detName").innerText = y.name;
  document.getElementById("detOrigin").innerText = `${y.country} 전승 설화`;
  document.getElementById("detEmotion").innerText =
    `상징 정서: ${y.plutchik_ko}`;
  document.getElementById("detStory").innerText =
    y.story || "기록된 전승 설화가 없습니다.";
  document.getElementById("detDialogue").innerText =
    `"${y.narrative_dialogue}"`;
  document.getElementById("detAction").innerText = y.micro_action;

  document.getElementById("detailModal").classList.add("active");
}
