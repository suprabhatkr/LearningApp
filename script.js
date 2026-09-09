// State variables
const API_URL = ""; // Relative URL since frontend is served directly by FastAPI
let authToken = localStorage.getItem("jwt_token") || null;
let currentUser = null;
let currentProblemId = null;
let currentChapterId = null;
let currentQuizId = null;
let currentAiChapterId = null;
let currentHldBookChapterId = null;
let currentLldBookChapterId = null;
let currentBackendGuideId = null;
let leetcodeQuestions = [];
let trackerItems = [];
let hldBookData = null;
let lldBookData = null;
let lldBookTaskState = {};
let backendLearningData = null;
let backendLabDomains = [];
let currentBackendTopicId = null;
let currentBackendTopicDetail = null;
let backendCompletedTopics = new Set();
let aiReferences = [];

// DOM Elements
const toast = document.querySelector('.toast');
const sidebarLinks = document.querySelectorAll('.sidebar nav a');
const tabContents = document.querySelectorAll('.tab-content');
const crumbStrong = document.querySelector('#current-tab-label');

// Helpers
const showToast = (message) => {
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
};

function applySidebarState(collapsed, persist = true) {
  document.body.classList.toggle('sidebar-collapsed', collapsed);
  const toggleBtn = document.querySelector('#sidebar-toggle-btn');
  if (toggleBtn) {
    toggleBtn.textContent = collapsed ? "»" : "«";
    toggleBtn.setAttribute("aria-label", collapsed ? "Expand sidebar" : "Collapse sidebar");
  }
  if (persist) {
    localStorage.setItem("sidebar_collapsed", collapsed ? "1" : "0");
  }
}

function toggleSidebar() {
  const collapsed = !document.body.classList.contains('sidebar-collapsed');
  applySidebarState(collapsed, true);
}

// Auto-Authentication on Startup
async function authenticateUser() {
  const username = "senior_candidate";
  const password = "password123";
  const statusPill = document.querySelector('#auth-status-pill');

  try {
    if (!authToken) {
      statusPill.textContent = "Registering default profile...";
      // 1. Try to register
      const regRes = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });
      
      // 2. Obtain token (whether newly registered or already exists)
      statusPill.textContent = "Obtaining access token...";
      const tokenRes = await fetch(`${API_URL}/api/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });

      if (!tokenRes.ok) throw new Error("Authentication failed");
      
      const data = await tokenRes.json();
      authToken = data.access_token;
      localStorage.setItem("jwt_token", authToken);
    }

    // 3. Fetch User profile to confirm active token
    const meRes = await fetch(`${API_URL}/api/auth/me`, {
      headers: { "Authorization": `Bearer ${authToken}` }
    });

    if (!meRes.ok) {
      // Stale token, clear it and retry
      localStorage.removeItem("jwt_token");
      authToken = null;
      return authenticateUser();
    }

    currentUser = await meRes.json();
    document.querySelector('#user-display').textContent = currentUser.username;
    statusPill.textContent = "● Sandbox Active";
    statusPill.className = "status-indicator-bar connected";
    
    // Initialise UI components
    updateDashboardMetrics();
    loadDsaProblems();
    loadDsaSyllabus();
    loadSystemDesignChapters();
    loadSystemDesignExamples();
    loadHldBookChapters();
    loadLldBookChapters();
    loadTrackerItems();
    loadBackendLearningChapters();
    loadBackendLabSyllabus();
    loadBackendLabProgress();
    loadLldTheory();
    loadLldQuizzes();
    loadAiChapters();
    updateDbLabStatus();
    loadLeetcodeQuestions();

  } catch (err) {
    console.error("Auth error:", err);
    statusPill.textContent = "● Offline Mode";
    statusPill.className = "status-indicator-bar";
    showToast("Server offline. Connect to backend to unlock interactive execution.");

    // Initialise UI components with static/fallback data for offline mode
    loadDsaProblems();
    loadDsaSyllabus();
    loadSystemDesignChapters();
    loadSystemDesignExamples();
    loadHldBookChapters();
    loadLldBookChapters();
    loadTrackerItems();
    loadBackendLearningChapters();
    loadBackendLabSyllabus();
    loadBackendLabProgress();
    loadLldTheory();
    loadLldQuizzes();
    loadAiChapters();
    updateDbLabStatus();
    loadLeetcodeQuestions();
  }
}

// Global Headers Fetch Wrapper
async function authenticatedFetch(url, options = {}) {
  options.headers = options.headers || {};
  if (authToken) {
    options.headers["Authorization"] = `Bearer ${authToken}`;
  }
  return fetch(url, options);
}

// Navigation Tabs Switcher
function switchTab(targetId) {
  tabContents.forEach(content => {
    content.style.display = content.id === targetId ? "block" : "none";
  });
  
  sidebarLinks.forEach(link => {
    if (link.dataset.target === targetId) {
      link.classList.add('active');
      crumbStrong.textContent = link.querySelector('span').textContent;
    } else {
      link.classList.remove('active');
    }
  });

  // Special cases when entering tabs
  if (targetId === "lab-section") {
    updateDbLabStatus();
    loadBackendLearningChapters();
    loadBackendLabSyllabus();
    loadBackendLabProgress();
  } else if (targetId === "tracker-section") {
    loadTrackerItems();
  } else if (targetId === "leetcode-section") {
    if (!leetcodeQuestions || leetcodeQuestions.length === 0) {
      loadLeetcodeQuestions();
    } else {
      filterLeetcodeQuestions();
    }
  }
}

// Bind Navigation Clicks
sidebarLinks.forEach(link => {
  link.onclick = (e) => {
    e.preventDefault();
    const target = link.dataset.target;
    switchTab(target);
  };
});

// Update Dashboard Statistics
async function updateDashboardMetrics() {
  if (!currentUser) return;
  document.querySelector('#readiness-val').innerHTML = `${Math.round(currentUser.readiness_score)}<span>%</span>`;
  
  // Calculate modules completed
  try {
    // In a full implementation, we could query user achievements.
    // For now we calculate from UI states or display dynamically.
  } catch (e) {}
}

// Reset candidate progress utility
async function resetProgress() {
  localStorage.removeItem("jwt_token");
  authToken = null;
  showToast("Resetting sandbox profile context...");
  setTimeout(() => window.location.reload(), 800);
}


/* ==========================================
   1. DSA PRACTICE CONTROLLER
   ========================================== */
let dsaProblems = [];
let dsaSyllabusData = {};

async function loadDsaSyllabus() {
  try {
    const res = await fetch(`${API_URL}/api/dsa/topics`);
    if (!res.ok) return;
    dsaSyllabusData = await res.json();
    showSyllabus('trees'); // Load trees by default
  } catch (err) {
    console.error("Syllabus error:", err);
  }
}

function showSyllabus(topicKey) {
  const tabs = document.querySelectorAll('.syllabus-tab');
  tabs.forEach(tab => {
    if (tab.textContent.toLowerCase().includes(topicKey)) {
      tab.classList.add('active');
    } else {
      tab.classList.remove('active');
    }
  });

  const contentBox = document.querySelector('#syllabus-content');
  const topic = dsaSyllabusData[topicKey];
  if (!topic) return;

  contentBox.innerHTML = `
    <h3>${topic.title}</h3>
    <div>${simpleMarkdownToHtml(topic.concept)}</div>
  `;
}

async function loadDsaProblems() {
  try {
    const res = await fetch(`${API_URL}/api/dsa/problems`);
    if (!res.ok) return;
    dsaProblems = await res.json();
    
    const container = document.querySelector('#problem-list-container');
    container.innerHTML = "";
    
    dsaProblems.forEach(p => {
      const card = document.createElement('button');
      card.className = "problem-card";
      card.id = `dsa-card-${p.id}`;
      card.onclick = () => selectProblem(p.id);
      card.innerHTML = `
        <h4>${p.title}</h4>
        <div class="meta-row">
          <span class="diff">${p.difficulty}</span>
          <span class="status-indicator" id="dsa-status-${p.id}">Pending</span>
        </div>
      `;
      container.appendChild(card);
    });
    
    // Auto select first problem
    if (dsaProblems.length > 0) {
      selectProblem(dsaProblems[0].id);
    }
  } catch (err) {
    console.error("DSA list load error:", err);
  }
}

function selectProblem(id) {
  currentProblemId = id;
  const problem = dsaProblems.find(p => p.id === id);
  if (!problem) return;
  
  // Highlight card
  document.querySelectorAll('.problem-card').forEach(c => c.classList.remove('active'));
  document.querySelector(`#dsa-card-${id}`).classList.add('active');
  
  // Show editor
  document.querySelector('#no-problem-selected').style.display = "none";
  document.querySelector('#problem-editor-container').style.display = "block";
  
  document.querySelector('#editor-title').textContent = problem.title;
  document.querySelector('#editor-difficulty').textContent = problem.difficulty;
  document.querySelector('#editor-description').innerHTML = simpleMarkdownToHtml(problem.description);
  
  // Set starter code
  document.querySelector('#code-editor').value = problem.starter_code;
  document.querySelector('#console-output').textContent = "Write your python solution above, and click 'Run Tests' to compile.";
}

async function submitCode() {
  if (!currentProblemId) return;
  const code = document.querySelector('#code-editor').value;
  const consoleOutput = document.querySelector('#console-output');
  
  consoleOutput.textContent = "Spawning execution process inside backend. Evaluating test cases...";
  
  try {
    const res = await authenticatedFetch(`${API_URL}/api/dsa/problems/${currentProblemId}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ problem_id: currentProblemId, code })
    });
    
    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || "Submission failed");
    }
    
    const data = await res.json();
    
    if (data.passed) {
      consoleOutput.innerHTML = `<span style="color: var(--green); font-weight: bold;">[SUCCESS]</span> ${data.message}\nRuntime: ${data.runtime_ms} ms\n\n`;
      data.details.forEach(d => {
        consoleOutput.innerHTML += `Test Case:\nInput: ${d.input}\nExpected: ${d.expected}\nActual: ${d.actual}\nResult: PASS\n`;
      });
      document.querySelector(`#dsa-status-${currentProblemId}`).textContent = "✓ Completed";
      document.querySelector(`#dsa-status-${currentProblemId}`).className = "status-indicator done";
      showToast("Problem Solved! Readiness score updated.");
      
      // Update global metrics
      currentUser.readiness_score = Math.min(100.0, currentUser.readiness_score + 2.5);
      updateDashboardMetrics();
      updateRoadmapPills();
    } else {
      consoleOutput.innerHTML = `<span style="color: var(--red); font-weight: bold;">[FAILED]</span> ${data.message}\nRuntime: ${data.runtime_ms} ms\n\n`;
      data.details.forEach(d => {
        consoleOutput.innerHTML += `Test Case Detail:\nInput: ${d.input}\nExpected: ${d.expected}\nLog Output:\n${d.actual}\n`;
      });
    }
  } catch (err) {
    consoleOutput.textContent = `Execution Error: ${err.message}`;
  }
}

function updateRoadmapPills() {
  // Solve count calculation
  const solved = document.querySelectorAll('.status-indicator.done').length;
  document.querySelector('#count').innerHTML = `${solved}<span> / 3</span>`;
  document.querySelector('#count-progress-bar').style.width = `${(solved/3)*100}%`;
  document.querySelector('#card-dsa-status').textContent = `${solved} / 3 Complete`;
}


/* ==========================================
   2. SYSTEM DESIGN CONTROLLER
   ========================================== */
let systemChapters = {};
let systemExamples = [];

async function loadSystemDesignChapters() {
  try {
    const res = await fetch(`${API_URL}/api/system-design/chapters`);
    if (!res.ok) return;
    systemChapters = await res.json();
    
    const container = document.querySelector('#sys-chapter-list');
    container.innerHTML = "";
    
    Object.keys(systemChapters).forEach(key => {
      const ch = systemChapters[key];
      const card = document.createElement('button');
      card.className = "chapter-card";
      card.id = `sys-card-${key}`;
      card.onclick = () => readChapter(key);
      card.innerHTML = `
        <h4>${ch.title}</h4>
        <div class="chapter-meta">
          <span>Module Chapter</span>
          <span class="read-status" id="sys-status-${key}">Unread</span>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (e) {
    console.error("System Design loading failed:", e);
  }
}

function readChapter(key) {
  currentChapterId = key;
  const chapter = systemChapters[key];
  if (!chapter) return;
  
  document.querySelectorAll('.chapter-card').forEach(c => c.classList.remove('active'));
  document.querySelector(`#sys-card-${key}`).classList.add('active');
  
  document.querySelector('#no-chapter-selected').style.display = "none";
  document.querySelector('#chapter-reader').style.display = "block";
  
  document.querySelector('#reader-title').textContent = chapter.title;
  document.querySelector('#reader-content').innerHTML = simpleMarkdownToHtml(chapter.content);
  document.querySelector('#reader-case-study').textContent = chapter.example_case;
  
  const statusLabel = document.querySelector(`#sys-status-${key}`);
  const markBtn = document.querySelector('#mark-chapter-complete-btn');
  
  if (statusLabel.textContent === "Completed") {
    markBtn.textContent = "Completed ✓";
    markBtn.className = "complete-chapter-btn done";
    markBtn.disabled = true;
  } else {
    markBtn.textContent = "Mark as Completed ✓";
    markBtn.className = "complete-chapter-btn";
    markBtn.disabled = false;
  }
}

async function markChapterComplete() {
  if (!currentChapterId) return;
  
  try {
    const res = await authenticatedFetch(`${API_URL}/api/system-design/chapters/${currentChapterId}/complete`, {
      method: "POST"
    });
    if (!res.ok) throw new Error("Completion registration failed");
    
    const data = await res.json();
    
    const statusLabel = document.querySelector(`#sys-status-${currentChapterId}`);
    statusLabel.textContent = "Completed";
    statusLabel.style.color = "var(--green)";
    
    const markBtn = document.querySelector('#mark-chapter-complete-btn');
    markBtn.textContent = "Completed ✓";
    markBtn.className = "complete-chapter-btn done";
    markBtn.disabled = true;
    
    currentUser.readiness_score = data.readiness_score;
    updateDashboardMetrics();
    
    const completedCount = Array.from(document.querySelectorAll('.read-status')).filter(x => x.textContent === "Completed").length;
    document.querySelector('#card-sys-status').textContent = `${completedCount} / 3 Complete`;
    showToast("Chapter logged to profile database!");
  } catch (err) {
    showToast(err.message);
  }
}

async function loadSystemDesignExamples() {
  try {
    const res = await fetch(`${API_URL}/api/system-design/examples`);
    if (!res.ok) return;
    systemExamples = await res.json();
    
    const tabContainer = document.querySelector('#examples-tab-bar');
    tabContainer.innerHTML = "";
    
    systemExamples.forEach((ex, idx) => {
      const btn = document.createElement('button');
      btn.className = `example-tab-btn ${idx === 0 ? 'active' : ''}`;
      btn.textContent = ex.title;
      btn.onclick = () => {
        document.querySelectorAll('.example-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        showExampleDetails(ex.id);
      };
      tabContainer.appendChild(btn);
    });
    
    if (systemExamples.length > 0) {
      showExampleDetails(systemExamples[0].id);
    }
  } catch (e) {
    console.error("System Design examples failed:", e);
  }
}

function showExampleDetails(id) {
  const ex = systemExamples.find(e => e.id === id);
  if (!ex) return;
  
  const box = document.querySelector('#example-details-box');
  box.innerHTML = `
    <h3>${ex.title}</h3>
    <div class="scale-label">Operating Scale: ${ex.scale}</div>
    <div>${simpleMarkdownToHtml(ex.design_flow)}</div>
  `;
}


/* ==========================================
   3. HLD / LLD BOOK CONTROLLER
   ========================================== */
async function loadHldBookChapters() {
  try {
    const res = await fetch(`${API_URL}/api/books/hld`);
    if (!res.ok) return;
    hldBookData = await res.json();
    const container = document.querySelector('#hld-chapter-list');
    if (!container) return;
    container.innerHTML = "";

    hldBookData.chapters.forEach(ch => {
      const card = document.createElement('button');
      card.className = "chapter-card";
      card.id = `hld-book-card-${ch.id}`;
      card.onclick = () => readHldBookChapter(ch.id);
      card.innerHTML = `
        <h4>${ch.title}</h4>
        <div class="chapter-meta">
          <span>Chapter Reader</span>
          <span>Page ${ch.pdf_page}</span>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (e) {
    console.error("HLD book loading failed:", e);
  }
}

function readHldBookChapter(chapterId) {
  if (!hldBookData) return;
  const chapter = hldBookData.chapters.find(c => c.id === chapterId);
  if (!chapter) return;
  currentHldBookChapterId = chapterId;

  document.querySelectorAll('[id^="hld-book-card-"]').forEach(c => c.classList.remove('active'));
  const selectedCard = document.querySelector(`#hld-book-card-${chapterId}`);
  if (selectedCard) selectedCard.classList.add('active');

  document.querySelector('#no-hld-selected').style.display = "none";
  document.querySelector('#hld-chapter-reader').style.display = "block";
  document.querySelector('#hld-reader-title').textContent = chapter.title;
  document.querySelector('#hld-reader-goal').textContent = chapter.chapter_goal;
  document.querySelector('#hld-pdf-viewer').src = `${API_URL}/api/books/hld/pdf#page=${chapter.pdf_page}`;

  renderQuestionsList('#hld-questions-list', chapter.questions);
}

async function loadLldBookChapters() {
  try {
    const chapterRes = await fetch(`${API_URL}/api/books/lld`);
    if (!chapterRes.ok) return;
    lldBookData = await chapterRes.json();

    const taskRes = await authenticatedFetch(`${API_URL}/api/books/lld/tasks`);
    if (taskRes.ok) {
      const tasks = await taskRes.json();
      lldBookTaskState = {};
      tasks.chapters.forEach(ch => {
        lldBookTaskState[ch.chapter_id] = ch.completed;
      });
    }

    const container = document.querySelector('#lld-book-chapter-list');
    if (!container) return;
    container.innerHTML = "";

    lldBookData.chapters.forEach(ch => {
      const isCompleted = !!lldBookTaskState[ch.id];
      const card = document.createElement('button');
      card.className = "chapter-card";
      card.id = `lld-book-card-${ch.id}`;
      card.onclick = () => readLldBookChapter(ch.id);
      card.innerHTML = `
        <h4>${ch.title}</h4>
        <div class="chapter-meta">
          <span>Page ${ch.pdf_page}</span>
          <span class="read-status" id="lld-book-status-${ch.id}" style="color:${isCompleted ? 'var(--green)' : '#666'}">${isCompleted ? 'Completed' : 'Pending'}</span>
        </div>
      `;
      container.appendChild(card);
    });
    updateLldBookProgressLabel();
  } catch (e) {
    console.error("LLD book loading failed:", e);
  }
}

function readLldBookChapter(chapterId) {
  if (!lldBookData) return;
  const chapter = lldBookData.chapters.find(c => c.id === chapterId);
  if (!chapter) return;
  currentLldBookChapterId = chapterId;

  document.querySelectorAll('[id^="lld-book-card-"]').forEach(c => c.classList.remove('active'));
  const selectedCard = document.querySelector(`#lld-book-card-${chapterId}`);
  if (selectedCard) selectedCard.classList.add('active');

  document.querySelector('#no-lld-book-selected').style.display = "none";
  document.querySelector('#lld-book-reader').style.display = "block";
  document.querySelector('#lld-book-reader-title').textContent = chapter.title;
  document.querySelector('#lld-book-reader-goal').textContent = chapter.chapter_goal;
  document.querySelector('#lld-pdf-viewer').src = `${API_URL}/api/books/lld/pdf#page=${chapter.pdf_page}`;

  renderQuestionsList('#lld-book-questions-list', chapter.questions);
  syncLldBookCompleteButtonState();
}

function syncLldBookCompleteButtonState() {
  const completed = !!lldBookTaskState[currentLldBookChapterId];
  const markBtn = document.querySelector('#mark-lld-book-complete-btn');
  if (!markBtn) return;
  if (completed) {
    markBtn.textContent = "Task Completed ✓";
    markBtn.className = "complete-chapter-btn done";
    markBtn.disabled = true;
  } else {
    markBtn.textContent = "Mark Task Completed ✓";
    markBtn.className = "complete-chapter-btn";
    markBtn.disabled = false;
  }
}

async function markLldBookChapterComplete() {
  if (!currentLldBookChapterId) return;
  try {
    const res = await authenticatedFetch(`${API_URL}/api/books/lld/chapters/${currentLldBookChapterId}/complete`, {
      method: "POST"
    });
    if (!res.ok) throw new Error("Unable to mark chapter task as completed");
    const data = await res.json();
    lldBookTaskState[currentLldBookChapterId] = true;

    const statusLabel = document.querySelector(`#lld-book-status-${currentLldBookChapterId}`);
    if (statusLabel) {
      statusLabel.textContent = "Completed";
      statusLabel.style.color = "var(--green)";
    }
    syncLldBookCompleteButtonState();
    updateLldBookProgressLabel();

    if (currentUser && data.readiness_score !== undefined) {
      currentUser.readiness_score = data.readiness_score;
      updateDashboardMetrics();
    }
    showToast("LLD chapter task completed.");
  } catch (err) {
    showToast(err.message);
  }
}

function updateLldBookProgressLabel() {
  const label = document.querySelector('#lld-book-progress-label');
  if (!label || !lldBookData) return;
  const total = lldBookData.chapters.length;
  const completed = lldBookData.chapters.filter(ch => !!lldBookTaskState[ch.id]).length;
  label.textContent = `${completed} / ${total} chapters completed`;
}

async function loadBackendLearningChapters() {
  try {
    const res = await fetch(`${API_URL}/api/books/backend-learning`);
    if (!res.ok) return;
    backendLearningData = await res.json();
    const container = document.querySelector('#backend-guide-list');
    if (!container) return;

    container.innerHTML = "";
    backendLearningData.chapters.forEach(ch => {
      const card = document.createElement('button');
      card.className = "chapter-card";
      card.id = `backend-guide-card-${ch.id}`;
      card.onclick = () => readBackendLearningChapter(ch.id);
      card.innerHTML = `
        <h4>${ch.title}</h4>
        <div class="chapter-meta">
          <span>Backend Chapter</span>
          <span>PDF Guide</span>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (e) {
    console.error("Backend learning chapters failed:", e);
  }
}

function readBackendLearningChapter(chapterId) {
  if (!backendLearningData) return;
  const chapter = backendLearningData.chapters.find(c => c.id === chapterId);
  if (!chapter) return;
  currentBackendGuideId = chapterId;

  document.querySelectorAll('[id^="backend-guide-card-"]').forEach(c => c.classList.remove('active'));
  const selectedCard = document.querySelector(`#backend-guide-card-${chapterId}`);
  if (selectedCard) selectedCard.classList.add('active');

  document.querySelector('#no-backend-guide-selected').style.display = "none";
  document.querySelector('#backend-guide-reader').style.display = "block";
  document.querySelector('#backend-guide-title').textContent = chapter.title;
  document.querySelector('#backend-guide-summary').textContent = chapter.summary;
  document.querySelector('#backend-guide-pdf-viewer').src = `${API_URL}/api/books/backend-learning/${chapterId}/pdf`;
}

function renderQuestionsList(listSelector, questions) {
  const list = document.querySelector(listSelector);
  if (!list) return;
  list.innerHTML = "";
  if (!questions || questions.length === 0) {
    list.innerHTML = "<li>No questions added yet. You can add chapter questions later.</li>";
    return;
  }
  questions.forEach(q => {
    const li = document.createElement('li');
    li.textContent = q;
    list.appendChild(li);
  });
}

function toggleBookReaderMode(bookType) {
  const selectorMap = {
    hld: { layout: '#hld-book-layout', button: '#hld-reader-expand-btn' },
    lld: { layout: '#lld-book-layout', button: '#lld-reader-expand-btn' },
    backend: { layout: '#backend-learning-layout', button: '#backend-guide-expand-btn' }
  };
  const config = selectorMap[bookType];
  if (!config) return;

  const layout = document.querySelector(config.layout);
  const button = document.querySelector(config.button);
  if (!layout || !button) return;

  layout.classList.toggle('reader-fullpage');
  const expanded = layout.classList.contains('reader-fullpage');
  button.textContent = expanded ? "Restore Layout ↙" : "Full Page ⛶";

  if (expanded) {
    layout.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}


/* ==========================================
   4. PROGRESS TRACKER CONTROLLER
   ========================================== */
async function loadTrackerItems() {
  try {
    const res = await authenticatedFetch(`${API_URL}/api/tracker/items`);
    if (!res.ok) return;
    trackerItems = await res.json();
    renderTrackerItems();
  } catch (e) {
    console.error("Tracker loading failed:", e);
  }
}

async function createTrackerItem() {
  const titleInput = document.querySelector('#tracker-title-input');
  const categoryInput = document.querySelector('#tracker-category-select');
  const targetInput = document.querySelector('#tracker-target-input');
  const notesInput = document.querySelector('#tracker-notes-input');
  if (!titleInput || !categoryInput || !targetInput || !notesInput) return;

  const title = titleInput.value.trim();
  if (!title) {
    showToast("Please enter a target or todo title.");
    return;
  }

  try {
    const res = await authenticatedFetch(`${API_URL}/api/tracker/items`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        category: categoryInput.value,
        target: targetInput.value.trim() || null,
        notes: notesInput.value.trim() || null
      })
    });
    if (!res.ok) throw new Error("Could not add tracker item");

    titleInput.value = "";
    targetInput.value = "";
    notesInput.value = "";
    await loadTrackerItems();
    showToast("Tracker item added.");
  } catch (e) {
    showToast(e.message);
  }
}

async function toggleTrackerItem(itemId, completed) {
  try {
    const res = await authenticatedFetch(`${API_URL}/api/tracker/items/${itemId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed })
    });
    if (!res.ok) throw new Error("Could not update tracker item");
    await loadTrackerItems();
  } catch (e) {
    showToast(e.message);
  }
}

async function deleteTrackerItem(itemId) {
  try {
    const res = await authenticatedFetch(`${API_URL}/api/tracker/items/${itemId}`, {
      method: "DELETE"
    });
    if (!res.ok) throw new Error("Could not delete tracker item");
    await loadTrackerItems();
  } catch (e) {
    showToast(e.message);
  }
}

function renderTrackerItems() {
  const list = document.querySelector('#tracker-items-list');
  const openCount = document.querySelector('#tracker-open-count');
  const doneCount = document.querySelector('#tracker-done-count');
  if (!list || !openCount || !doneCount) return;

  const open = trackerItems.filter(x => !x.completed).length;
  const done = trackerItems.filter(x => x.completed).length;
  openCount.textContent = `${open} open`;
  doneCount.textContent = `${done} done`;

  if (!trackerItems.length) {
    list.innerHTML = `<p class="placeholder-text">Add your first target to start tracking progress.</p>`;
    return;
  }

  list.innerHTML = trackerItems.map(item => `
    <div class="tracker-item ${item.completed ? 'completed' : ''}">
      <div class="tracker-item-title-row">
        <h4>${item.title}</h4>
        <span class="pattern-badge">${item.category}</span>
      </div>
      <div class="tracker-meta-line">${item.target ? `Target: ${item.target}` : 'No target date set'}</div>
      ${item.notes ? `<div class="tracker-notes-line">${item.notes}</div>` : ''}
      <div class="tracker-actions">
        <button class="${item.completed ? 'reopen-btn' : 'done-btn'}" onclick="toggleTrackerItem(${item.id}, ${!item.completed})">${item.completed ? 'Mark Open' : 'Mark Complete'}</button>
        <button class="delete-btn" onclick="deleteTrackerItem(${item.id})">Delete</button>
      </div>
    </div>
  `).join("");
}


/* ==========================================
   5. LLD & QUIZ ENGINE CONTROLLER
   ========================================== */
let lldSyllabusChapters = {};
let lldQuizzesData = {};
let selectedAnswers = {};

async function loadLldTheory() {
  try {
    const res = await fetch(`${API_URL}/api/lld/chapters`);
    if (!res.ok) return;
    lldSyllabusChapters = await res.json();
    showLldTheory('solid');
  } catch (e) {}
}

function showLldTheory(topic) {
  const chapter = lldSyllabusChapters[topic];
  const display = document.querySelector('#lld-theory-display');
  if (!chapter) return;
  
  let codeSnippetHtml = "";
  if (chapter.code_example) {
    codeSnippetHtml = `
      <div style="margin-top: 15px;">
        <h5 style="margin: 0 0 5px 0;">Violating Code:</h5>
        <pre><code>${chapter.code_example.bad}</code></pre>
        <h5 style="margin: 15px 0 5px 0;">SOLID Conforming Code:</h5>
        <pre><code>${chapter.code_example.good}</code></pre>
      </div>
    `;
  }
  
  display.innerHTML = `
    <h3>${chapter.title}</h3>
    <div>${simpleMarkdownToHtml(chapter.content)}</div>
    ${codeSnippetHtml}
  `;
}

async function loadLldQuizzes() {
  try {
    const res = await fetch(`${API_URL}/api/lld/quizzes`);
    if (!res.ok) return;
    lldQuizzesData = await res.json();
  } catch (e) {}
}

function startQuiz(quizKey) {
  currentQuizId = quizKey;
  selectedAnswers = {};
  
  const quiz = lldQuizzesData[quizKey];
  if (!quiz) return;
  
  document.querySelector('#quiz-runner-box').style.display = "block";
  document.querySelector('#quiz-run-title').textContent = quiz.title;
  document.querySelector('#quiz-results-summary').style.display = "none";
  
  const container = document.querySelector('#quiz-questions-container');
  container.innerHTML = "";
  
  quiz.questions.forEach((q, qidx) => {
    const qcard = document.createElement('div');
    qcard.className = "question-card";
    qcard.innerHTML = `
      <div class="question-text">${qidx + 1}. ${q.question}</div>
      <div class="options-list" id="opt-list-${q.id}"></div>
    `;
    container.appendChild(qcard);
    
    const optionsContainer = qcard.querySelector(`#opt-list-${q.id}`);
    q.options.forEach((opt, oidx) => {
      const obtn = document.createElement('button');
      obtn.className = "option-btn";
      obtn.id = `opt-${q.id}-${oidx}`;
      obtn.textContent = opt;
      obtn.onclick = () => selectOption(q.id, oidx);
      optionsContainer.appendChild(obtn);
    });
  });
}

function selectOption(qId, oIdx) {
  // Clear previous selections for this question
  const quiz = lldQuizzesData[currentQuizId];
  const q = quiz.questions.find(x => x.id === qId);
  q.options.forEach((_, idx) => {
    document.querySelector(`#opt-${qId}-${idx}`).classList.remove('selected');
  });
  
  // Mark selected
  document.querySelector(`#opt-${qId}-${oIdx}`).classList.add('selected');
  selectedAnswers[qId] = oIdx;
}

async function submitQuizAnswers() {
  if (!currentQuizId) return;
  const quiz = lldQuizzesData[currentQuizId];
  
  // Validate all questions answered
  const answeredCount = Object.keys(selectedAnswers).length;
  if (answeredCount < quiz.questions.length) {
    showToast("Please answer all questions before submitting.");
    return;
  }
  
  const payload = {
    quiz_id: currentQuizId,
    answers: Object.keys(selectedAnswers).map(qid => ({
      question_id: qid,
      selected_option: selectedAnswers[qid]
    }))
  };
  
  try {
    const res = await authenticatedFetch(`${API_URL}/api/lld/quizzes/${currentQuizId}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) throw new Error("Quiz submission failed");
    
    const result = await res.json();
    
    // Display result colors & explanations
    result.results.forEach(r => {
      // Correct answer index
      const correctIdx = r.correct_option;
      const selectedIdx = r.selected_option;
      
      // Paint options
      const quizQ = quiz.questions.find(x => x.id === r.question_id);
      quizQ.options.forEach((_, oidx) => {
        const btn = document.querySelector(`#opt-${r.question_id}-${oidx}`);
        btn.disabled = true;
        if (oidx === correctIdx) {
          btn.className = "option-btn correct";
        } else if (oidx === selectedIdx && !r.passed) {
          btn.className = "option-btn incorrect";
        }
      });
      
      // Inject explanation block
      const optList = document.querySelector(`#opt-list-${r.question_id}`);
      const explDiv = document.createElement('div');
      explDiv.className = "explanation-box";
      explDiv.innerHTML = `<strong>${r.passed ? "Correct!" : "Incorrect."}</strong> ${r.explanation}`;
      optList.appendChild(explDiv);
    });
    
    // Show summary card
    const summary = document.querySelector('#quiz-results-summary');
    summary.style.display = "block";
    summary.innerHTML = `
      <h4>Assessment Finished</h4>
      <div class="score-display">${Math.round(result.score)}%</div>
      <p>${result.passed ? "Passed ✓ Target readiness unlocked." : "Failed. 70% required to pass. Retry to boost score."}</p>
    `;
    
    if (result.passed) {
      currentUser.readiness_score = Math.min(100.0, currentUser.readiness_score + 4.0);
      updateDashboardMetrics();
      updateQuizProgressStats();
    }
    
  } catch (err) {
    showToast(err.message);
  }
}

function updateQuizProgressStats() {
  document.querySelector('#card-lld-status').textContent = "Quizzes Completed";
}


/* ==========================================
   4. AI LEARNING CONTROLLER
   ========================================== */
let aiChapters = {};
let aiQuizData = {};
let selectedAiAnswers = {};

async function loadAiChapters() {
  try {
    const [chaptersRes, refsRes] = await Promise.all([
      fetch(`${API_URL}/api/ai/chapters`),
      fetch(`${API_URL}/api/ai/references`)
    ]);
    if (!chaptersRes.ok) return;
    aiChapters = await chaptersRes.json();
    aiReferences = refsRes.ok ? ((await refsRes.json()).items || []) : [];
    
    const menu = document.querySelector('#ai-chapters-menu');
    menu.innerHTML = "";
    
    Object.keys(aiChapters).forEach(key => {
      const ch = aiChapters[key];
      const card = document.createElement('button');
      card.className = "ai-chapter-card";
      card.id = `ai-card-${key}`;
      card.onclick = () => readAiChapter(key);
      card.innerHTML = `
        <h4>${ch.title}</h4>
      `;
      menu.appendChild(card);
    });
    renderAiReferenceList();
    
    if (Object.keys(aiChapters).length > 0) {
      readAiChapter(Object.keys(aiChapters)[0]);
    }
  } catch (e) {}
}

function renderAiReferenceList() {
  const host = document.querySelector('#ai-reference-list');
  if (!host) return;
  if (!aiReferences.length) {
    host.innerHTML = `<p class="ai-reference-empty">No references loaded.</p>`;
    return;
  }
  host.innerHTML = aiReferences.map(ref => `
    <a class="ai-reference-link ${ref.available ? '' : 'disabled'}"
       href="${ref.available ? ref.pdf_url : '#'}"
       ${ref.available ? 'target="_blank" rel="noopener noreferrer"' : ''}
       title="${ref.filename}">
      <span>${ref.week}</span>
      <strong>${ref.title}</strong>
    </a>
  `).join('');
}

function readAiChapter(key) {
  currentAiChapterId = key;
  const chapter = aiChapters[key];
  if (!chapter) return;
  
  document.querySelectorAll('.ai-chapter-card').forEach(c => c.classList.remove('active'));
  document.querySelector(`#ai-card-${key}`).classList.add('active');
  
  document.querySelector('#no-ai-selected').style.display = "none";
  document.querySelector('#ai-content-box').style.display = "block";
  document.querySelector('#ai-quiz-runner').style.display = "none";
  
  document.querySelector('#ai-chapter-title').textContent = chapter.title;
  const chapterRefs = (chapter.reference_ids || [])
    .map(refId => aiReferences.find(r => r.id === refId))
    .filter(Boolean);
  const referenceHtml = chapterRefs.length ? `
    <div class="ai-inline-references">
      <h4>Chapter References</h4>
      ${chapterRefs.map(ref => `
        <a href="${ref.pdf_url}" target="_blank" rel="noopener noreferrer">${ref.week} - ${ref.title}</a>
      `).join('')}
    </div>
  ` : "";
  document.querySelector('#ai-chapter-body').innerHTML = `${simpleMarkdownToHtml(chapter.content)}${referenceHtml}`;
}

async function startAiQuiz() {
  try {
    const res = await fetch(`${API_URL}/api/ai/quizzes`);
    if (!res.ok) return;
    const data = await res.json();
    aiQuizData = data.ai_general_quiz;
    
    selectedAiAnswers = {};
    
    document.querySelector('#ai-content-box').style.display = "none";
    document.querySelector('#ai-quiz-runner').style.display = "block";
    document.querySelector('#ai-quiz-results').style.display = "none";
    
    const container = document.querySelector('#ai-quiz-questions');
    container.innerHTML = "";
    
    aiQuizData.questions.forEach((q, idx) => {
      const qcard = document.createElement('div');
      qcard.className = "question-card";
      qcard.innerHTML = `
        <div class="question-text">${idx+1}. ${q.question}</div>
        <div class="options-list" id="ai-opt-list-${q.id}"></div>
      `;
      container.appendChild(qcard);
      
      const optContainer = qcard.querySelector(`#ai-opt-list-${q.id}`);
      q.options.forEach((opt, oidx) => {
        const btn = document.createElement('button');
        btn.className = "option-btn";
        btn.id = `ai-opt-${q.id}-${oidx}`;
        btn.textContent = opt;
        btn.onclick = () => {
          q.options.forEach((_, i) => document.querySelector(`#ai-opt-${q.id}-${i}`).classList.remove('selected'));
          btn.classList.add('selected');
          selectedAiAnswers[q.id] = oidx;
        };
        optContainer.appendChild(btn);
      });
    });
  } catch (e) {
    showToast("Error starting AI Quiz");
  }
}

function closeAiQuiz() {
  document.querySelector('#ai-quiz-runner').style.display = "none";
  document.querySelector('#ai-content-box').style.display = "block";
}

async function submitAiQuizAnswers() {
  const total = aiQuizData.questions.length;
  if (Object.keys(selectedAiAnswers).length < total) {
    showToast("Answer all questions first.");
    return;
  }
  
  const payload = {
    quiz_id: "ai_general_quiz",
    answers: Object.keys(selectedAiAnswers).map(qid => ({
      question_id: qid,
      selected_option: selectedAiAnswers[qid]
    }))
  };
  
  try {
    const res = await authenticatedFetch(`${API_URL}/api/ai/quizzes/ai_general_quiz/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) throw new Error("Submit failed");
    
    const result = await res.json();
    
    result.results.forEach(r => {
      const correctIdx = r.correct_option;
      const selectedIdx = r.selected_option;
      
      const q = aiQuizData.questions.find(x => x.id === r.question_id);
      q.options.forEach((_, i) => {
        const btn = document.querySelector(`#ai-opt-${r.question_id}-${i}`);
        btn.disabled = true;
        if (i === correctIdx) btn.className = "option-btn correct";
        else if (i === selectedIdx && !r.passed) btn.className = "option-btn incorrect";
      });
      
      const box = document.querySelector(`#ai-opt-list-${r.question_id}`);
      const expl = document.createElement('div');
      expl.className = "explanation-box";
      expl.innerHTML = `<strong>${r.passed ? 'Passed!' : 'Incorrect'}</strong> ${r.explanation}`;
      box.appendChild(expl);
    });
    
    const summary = document.querySelector('#ai-quiz-results');
    summary.style.display = "block";
    summary.innerHTML = `
      <h4>AI Benchmark Results</h4>
      <div class="score-display">${Math.round(result.score)}%</div>
      <p>${result.passed ? "Sufficient alignment achieved!" : "Score low. Underfitting detected, retry."}</p>
    `;
    
    if (result.passed) {
      currentUser.readiness_score = Math.min(100.0, currentUser.readiness_score + 4.0);
      updateDashboardMetrics();
    }
  } catch (err) {
    showToast(err.message);
  }
}


/* ==========================================
   5. BACKEND PLAYGROUND LAB CONTROLLER
   ========================================== */
async function loadBackendLabSyllabus() {
  try {
    const res = await fetch(`${API_URL}/api/lab/learning/domains`);
    if (!res.ok) return;
    const data = await res.json();
    backendLabDomains = data.domains || [];
    renderBackendDomainList();
    updateBackendProgressStrip();
  } catch (e) {
    console.error("Backend syllabus load failed:", e);
  }
}

async function loadBackendLabProgress() {
  try {
    const res = await authenticatedFetch(`${API_URL}/api/lab/learning/progress`);
    if (!res.ok) return;
    const data = await res.json();
    backendCompletedTopics = new Set(data.completed_topic_ids || []);
    renderBackendDomainList();
    updateBackendProgressStrip();
  } catch (e) {
    console.error("Backend progress load failed:", e);
  }
}

function renderBackendDomainList() {
  const host = document.querySelector('#backend-domain-list');
  if (!host) return;

  if (!backendLabDomains.length) {
    host.innerHTML = `<p class="placeholder-text">Loading backend syllabus...</p>`;
    return;
  }

  host.innerHTML = backendLabDomains.map(domain => `
    <div class="backend-domain-card">
      <h5 class="backend-domain-title">${domain.title} (${domain.topic_count})</h5>
      <div class="backend-topic-list">
        ${(domain.topics || []).map(topic => `
          <button class="backend-topic-item ${currentBackendTopicId === topic.id ? 'active' : ''} ${backendCompletedTopics.has(topic.id) ? 'done' : ''}" onclick="openBackendTopic('${topic.id}')">
            ${topic.number}. ${topic.title}
          </button>
        `).join('')}
      </div>
    </div>
  `).join('');
}

async function openBackendTopic(topicId) {
  try {
    const res = await fetch(`${API_URL}/api/lab/learning/topics/${topicId}`);
    if (!res.ok) throw new Error("Unable to open topic");
    currentBackendTopicDetail = await res.json();
    currentBackendTopicId = topicId;

    document.querySelector('#backend-topic-empty').style.display = "none";
    document.querySelector('#backend-topic-workspace').style.display = "block";
    document.querySelector('#backend-topic-title').textContent = currentBackendTopicDetail.title;

    const detailedMarkdown = currentBackendTopicDetail.detailed_markdown;
    if (detailedMarkdown) {
      document.querySelector('#backend-topic-learn-content').innerHTML = simpleMarkdownToHtml(detailedMarkdown);
    } else {
      const learnHtml = `
        <h4>${currentBackendTopicDetail.domain_title}</h4>
        <p><strong>Concept Focus:</strong> ${currentBackendTopicDetail.concept}</p>
        <p><strong>Hands-on Task:</strong> ${currentBackendTopicDetail.hands_on}</p>
        <p><strong>Challenge Mode:</strong> ${currentBackendTopicDetail.challenge}</p>
        <h4>Quick Checks</h4>
        <ul>${(currentBackendTopicDetail.quick_check || []).map(q => `<li>${q}</li>`).join('')}</ul>
      `;
      document.querySelector('#backend-topic-learn-content').innerHTML = learnHtml;
    }
    document.querySelector('#backend-code-editor').value = currentBackendTopicDetail.default_code || "";

    switchBackendOutputTab('terminal');
    document.querySelector('#backend-output-terminal-pre').textContent = "Ready. Click 'Run Simulation ⚡' to execute this topic playground.";
    document.querySelector('#backend-state-table-wrap').innerHTML = "";
    document.querySelector('#backend-metrics-wrap').innerHTML = "";

    const done = backendCompletedTopics.has(topicId);
    const completeBtn = document.querySelector('#backend-mark-complete-btn');
    completeBtn.disabled = false;
    completeBtn.textContent = done ? "Topic Completed ✓" : "Mark Topic Completed ✓";
    completeBtn.className = done ? "complete-chapter-btn done" : "complete-chapter-btn";

    renderBackendDomainList();
    updateBackendProgressStrip();
  } catch (e) {
    showToast(e.message);
  }
}

function switchBackendOutputTab(tabKey) {
  const tabs = ['terminal', 'state', 'metrics'];
  tabs.forEach(key => {
    const btn = document.querySelector(`#backend-tab-${key}`);
    const card = document.querySelector(`#backend-output-${key}`);
    if (btn) btn.classList.toggle('active', key === tabKey);
    if (card) card.style.display = key === tabKey ? "block" : "none";
  });
}

function updateBackendProgressStrip() {
  const positionEl = document.querySelector('#backend-topic-position');
  const domainEl = document.querySelector('#backend-topic-domain');
  const completeEl = document.querySelector('#backend-complete-count');
  if (!positionEl || !domainEl || !completeEl) return;

  const total = backendLabDomains.reduce((acc, d) => acc + (d.topic_count || 0), 0);
  const completed = backendCompletedTopics.size;
  let position = 0;
  if (currentBackendTopicDetail?.number) {
    position = currentBackendTopicDetail.number;
  }

  positionEl.textContent = `Topic ${position || 0} of ${total || 100}`;
  domainEl.textContent = currentBackendTopicDetail ? currentBackendTopicDetail.domain_title : "Select a topic from the syllabus";
  completeEl.textContent = `${completed} Completed`;
}

async function executeBackendTopic() {
  if (!currentBackendTopicId) {
    showToast("Select a topic first.");
    return;
  }

  const ttl = Number(document.querySelector('#backend-param-ttl')?.value || 60);
  const concurrency = Number(document.querySelector('#backend-param-concurrency')?.value || 25);
  const requestCount = Number(document.querySelector('#backend-param-requests')?.value || 200);
  const code = document.querySelector('#backend-code-editor')?.value || "";

  document.querySelector('#backend-output-terminal-pre').textContent = "Executing topic simulation...";
  switchBackendOutputTab('terminal');

  try {
    const res = await authenticatedFetch(`${API_URL}/api/lab/learning/topics/${currentBackendTopicId}/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code,
        params: {
          ttl_seconds: ttl,
          concurrency: concurrency,
          request_count: requestCount
        }
      })
    });
    if (!res.ok) throw new Error("Execution failed");
    const data = await res.json();

    document.querySelector('#backend-output-terminal-pre').textContent = (data.logs || []).join('\n');
    renderBackendStateTable(data.state || []);
    renderBackendMetrics(data.metrics || {}, data.execution_ms);
  } catch (e) {
    document.querySelector('#backend-output-terminal-pre').textContent = `Execution Error: ${e.message}`;
  }
}

function renderBackendStateTable(rows) {
  const wrap = document.querySelector('#backend-state-table-wrap');
  if (!wrap) return;
  if (!rows.length) {
    wrap.innerHTML = `<p class="placeholder-text">No runtime state emitted for this run.</p>`;
    return;
  }
  const keys = Object.keys(rows[0]);
  const header = keys.map(k => `<th>${k}</th>`).join('');
  const body = rows.map(r => `<tr>${keys.map(k => `<td>${String(r[k])}</td>`).join('')}</tr>`).join('');
  wrap.innerHTML = `<table class="backend-state-table"><thead><tr>${header}</tr></thead><tbody>${body}</tbody></table>`;
}

function renderBackendMetrics(metrics, executionMs) {
  const wrap = document.querySelector('#backend-metrics-wrap');
  if (!wrap) return;
  const rows = Object.keys(metrics).map(key => `
    <div class="backend-metric-row"><span>${key}</span><b>${metrics[key]}</b></div>
  `).join('');
  const total = `<div class="backend-metric-row"><span>execution_ms</span><b>${executionMs}</b></div>`;
  wrap.innerHTML = `${rows}${total}`;
}

async function markBackendTopicComplete() {
  if (!currentBackendTopicId) {
    showToast("Select a topic first.");
    return;
  }

  try {
    const res = await authenticatedFetch(`${API_URL}/api/lab/learning/topics/${currentBackendTopicId}/complete`, {
      method: "POST"
    });
    if (!res.ok) throw new Error("Unable to mark topic complete");
    const data = await res.json();
    backendCompletedTopics.add(currentBackendTopicId);
    const completeBtn = document.querySelector('#backend-mark-complete-btn');
    completeBtn.textContent = "Topic Completed ✓";
    completeBtn.className = "complete-chapter-btn done";
    if (currentUser && data.readiness_score !== undefined) {
      currentUser.readiness_score = data.readiness_score;
      updateDashboardMetrics();
    }
    renderBackendDomainList();
    updateBackendProgressStrip();
    showToast("Backend topic marked as completed.");
  } catch (e) {
    showToast(e.message);
  }
}

async function updateDbLabStatus() {
  try {
    const res = await authenticatedFetch(`${API_URL}/api/lab/status`);
    if (!res.ok) return;
    const data = await res.json();
    
    // Update pills
    updateDbCard("postgres", data.postgres);
    updateDbCard("redis", data.redis);
    updateDbCard("elastic", data.elasticsearch);
  } catch (e) {
    console.error("DB Status check failed:", e);
  }
}

function updateDbCard(dbKey, statusData) {
  const pill = document.querySelector(`#status-${dbKey}`);
  const desc = document.querySelector(`#desc-${dbKey}`);
  
  if (statusData.active) {
    pill.textContent = statusData.details;
    pill.className = "status-pill online";
  } else {
    pill.textContent = statusData.details;
    pill.className = "status-pill offline";
  }
  desc.textContent = statusData.explanation;
}

async function runLabTest(dbKey) {
  const consoleOut = document.querySelector('#lab-console-output');
  const codeDisplay = document.querySelector('#lab-code-display');
  
  consoleOut.textContent = `Pinging '/api/lab/${dbKey}/test' endpoint. Waiting for response...`;
  codeDisplay.textContent = `# Initializing code reference view...`;
  
  try {
    const res = await authenticatedFetch(`${API_URL}/api/lab/${dbKey === 'elastic' ? 'elasticsearch' : dbKey}/test`);
    if (!res.ok) throw new Error("Test execution failed");
    
    const data = await res.json();
    
    consoleOut.innerHTML = `
<span style="color: var(--green); font-weight: bold;">[API SUCCESS]</span> Status OK
Execution Latency: ${data.latency_ms || data.results?.timings_ms?.get_operation || "N/A"} ms
Mocked Fallback: ${data.is_mocked !== undefined ? data.is_mocked : "False"}

Response Data:
${JSON.stringify(data.results || data, null, 2)}
    `;
    
    // Render the FastAPI Python integration code template
    codeDisplay.textContent = data.code_snippet;
    
  } catch (e) {
    consoleOut.textContent = `Lab Test Failure: ${e.message}`;
  }
}


/* ==========================================
   6. LEETCODE 100 CONTROLLER
   ========================================== */
const LEETCODE_FALLBACK_QUESTIONS = [
  {
    "id": "1",
    "name": "Two Sum",
    "pattern": "Hash Table",
    "difficulty": "Easy",
    "companies": "Meta, Google, Amazon, Uber, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/two-sum/",
    "solved": true
  },
  {
    "id": "2",
    "name": "Best Time to Buy and Sell Stock",
    "pattern": "Array / DP",
    "difficulty": "Easy",
    "companies": "Meta, Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
    "solved": true
  },
  {
    "id": "3",
    "name": "Contains Duplicate",
    "pattern": "Hash Set",
    "difficulty": "Easy",
    "companies": "Meta, Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/contains-duplicate/",
    "solved": true
  },
  {
    "id": "4",
    "name": "Valid Anagram",
    "pattern": "Hash Table / Sorting",
    "difficulty": "Easy",
    "companies": "Meta, Google, Uber",
    "leetcode_url": "https://leetcode.com/problems/valid-anagram/",
    "solved": true
  },
  {
    "id": "5",
    "name": "Valid Parentheses",
    "pattern": "Stack",
    "difficulty": "Easy",
    "companies": "Meta, Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/valid-parentheses/",
    "solved": true
  },
  {
    "id": "6",
    "name": "Merge Two Sorted Lists",
    "pattern": "Two Pointers / Linked List",
    "difficulty": "Easy",
    "companies": "Meta, Google, Amazon, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/merge-two-sorted-lists/",
    "solved": true
  },
  {
    "id": "7",
    "name": "Invert Binary Tree",
    "pattern": "Tree Traversal (DFS/BFS)",
    "difficulty": "Easy",
    "companies": "Meta, Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/invert-binary-tree/",
    "solved": true
  },
  {
    "id": "8",
    "name": "Maximum Depth of Binary Tree",
    "pattern": "Tree Traversal (DFS)",
    "difficulty": "Easy",
    "companies": "Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/maximum-depth-of-binary-tree/",
    "solved": true
  },
  {
    "id": "9",
    "name": "Reverse Linked List",
    "pattern": "Linked List Manipulation",
    "difficulty": "Easy",
    "companies": "Meta, Amazon, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/reverse-linked-list/",
    "solved": true
  },
  {
    "id": "10",
    "name": "Climbing Stairs",
    "pattern": "Dynamic Programming",
    "difficulty": "Easy",
    "companies": "Google, Amazon, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/climbing-stairs/",
    "solved": true
  },
  {
    "id": "11",
    "name": "Longest Substring Without Repeating Characters",
    "pattern": "Sliding Window",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
    "solved": true
  },
  {
    "id": "12",
    "name": "Longest Repeating Character Replacement",
    "pattern": "Sliding Window",
    "difficulty": "Medium",
    "companies": "Meta, Google, Uber",
    "leetcode_url": "https://leetcode.com/problems/longest-repeating-character-replacement/",
    "solved": true
  },
  {
    "id": "13",
    "name": "Minimum Window Substring",
    "pattern": "Sliding Window / Two Pointers",
    "difficulty": "Hard",
    "companies": "Meta, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/minimum-window-substring/",
    "solved": true
  },
  {
    "id": "14",
    "name": "Product of Array Except Self",
    "pattern": "Array / Prefix Sum",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/product-of-array-except-self/",
    "solved": true
  },
  {
    "id": "15",
    "name": "Maximum Subarray",
    "pattern": "Dynamic Programming (Kadane's)",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/maximum-subarray/",
    "solved": true
  },
  {
    "id": "16",
    "name": "3Sum",
    "pattern": "Two Pointers",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/3sum/",
    "solved": true
  },
  {
    "id": "17",
    "name": "Merge Intervals",
    "pattern": "Intervals / Sorting",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/merge-intervals/",
    "solved": true
  },
  {
    "id": "18",
    "name": "Group Anagrams",
    "pattern": "Hash Table / String",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/group-anagrams/",
    "solved": true
  },
  {
    "id": "19",
    "name": "Number of Islands",
    "pattern": "Graph Traversal (DFS/BFS)",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon, Uber, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/number-of-islands/",
    "solved": true
  },
  {
    "id": "20",
    "name": "Clone Graph",
    "pattern": "Graph Traversal (DFS/BFS)",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/clone-graph/",
    "solved": true
  },
  {
    "id": "21",
    "name": "Container With Most Water",
    "pattern": "Two Pointers",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/container-with-most-water/",
    "solved": true
  },
  {
    "id": "22",
    "name": "Search in Rotated Sorted Array",
    "pattern": "Binary Search",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/search-in-rotated-sorted-array/",
    "solved": true
  },
  {
    "id": "23",
    "name": "Combination Sum",
    "pattern": "Backtracking",
    "difficulty": "Medium",
    "companies": "Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/combination-sum/",
    "solved": true
  },
  {
    "id": "24",
    "name": "Palindromic Substrings",
    "pattern": "Dynamic Programming / Expand Around Center",
    "difficulty": "Medium",
    "companies": "Meta, Amazon",
    "leetcode_url": "https://leetcode.com/problems/palindromic-substrings/",
    "solved": true
  },
  {
    "id": "25",
    "name": "Validate Binary Search Tree",
    "pattern": "Tree Traversal (DFS)",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/validate-binary-search-tree/",
    "solved": true
  },
  {
    "id": "26",
    "name": "Binary Tree Level Order Traversal",
    "pattern": "Tree Traversal (BFS)",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/binary-tree-level-order-traversal/",
    "solved": true
  },
  {
    "id": "27",
    "name": "Lowest Common Ancestor of a Binary Tree",
    "pattern": "Tree Traversal (DFS)",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/",
    "solved": false
  },
  {
    "id": "28",
    "name": "Construct Binary Tree from Preorder and Inorder Traversal",
    "pattern": "Tree Traversal / Recursion",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/",
    "solved": false
  },
  {
    "id": "29",
    "name": "Implement Trie (Prefix Tree)",
    "pattern": "Trie / Design",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/implement-trie-prefix-tree/",
    "solved": false
  },
  {
    "id": "30",
    "name": "Course Schedule",
    "pattern": "Graph / Topological Sort",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/course-schedule/",
    "solved": false
  },
  {
    "id": "31",
    "name": "Coin Change",
    "pattern": "Dynamic Programming",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Google, Uber",
    "leetcode_url": "https://leetcode.com/problems/coin-change/",
    "solved": false
  },
  {
    "id": "32",
    "name": "Word Break",
    "pattern": "Dynamic Programming",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/word-break/",
    "solved": false
  },
  {
    "id": "33",
    "name": "Longest Increasing Subsequence",
    "pattern": "Dynamic Programming",
    "difficulty": "Medium",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/longest-increasing-subsequence/",
    "solved": false
  },
  {
    "id": "34",
    "name": "House Robber",
    "pattern": "Dynamic Programming",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/house-robber/",
    "solved": false
  },
  {
    "id": "35",
    "name": "Unique Paths",
    "pattern": "Dynamic Programming",
    "difficulty": "Medium",
    "companies": "Meta, Google, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/unique-paths/",
    "solved": false
  },
  {
    "id": "36",
    "name": "Top K Frequent Elements",
    "pattern": "Heap / Quickselect",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/top-k-frequent-elements/",
    "solved": false
  },
  {
    "id": "37",
    "name": "Kth Smallest Element in a BST",
    "pattern": "Tree Traversal (In-order)",
    "difficulty": "Medium",
    "companies": "Meta, Uber",
    "leetcode_url": "https://leetcode.com/problems/kth-smallest-element-in-a-bst/",
    "solved": false
  },
  {
    "id": "38",
    "name": "Remove Nth Node From End of List",
    "pattern": "Two Pointers / Linked List",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/remove-nth-node-from-end-of-list/",
    "solved": false
  },
  {
    "id": "39",
    "name": "Longest Consecutive Sequence",
    "pattern": "Hash Set / Array",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/longest-consecutive-sequence/",
    "solved": false
  },
  {
    "id": "40",
    "name": "Reorder List",
    "pattern": "Linked List Manipulation",
    "difficulty": "Medium",
    "companies": "Meta, Amazon",
    "leetcode_url": "https://leetcode.com/problems/reorder-list/",
    "solved": false
  },
  {
    "id": "41",
    "name": "LRU Cache",
    "pattern": "Design / Hash Map + DLL",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon, Uber, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/lru-cache/",
    "solved": false
  },
  {
    "id": "42",
    "name": "Word Search",
    "pattern": "Backtracking / Matrix Traversal",
    "difficulty": "Medium",
    "companies": "Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/word-search/",
    "solved": false
  },
  {
    "id": "43",
    "name": "Rotate Image",
    "pattern": "Matrix Manipulation",
    "difficulty": "Medium",
    "companies": "Amazon, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/rotate-image/",
    "solved": false
  },
  {
    "id": "44",
    "name": "Spiral Matrix",
    "pattern": "Matrix Traversal",
    "difficulty": "Medium",
    "companies": "Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/spiral-matrix/",
    "solved": false
  },
  {
    "id": "45",
    "name": "Set Matrix Zeroes",
    "pattern": "Matrix / Array",
    "difficulty": "Medium",
    "companies": "Meta, Amazon",
    "leetcode_url": "https://leetcode.com/problems/set-matrix-zeroes/",
    "solved": false
  },
  {
    "id": "46",
    "name": "Subarray Sum Equals K",
    "pattern": "Hash Map / Prefix Sum",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/subarray-sum-equals-k/",
    "solved": false
  },
  {
    "id": "47",
    "name": "Decode Ways",
    "pattern": "Dynamic Programming",
    "difficulty": "Medium",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/decode-ways/",
    "solved": false
  },
  {
    "id": "48",
    "name": "Find Minimum in Rotated Sorted Array",
    "pattern": "Binary Search",
    "difficulty": "Medium",
    "companies": "Meta, Google, Uber",
    "leetcode_url": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/",
    "solved": false
  },
  {
    "id": "49",
    "name": "Add Two Numbers",
    "pattern": "Linked List / Math",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/add-two-numbers/",
    "solved": false
  },
  {
    "id": "50",
    "name": "Copy List with Random Pointer",
    "pattern": "Hash Map / Linked List",
    "difficulty": "Medium",
    "companies": "Meta, Amazon",
    "leetcode_url": "https://leetcode.com/problems/copy-list-with-random-pointer/",
    "solved": false
  },
  {
    "id": "51",
    "name": "Pacific Atlantic Water Flow",
    "pattern": "Graph Traversal (DFS/BFS)",
    "difficulty": "Medium",
    "companies": "Meta, Amazon",
    "leetcode_url": "https://leetcode.com/problems/pacific-atlantic-water-flow/",
    "solved": false
  },
  {
    "id": "52",
    "name": "Non-overlapping Intervals",
    "pattern": "Intervals / Greedy",
    "difficulty": "Medium",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/non-overlapping-intervals/",
    "solved": false
  },
  {
    "id": "53",
    "name": "K Closest Points to Origin",
    "pattern": "Heap / Sorting",
    "difficulty": "Medium",
    "companies": "Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/k-closest-points-to-origin/",
    "solved": false
  },
  {
    "id": "54",
    "name": "Task Scheduler",
    "pattern": "Heap / Greedy",
    "difficulty": "Medium",
    "companies": "Meta, Amazon",
    "leetcode_url": "https://leetcode.com/problems/task-scheduler/",
    "solved": false
  },
  {
    "id": "55",
    "name": "Daily Temperatures",
    "pattern": "Monotonic Stack",
    "difficulty": "Medium",
    "companies": "Google, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/daily-temperatures/",
    "solved": false
  },
  {
    "id": "56",
    "name": "Meeting Rooms II",
    "pattern": "Heap / Intervals",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/meeting-rooms-ii/",
    "solved": false
  },
  {
    "id": "57",
    "name": "Number of Connected Components in an Undirected Graph",
    "pattern": "Graph Traversal / Union-Find",
    "difficulty": "Medium",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/",
    "solved": false
  },
  {
    "id": "58",
    "name": "Graph Valid Tree",
    "pattern": "Graph Traversal / Union-Find",
    "difficulty": "Medium",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/graph-valid-tree/",
    "solved": false
  },
  {
    "id": "59",
    "name": "Alien Dictionary",
    "pattern": "Graph / Topological Sort",
    "difficulty": "Hard",
    "companies": "Meta, Uber",
    "leetcode_url": "https://leetcode.com/problems/alien-dictionary/",
    "solved": false
  },
  {
    "id": "60",
    "name": "Merge k Sorted Lists",
    "pattern": "Heap / Priority Queue",
    "difficulty": "Hard",
    "companies": "Meta, Amazon, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/merge-k-sorted-lists/",
    "solved": false
  },
  {
    "id": "61",
    "name": "Find Median from Data Stream",
    "pattern": "Two Heaps",
    "difficulty": "Hard",
    "companies": "Meta, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/find-median-from-data-stream/",
    "solved": false
  },
  {
    "id": "62",
    "name": "Trapping Rain Water",
    "pattern": "Two Pointers / Stack / DP",
    "difficulty": "Hard",
    "companies": "Google, Amazon, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/trapping-rain-water/",
    "solved": false
  },
  {
    "id": "63",
    "name": "Binary Tree Maximum Path Sum",
    "pattern": "Tree Traversal (DFS)",
    "difficulty": "Hard",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/binary-tree-maximum-path-sum/",
    "solved": false
  },
  {
    "id": "64",
    "name": "Serialize and Deserialize Binary Tree",
    "pattern": "Tree Traversal / Design",
    "difficulty": "Hard",
    "companies": "Meta, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/",
    "solved": false
  },
  {
    "id": "65",
    "name": "Word Search II",
    "pattern": "Trie / Backtracking",
    "difficulty": "Hard",
    "companies": "Meta, Uber",
    "leetcode_url": "https://leetcode.com/problems/word-search-ii/",
    "solved": false
  },
  {
    "id": "66",
    "name": "Regular Expression Matching",
    "pattern": "Dynamic Programming",
    "difficulty": "Hard",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/regular-expression-matching/",
    "solved": false
  },
  {
    "id": "67",
    "name": "Longest Valid Parentheses",
    "pattern": "Stack / Dynamic Programming",
    "difficulty": "Hard",
    "companies": "Meta, Amazon",
    "leetcode_url": "https://leetcode.com/problems/longest-valid-parentheses/",
    "solved": false
  },
  {
    "id": "68",
    "name": "Basic Calculator",
    "pattern": "Stack / Recursion",
    "difficulty": "Hard",
    "companies": "Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/basic-calculator/",
    "solved": false
  },
  {
    "id": "69",
    "name": "Sliding Window Maximum",
    "pattern": "Monotonic Deque",
    "difficulty": "Hard",
    "companies": "Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/sliding-window-maximum/",
    "solved": false
  },
  {
    "id": "70",
    "name": "Bus Routes",
    "pattern": "Graph Traversal (BFS)",
    "difficulty": "Hard",
    "companies": "Uber",
    "leetcode_url": "https://leetcode.com/problems/bus-routes/",
    "solved": false
  },
  {
    "id": "71",
    "name": "Largest Rectangle in Histogram",
    "pattern": "Monotonic Stack",
    "difficulty": "Hard",
    "companies": "Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/largest-rectangle-in-histogram/",
    "solved": false
  },
  {
    "id": "72",
    "name": "Word Ladder",
    "pattern": "Graph Traversal (BFS)",
    "difficulty": "Hard",
    "companies": "Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/word-ladder/",
    "solved": false
  },
  {
    "id": "73",
    "name": "Median of Two Sorted Arrays",
    "pattern": "Binary Search",
    "difficulty": "Hard",
    "companies": "Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/median-of-two-sorted-arrays/",
    "solved": false
  },
  {
    "id": "74",
    "name": "Reverse Nodes in k-Group",
    "pattern": "Linked List / Recursion",
    "difficulty": "Hard",
    "companies": "Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/reverse-nodes-in-k-group/",
    "solved": false
  },
  {
    "id": "75",
    "name": "LFU Cache",
    "pattern": "Design / Hash Map + DLL",
    "difficulty": "Hard",
    "companies": "Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/lfu-cache/",
    "solved": false
  },
  {
    "id": "76",
    "name": "Valid Sudoku",
    "pattern": "Hash Set / Array",
    "difficulty": "Medium",
    "companies": "Google, Uber",
    "leetcode_url": "https://leetcode.com/problems/valid-sudoku/",
    "solved": false
  },
  {
    "id": "77",
    "name": "String to Integer (atoi)",
    "pattern": "String Manipulation",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/string-to-integer-atoi/",
    "solved": false
  },
  {
    "id": "78",
    "name": "Flatten Binary Tree to Linked List",
    "pattern": "Tree Traversal (DFS)",
    "difficulty": "Medium",
    "companies": "Meta, Google, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/flatten-binary-tree-to-linked-list/",
    "solved": false
  },
  {
    "id": "79",
    "name": "Permutations",
    "pattern": "Backtracking",
    "difficulty": "Medium",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/permutations/",
    "solved": false
  },
  {
    "id": "80",
    "name": "Jump Game",
    "pattern": "Greedy / DP",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/jump-game/",
    "solved": false
  },
  {
    "id": "81",
    "name": "Find the Duplicate Number",
    "pattern": "Two Pointers (Floyd's Cycle) / Binary Search",
    "difficulty": "Medium",
    "companies": "Meta, Amazon",
    "leetcode_url": "https://leetcode.com/problems/find-the-duplicate-number/",
    "solved": false
  },
  {
    "id": "82",
    "name": "Kth Largest Element in an Array",
    "pattern": "Heap / Quickselect",
    "difficulty": "Medium",
    "companies": "Amazon, Uber, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/kth-largest-element-in-an-array/",
    "solved": false
  },
  {
    "id": "83",
    "name": "Binary Tree Right Side View",
    "pattern": "Tree Traversal (BFS)",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Nvidia",
    "leetcode_url": "https://leetcode.com/problems/binary-tree-right-side-view/",
    "solved": false
  },
  {
    "id": "84",
    "name": "Add and Search Word - Data structure design",
    "pattern": "Trie / Design",
    "difficulty": "Medium",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/add-and-search-word---data-structure-design/",
    "solved": false
  },
  {
    "id": "85",
    "name": "Insert Interval",
    "pattern": "Intervals / Array",
    "difficulty": "Medium",
    "companies": "Meta, Uber",
    "leetcode_url": "https://leetcode.com/problems/insert-interval/",
    "solved": false
  },
  {
    "id": "86",
    "name": "Longest Palindromic Substring",
    "pattern": "Dynamic Programming / Expand Around Center",
    "difficulty": "Medium",
    "companies": "Meta, Amazon, Uber",
    "leetcode_url": "https://leetcode.com/problems/longest-palindromic-substring/",
    "solved": false
  },
  {
    "id": "87",
    "name": "Accounts Merge",
    "pattern": "Graph Traversal / Union-Find",
    "difficulty": "Medium",
    "companies": "Meta, Amazon",
    "leetcode_url": "https://leetcode.com/problems/accounts-merge/",
    "solved": false
  },
  {
    "id": "88",
    "name": "Next Permutation",
    "pattern": "Array Manipulation",
    "difficulty": "Medium",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/next-permutation/",
    "solved": false
  },
  {
    "id": "89",
    "name": "Evaluate Division",
    "pattern": "Graph Traversal (DFS/BFS)",
    "difficulty": "Medium",
    "companies": "Google, Uber",
    "leetcode_url": "https://leetcode.com/problems/evaluate-division/",
    "solved": false
  },
  {
    "id": "90",
    "name": "Sort Colors",
    "pattern": "Two Pointers",
    "difficulty": "Medium",
    "companies": "Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/sort-colors/",
    "solved": false
  },
  {
    "id": "91",
    "name": "Subsets",
    "pattern": "Backtracking",
    "difficulty": "Medium",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/subsets/",
    "solved": false
  },
  {
    "id": "92",
    "name": "Letter Combinations of a Phone Number",
    "pattern": "Backtracking",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/letter-combinations-of-a-phone-number/",
    "solved": false
  },
  {
    "id": "93",
    "name": "Find First and Last Position of Element in Sorted Array",
    "pattern": "Binary Search",
    "difficulty": "Medium",
    "companies": "Meta, Google, Amazon",
    "leetcode_url": "https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/",
    "solved": false
  },
  {
    "id": "94",
    "name": "Encode and Decode Strings",
    "pattern": "String / Design",
    "difficulty": "Medium",
    "companies": "Meta, Google",
    "leetcode_url": "https://leetcode.com/problems/encode-and-decode-strings/",
    "solved": false
  },
  {
    "id": "95",
    "name": "Rotting Oranges",
    "pattern": "Graph Traversal (BFS)",
    "difficulty": "Medium",
    "companies": "Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/rotting-oranges/",
    "solved": false
  },
  {
    "id": "96",
    "name": "Time Based Key-Value Store",
    "pattern": "Hash Map / Binary Search",
    "difficulty": "Medium",
    "companies": "Google, Uber",
    "leetcode_url": "https://leetcode.com/problems/time-based-key-value-store/",
    "solved": false
  },
  {
    "id": "97",
    "name": "Car Fleet",
    "pattern": "Stack",
    "difficulty": "Medium",
    "companies": "Google",
    "leetcode_url": "https://leetcode.com/problems/car-fleet/",
    "solved": false
  },
  {
    "id": "98",
    "name": "Design Hit Counter",
    "pattern": "Design / Queue",
    "difficulty": "Medium",
    "companies": "Uber",
    "leetcode_url": "https://leetcode.com/problems/design-hit-counter/",
    "solved": false
  },
  {
    "id": "99",
    "name": "Minimum Knight Moves",
    "pattern": "Graph Traversal (BFS)",
    "difficulty": "Medium",
    "companies": "Google",
    "leetcode_url": "https://leetcode.com/problems/minimum-knight-moves/",
    "solved": false
  },
  {
    "id": "100",
    "name": "Reorganize String",
    "pattern": "Heap / Greedy",
    "difficulty": "Medium",
    "companies": "Amazon, Google",
    "leetcode_url": "https://leetcode.com/problems/reorganize-string/",
    "solved": false
  }
];

async function loadLeetcodeQuestions() {
  try {
    const res = await authenticatedFetch(`${API_URL}/api/leetcode/questions`);
    if (res.ok) {
      leetcodeQuestions = await res.json();
    } else {
      leetcodeQuestions = await fetchCsvLeetcodeFallback();
    }
  } catch (err) {
    console.error("Failed to load LeetCode questions from API:", err);
    leetcodeQuestions = await fetchCsvLeetcodeFallback();
  }

  // Populate Pattern Select Dropdown
  const patternSelect = document.querySelector('#leetcode-pattern-select');
  if (patternSelect) {
    const currentVal = patternSelect.value || "all";
    patternSelect.innerHTML = '<option value="all">All Patterns</option>';
    
    const uniquePatterns = [...new Set(leetcodeQuestions.map(q => q.pattern))].sort();
    uniquePatterns.forEach(p => {
      const opt = document.createElement('option');
      opt.value = p;
      opt.textContent = p;
      patternSelect.appendChild(opt);
    });
    
    patternSelect.value = uniquePatterns.includes(currentVal) ? currentVal : "all";
  }
  
  // Calculate and display statistics
  updateLeetcodeStats();
  
  // Initial Render
  filterLeetcodeQuestions();
}

async function fetchCsvLeetcodeFallback() {
  try {
    const res = await fetch(`${API_URL}/leetcode-questions.csv`);
    if (res.ok) {
      const text = await res.text();
      const parsed = parseCsvLeetcodeText(text);
      if (parsed && parsed.length > 0) return parsed;
    }
  } catch (e) {
    console.error("CSV fetch error, using embedded dataset:", e);
  }
  return LEETCODE_FALLBACK_QUESTIONS;
}

function parseCsvLeetcodeText(csvText) {
  const lines = csvText.split('\n').map(l => l.trim()).filter(l => l.length > 0);
  if (lines.length <= 1) return LEETCODE_FALLBACK_QUESTIONS;
  
  const results = [];
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    const cols = line.match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g) || line.split(',');
    const cleanCols = cols.map(c => c.replace(/^"|"$/g, '').trim());
    if (cleanCols.length >= 6) {
      const qid = cleanCols[0];
      const name = cleanCols[1];
      const pattern = cleanCols[2];
      const diff = cleanCols[3];
      const companies = cleanCols[4];
      const solved = cleanCols[5].toLowerCase() === 'solved';
      const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
      
      results.push({
        id: qid,
        name: name,
        pattern: pattern,
        difficulty: diff,
        companies: companies,
        leetcode_url: `https://leetcode.com/problems/${slug}/`,
        solved: solved
      });
    }
  }
  return results.length > 0 ? results : LEETCODE_FALLBACK_QUESTIONS;
}

function updateLeetcodeStats() {
  const total = leetcodeQuestions.length;
  const solvedCount = leetcodeQuestions.filter(q => q.solved).length;
  const statEl = document.querySelector('#leetcode-solved-stat');
  if (statEl) statEl.textContent = solvedCount;
  const barEl = document.querySelector('#leetcode-progress-bar');
  if (barEl) {
    const percentage = total > 0 ? (solvedCount / total) * 100 : 0;
    barEl.style.width = `${percentage}%`;
  }
}

function renderLeetcodeQuestions(listToRender = leetcodeQuestions) {
  const tbody = document.querySelector('#leetcode-table-body');
  if (!tbody) return;
  tbody.innerHTML = "";
  
  if (!listToRender || listToRender.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 30px; color: #666; font-weight: 500;">No matching LeetCode problems found.</td></tr>`;
    return;
  }
  
  listToRender.forEach(q => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${q.id}</td>
      <td>
        <a href="${q.leetcode_url}" target="_blank">
          ${q.name} <i>↗</i>
        </a>
      </td>
      <td><span class="pattern-badge">${q.pattern}</span></td>
      <td><span class="difficulty-badge ${q.difficulty.toLowerCase()}">${q.difficulty}</span></td>
      <td><div class="companies-text" title="${q.companies}">${q.companies}</div></td>
      <td style="text-align: center;">
        <button class="solved-btn ${q.solved ? 'active' : ''}" onclick="toggleLeetcodeSolved('${q.id}', ${!q.solved})">
          ${q.solved ? 'Solved' : 'Unsolved'}
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function filterLeetcodeQuestions() {
  const searchEl = document.querySelector('#leetcode-search-input');
  const diffEl = document.querySelector('#leetcode-difficulty-select');
  const solvedEl = document.querySelector('#leetcode-solved-select');
  const patternEl = document.querySelector('#leetcode-pattern-select');

  const searchVal = searchEl ? searchEl.value.toLowerCase().trim() : "";
  const diffVal = diffEl ? diffEl.value : "all";
  const solvedVal = solvedEl ? solvedEl.value : "all";
  const patternVal = patternEl ? patternEl.value : "all";
  
  const filtered = leetcodeQuestions.filter(q => {
    const matchesSearch = !searchVal || 
      q.name.toLowerCase().includes(searchVal) || 
      q.pattern.toLowerCase().includes(searchVal) || 
      q.companies.toLowerCase().includes(searchVal);
      
    const matchesDiff = diffVal === 'all' || q.difficulty.toLowerCase() === diffVal;
    
    const matchesSolved = solvedVal === 'all' || 
      (solvedVal === 'solved' ? q.solved : !q.solved);
      
    const matchesPattern = patternVal === 'all' || q.pattern === patternVal;
    
    return matchesSearch && matchesDiff && matchesSolved && matchesPattern;
  });
  
  renderLeetcodeQuestions(filtered);
}

async function toggleLeetcodeSolved(questionId, solvedState) {
  const question = leetcodeQuestions.find(q => q.id === questionId);
  if (question) {
    question.solved = solvedState;
  }
  updateLeetcodeStats();
  filterLeetcodeQuestions();

  try {
    const res = await authenticatedFetch(`${API_URL}/api/leetcode/questions/${questionId}/toggle`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ solved: solvedState })
    });
    
    if (res.ok) {
      const data = await res.json();
      if (currentUser && data.readiness_score !== undefined) {
        currentUser.readiness_score = data.readiness_score;
        updateDashboardMetrics();
      }
    }
    showToast(`LeetCode #${questionId} marked as ${solvedState ? 'Solved' : 'Unsolved'}`);
  } catch (err) {
    showToast(`LeetCode #${questionId} marked as ${solvedState ? 'Solved' : 'Unsolved'} (Offline)`);
  }
}

/* ==========================================
   MARKDOWN PARSING (FALLBACK HELPER)
   ========================================== */
function simpleMarkdownToHtml(markdown) {
  if (!markdown) return "";
  let html = markdown;
  
  // Code syntax blocks
  html = html.replace(/```python([\s\S]*?)```/g, '<pre><code class="python-syntax">$1</code></pre>');
  html = html.replace(/```lua([\s\S]*?)```/g, '<pre><code class="lua-syntax">$1</code></pre>');
  html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
  
  // Replace mathematical formulas
  html = html.replace(/\$\$(.*?)\$\$/g, '<code style="display:block; padding:8px; margin:5px 0;">$1</code>');
  html = html.replace(/\$(.*?)\$/g, '<code>$1</code>');
  
  // Inline code ticks
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  
  // Bold & Italics (**bold**, __bold__, ***bold-italic***, *italic*)
  html = html.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');
  html = html.replace(/(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');
  
  // Formats bullet points
  html = html.replace(/^\*\s(.*)$/gm, '<li>$1</li>');
  html = html.replace(/^(<li>.*<\/li>)/s, '<ul>$1</ul>'); // Nest list
  
  // Headings
  html = html.replace(/^####\s(.*)$/gm, '<h4>$1</h4>');
  html = html.replace(/^###\s(.*)$/gm, '<h3>$1</h3>');
  html = html.replace(/^##\s(.*)$/gm, '<h2>$1</h2>');
  html = html.replace(/^#\s(.*)$/gm, '<h1>$1</h1>');
  
  // Linebreaks
  html = html.replace(/\n/g, '<br>');
  
  return html;
}

// Kickstart Auth on DOM Load
document.addEventListener("DOMContentLoaded", () => {
  const isCollapsed = localStorage.getItem("sidebar_collapsed") === "1";
  applySidebarState(isCollapsed, false);
  authenticateUser();
});
