// ============================================================================
// 전역 변수 및 안전 날짜 초기화 (로컬 / 웹 배포 환경 자동 분기)
// ============================================================================
const isLocal =
  window.location.hostname === "127.0.0.1" ||
  window.location.hostname === "localhost";

// 로컬 환경이면 8000 포트 호출, 배포된 웹사이트면 Render 클라우드 백엔드 호출
const API_BASE = isLocal
  ? "http://127.0.0.1:8000/api"
  : "https://spookmate-backend.onrender.com/api"; // Render 배포 후 실제 백엔드 URL로 교체

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

  // 오늘 날짜를 일기 작성 기본값으로 자동 세팅 (YYYY-MM-DD)
  const dateInput = document.getElementById("diaryDate");
  if (dateInput) {
    const yyyy = todayObj.getFullYear();
    const mm = String(todayObj.getMonth() + 1).padStart(2, "0");
    const dd = String(todayObj.getDate()).padStart(2, "0");
    dateInput.value = `${yyyy}-${mm}-${dd}`;
  }

  // 닉네임 모달 인풋창에서 엔터(Enter) 키 입력 시 확인 처리
  if (modalInput) {
    modalInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") confirmNickname();
    });
  }

  // 저장된 닉네임이 없으면 등록 모달 오픈, 있으면 즉시 데이터 로드
  if (!savedUserId) {
    openLoginModal();
  } else {
    if (userInput) userInput.value = savedUserId;
    loadCalendar(currentYear, currentMonth);
    loadCompendium(savedUserId);
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

  const newId = modalInput?.value.trim() || "마포구 보안관";

  // 로컬 스토리지 및 상단 인풋에 저장
  localStorage.setItem("spookmate_user_id", newId);
  if (userInput) userInput.value = newId;

  // 모달 닫기
  if (modal) modal.classList.remove("active");

  // 해당 닉네임 기준 달력 및 도감 기록 새로고침
  loadCalendar(currentYear, currentMonth);
  loadCompendium(newId);
}

// ============================================================================
// 2. UI 제어 함수 (탭 전환 및 모달 제어)
// ============================================================================
/**
 * 상단 탭 전환 함수
 */
function switchTab(tabName) {
  document.querySelectorAll(".tab-btn").forEach((btn, idx) => {
    btn.classList.toggle(
      "active",
      ["write", "calendar", "compendium"][idx] === tabName,
    );
  });

  document.querySelectorAll(".tab-content").forEach((content) => {
    content.classList.remove("active");
  });

  const targetTab = document.getElementById(`tab-${tabName}`);
  if (targetTab) targetTab.classList.add("active");

  const userId =
    document.getElementById("userIdInput")?.value.trim() ||
    localStorage.getItem("spookmate_user_id") ||
    "user_01";

  if (tabName === "calendar") loadCalendar(currentYear, currentMonth);
  if (tabName === "compendium") loadCompendium(userId);
}

/**
 * 팝업 모달 닫기
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

  const userId =
    document.getElementById("userIdInput")?.value.trim() ||
    localStorage.getItem("spookmate_user_id") ||
    "user_01";
  const diaryDate = document.getElementById("diaryDate").value;
  const rawEntry = document.getElementById("rawEntry").value.trim();
  const submitBtn = document.getElementById("submitBtn");

  if (!rawEntry) {
    alert("털어놓을 하소연 내용을 입력해 주세요!");
    return;
  }

  // 중복 제출 방지 처리
  submitBtn.disabled = true;
  submitBtn.innerText = "스푹이 흔들어 깨우는 중...";

  try {
    const res = await fetch(`${API_BASE}/diary/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        diary_date: diaryDate,
        raw_entry: rawEntry,
      }),
    });

    if (!res.ok) {
      // 서버에서 500 등 에러가 발생한 경우 구체적인 이유 파싱
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `서버 에러 상태 코드: ${res.status}`);
    }

    const data = await res.json();

    // 요괴 소환 애니메이션 실행
    showYokaiHeroReveal(data);

    // 입력창 초기화
    document.getElementById("rawEntry").value = "";

    // ★ 일기 저장 성공 즉시 달력과 도감 현황 동기화
    loadCalendar(currentYear, currentMonth);
    loadCompendium(userId);
  } catch (err) {
    console.error("Diary Submit Error:", err);
    alert(`스푹이 소환 실패!\n원인: ${err.message}`);
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

  // 모달 초기화
  modalDetails.classList.remove("reveal");
  if (fallbackEmoji) fallbackEmoji.style.display = "none";

  if (yokaiImg) {
    yokaiImg.classList.remove("zoomed");
    yokaiImg.style.display = "inline-block";
    yokaiImg.className = "modal-yokai-img glitch-summon";
    yokaiImg.src = `img/${matched.id}.png`;
    yokaiImg.alt = matched.name;

    yokaiImg.onclick = function () {
      if (this.classList.contains("glitch-summon")) return;
      this.classList.toggle("zoomed");
    };
  }

  // 텍스트 데이터 바인딩
  document.getElementById("modalYokaiName").innerText =
    `${matched.name} (${matched.country})`;
  document.getElementById("modalEmotionTag").innerText = isPositive
    ? `#${serverData.analysis.emotion_tag} 에너지를 흡수해 요괴가 힘을 얻었습니다!`
    : `#${serverData.analysis.emotion_tag} 감정을 시원하게 먹어치웠습니다!`;

  // [입맛 싱크로율 XX%] 대사 접두사 및 파이썬 튜플 잔여물 정제 (버그 수정)
  const matchRate = matched.match_rate || 92;
  let quote = (matched.comfort_quote || "").trim();
  quote = quote.replace(/^\s*\(?['"]?/, "").replace(/['"]?,?\s*\)?$/, "");

  if (/^\[.*?\]/.test(quote)) {
    quote = quote.replace(/^\[.*?\]\s*/, `[입맛 싱크로율 ${matchRate}%] `);
  } else if (!quote.startsWith("[입맛 싱크로율")) {
    quote = `[입맛 싱크로율 ${matchRate}%] ${quote}`;
  }

  document.getElementById("modalDialogue").innerText = `"${quote}"`;
  document.getElementById("modalAlternative").innerText =
    serverData.analysis.alternative_thought;
  document.getElementById("modalAction").innerText = matched.micro_action;

  // 모달 오픈
  modal.classList.add("active");

  // 0.7초 뒤 기본 크기 안착
  setTimeout(() => {
    if (yokaiImg) {
      yokaiImg.className = "modal-yokai-img glitch-settled";
    }
  }, 700);

  // 1.05초 뒤 말풍선 및 CBT 처방전 등장
  setTimeout(() => {
    modalDetails.classList.add("reveal");
  }, 1050);
}

// ============================================================================
// 5. 월간 캘린더 렌더링 (오늘 날짜 강조 & 감정 스탬프 표시)
// ============================================================================
async function loadCalendar(year, month) {
  const userId =
    document.getElementById("userIdInput")?.value.trim() ||
    localStorage.getItem("spookmate_user_id") ||
    "user_01";
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
    // URL 인코딩 처리(encodeURIComponent)로 한글/공백 ID 보호
    const res = await fetch(
      `${API_BASE}/calendar?user_id=${encodeURIComponent(userId)}&year=${year}&month=${month}`,
    );
    const data = await res.json();
    const stampMap = {};
    if (data.stamps) {
      data.stamps.forEach((s) => {
        stampMap[s.diary_date] = s;
      });
    }

    const firstDay = new Date(year, month - 1, 1).getDay();
    const lastDate = new Date(year, month, 0).getDate();

    // 시작 전 빈 칸 생성
    for (let i = 0; i < firstDay; i++) {
      const emptyCell = document.createElement("div");
      emptyCell.className = "day-cell empty";
      grid.appendChild(emptyCell);
    }

    const todayStr = `${todayObj.getFullYear()}-${String(todayObj.getMonth() + 1).padStart(2, "0")}-${String(todayObj.getDate()).padStart(2, "0")}`;

    // 날짜 셀 채우기
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
    // URL 인코딩 처리(encodeURIComponent)
    const res = await fetch(
      `${API_BASE}/compendium?user_id=${encodeURIComponent(userId)}`,
    );
    const data = await res.json();

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
