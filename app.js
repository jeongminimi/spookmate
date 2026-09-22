// ============================================================================
// 전역 변수 및 안전 날짜 초기화 (로컬 / 웹 배포 환경 자동 분기)
// ============================================================================
const isLocal =
  window.location.hostname === "127.0.0.1" ||
  window.location.hostname === "localhost";

const API_BASE = isLocal
  ? "http://127.0.0.1:8000/api"
  : "https://spookmate-backend.onrender.com/api";

const todayObj = new Date();
let currentYear = todayObj.getFullYear();
let currentMonth = todayObj.getMonth() + 1;
let shrinkTimer = null; // 5초 요괴 축소 타이머

// ============================================================================
// 1. 앱 시작 시 닉네임 체크 및 사용자 기록 동기화
// ============================================================================
window.addEventListener("DOMContentLoaded", () => {
  const savedUserId = localStorage.getItem("spookmate_user_id");
  const userInput = document.getElementById("userIdInput");
  const modalInput = document.getElementById("modalNicknameInput");

  const dateInput = document.getElementById("diaryDate");
  if (dateInput) {
    const yyyy = todayObj.getFullYear();
    const mm = String(todayObj.getMonth() + 1).padStart(2, "0");
    const dd = String(todayObj.getDate()).padStart(2, "0");
    dateInput.value = `${yyyy}-${mm}-${dd}`;
  }

  if (modalInput) {
    modalInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") confirmNickname();
    });
  }

  if (!savedUserId) {
    openLoginModal();
  } else {
    if (userInput) userInput.value = savedUserId;
    loadCalendar(currentYear, currentMonth);
    loadCompendium(savedUserId);
  }
});

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

function confirmNickname() {
  const modalInput = document.getElementById("modalNicknameInput");
  const userInput = document.getElementById("userIdInput");
  const modal = document.getElementById("loginModal");

  const newId = modalInput?.value.trim() || "마포구 보안관";

  localStorage.setItem("spookmate_user_id", newId);
  if (userInput) userInput.value = newId;

  if (modal) modal.classList.remove("active");

  loadCalendar(currentYear, currentMonth);
  loadCompendium(newId);
}

// ============================================================================
// 2. UI 제어 함수
// ============================================================================
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

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove("active");
  if (shrinkTimer) clearTimeout(shrinkTimer);
}

// ============================================================================
// 3. 일기 작성 및 비동기 API 통신 (문틈 슬라이딩 애니메이션 1초 보장)
// ============================================================================
async function handleDiarySubmit(e) {
  e.preventDefault();

  const userId =
    document.getElementById("userIdInput")?.value.trim() ||
    localStorage.getItem("spookmate_user_id") ||
    "user_01";
  const diaryDate = document.getElementById("diaryDate").value;
  const rawEntry = document.getElementById("rawEntry").value.trim();
  const submitBtn = document.getElementById("submitBtn");
  const paperSlipArea = document.getElementById("paperSlipArea");

  if (!rawEntry) {
    alert("털어놓을 넋두리를 적어주세요.");
    return;
  }

  // 1. 문틈 아래로 종이가 쏙 빨려 들어가는 3D 애니메이션 가동
  submitBtn.disabled = true;
  submitBtn.innerText = "문틈 아래로 하소연 빨려들어가는 중...";
  if (paperSlipArea) paperSlipArea.classList.add("slipping");

  try {
    // 2. 백엔드 통신과 최소 1.0초의 슬라이딩 시각 효과를 병렬 보장
    const fetchPromise = fetch(`${API_BASE}/diary/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        diary_date: diaryDate,
        raw_entry: rawEntry,
      }),
    });

    const [res] = await Promise.all([
      fetchPromise,
      new Promise((resolve) => setTimeout(resolve, 1000)),
    ]);

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `서버 에러 상태 코드: ${res.status}`);
    }

    const data = await res.json();

    // 3. 대형 요괴 선(先)강조 출현 (5초 후 축소 시퀀스 포함)
    showYokaiHeroReveal(data);

    // 4. 입력창 리셋 및 종이 위치 원상 복구
    document.getElementById("rawEntry").value = "";
    if (paperSlipArea) paperSlipArea.classList.remove("slipping");

    // 달력 및 도감 실시간 동기화
    loadCalendar(currentYear, currentMonth);
    loadCompendium(userId);
  } catch (err) {
    console.error("Diary Submit Error:", err);
    if (paperSlipArea) paperSlipArea.classList.remove("slipping");
    alert(`배달 실패!\n원인: ${err.message}`);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerText = "문틈 아래로 하소연 밀어넣기";
  }
}

// ============================================================================
// 4. 요괴 선(先)강조 출현 -> 5초 후 축소 및 쪽지 노출 시퀀스
// ============================================================================
function showYokaiHeroReveal(serverData) {
  const modal = document.getElementById("resultModal");
  const stage = document.getElementById("modalYokaiStage");
  const details = document.getElementById("modalDetails");
  const eatingStatus = document.getElementById("eatingStatus");
  const yokaiImg = document.getElementById("modalYokaiImg");
  const matched = serverData.eaten_by_yokai;

  if (shrinkTimer) clearTimeout(shrinkTimer);

  // 1단계: 초기화 - 대형 일러스트 모드로 세팅하고 글씨 영역 숨김
  stage.classList.remove("settled");
  details.classList.remove("revealed");
  if (eatingStatus) eatingStatus.style.display = "block";

  // 요괴 이미지 및 기본 정보 바인딩 (img 폴더 경로 지정)
  if (yokaiImg) {
    yokaiImg.src = `img/${matched.id}.png`;
    yokaiImg.alt = matched.name;
  }
  document.getElementById("modalYokaiName").innerText = matched.name;
  document.getElementById("modalYokaiMeta").innerText =
    `${matched.country} 전승 | 상징: ${matched.plutchik_ko || serverData.analysis.emotion_tag}`;

  // 쪽지 텍스트 데이터 바인딩
  const matchRate = matched.match_rate || 90;
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

  // 모달 열기
  modal.classList.add("active");

  // 2단계: 정확히 5초(5000ms) 동안 대형 일러스트 강조 후 축소 & 쪽지 노출
  let remainingSeconds = 5;
  const countdownInterval = setInterval(() => {
    remainingSeconds--;
    if (remainingSeconds > 0 && eatingStatus) {
      eatingStatus.innerText = `스푹메이트가 요괴의 원혼을 씹어 삼키는 중... (${remainingSeconds}초)`;
    } else {
      clearInterval(countdownInterval);
    }
  }, 1000);

  shrinkTimer = setTimeout(() => {
    // 5초 경과: 요괴 일러스트가 상단 액자로 축소
    stage.classList.add("settled");
    if (eatingStatus) eatingStatus.style.display = "none";

    // 0.25초 뒤 문틈 쪽지 내용(대사 및 처방전)이 스르륵 등장
    setTimeout(() => {
      details.classList.add("revealed");
    }, 250);
  }, 5000);
}

// ============================================================================
// 5. 월간 캘린더 (월세 대장)
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

  const dayNames = ["일", "월", "화", "수", "목", "금", "토"];
  dayNames.forEach((d) => {
    const el = document.createElement("div");
    el.className = "day-name";
    el.innerText = d;
    grid.appendChild(el);
  });

  try {
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

    for (let i = 0; i < firstDay; i++) {
      const emptyCell = document.createElement("div");
      emptyCell.className = "day-cell empty";
      grid.appendChild(emptyCell);
    }

    const todayStr = `${todayObj.getFullYear()}-${String(todayObj.getMonth() + 1).padStart(2, "0")}-${String(todayObj.getDate()).padStart(2, "0")}`;

    for (let date = 1; date <= lastDate; date++) {
      const dateStr = `${year}-${String(month).padStart(2, "0")}-${String(date).padStart(2, "0")}`;
      const cell = document.createElement("div");
      cell.className = "day-cell";

      const isToday = dateStr === todayStr;
      if (isToday) cell.classList.add("today");

      cell.innerHTML = `<span class="day-number">${date}</span>`;

      if (stampMap[dateStr]) {
        const s = stampMap[dateStr];
        cell.innerHTML += `
          <div class="stamp-badge">완식</div>
          <div class="stamp-tag">${s.emotion_tag}</div>
        `;
        cell.title = `[하소연 내용] ${s.raw_entry}`;
      }

      grid.appendChild(cell);
    }
  } catch (err) {
    console.error("Calendar Load Error:", err);
  }
}

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
// 6. 73종 요괴 도감 (img 폴더 경로 적용)
// ============================================================================
async function loadCompendium(userId) {
  try {
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

      // img 폴더 내의 요괴 일러스트 연결
      const avatarHtml = y.is_unlocked
        ? `<img src="img/${y.id}.png" alt="${y.name}" onerror="this.style.display='none';">`
        : `<span style="font-size: 1.2rem; color: #555;">?</span>`;

      const displayName = y.is_unlocked ? y.name.split(" ")[0] : "미확인 악령";
      const displaySub = y.is_unlocked ? y.plutchik_ko : "봉인됨";

      card.innerHTML = `
        <div class="yokai-avatar">${avatarHtml}</div>
        <div class="yokai-name">${displayName}</div>
        <div class="yokai-element">${displaySub}</div>
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

function openYokaiDetail(y) {
  const detImg = document.getElementById("detAvatarImg");
  if (detImg) {
    detImg.style.display = "block";
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
