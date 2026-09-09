import sys

with open("script.js", "r", encoding="utf-8") as f:
    content = f.read()

with open("scratch/leetcode_fallback.json", "r", encoding="utf-8") as f:
    fallback_json = f.read()

# 1. Patch authenticateUser catch block
old_catch = """  } catch (err) {
    console.error("Auth error:", err);
    statusPill.textContent = "● Offline Mode";
    statusPill.className = "status-indicator-bar";
    showToast("Server offline. Connect to backend to unlock interactive execution.");
  }"""

new_catch = """  } catch (err) {
    console.error("Auth error:", err);
    statusPill.textContent = "● Offline Mode";
    statusPill.className = "status-indicator-bar";
    showToast("Server offline. Connect to backend to unlock interactive execution.");

    // Initialise UI components with static/fallback data for offline mode
    loadDsaProblems();
    loadDsaSyllabus();
    loadSystemDesignChapters();
    loadSystemDesignExamples();
    loadLldTheory();
    loadLldQuizzes();
    loadAiChapters();
    updateDbLabStatus();
    loadLeetcodeQuestions();
  }"""

if old_catch in content:
    content = content.replace(old_catch, new_catch)
    print("Patched authenticateUser catch block")
else:
    print("WARNING: old_catch not found")

# 2. Patch switchTab
old_switch = """  // Special cases when entering tabs
  if (targetId === "lab-section") {
    updateDbLabStatus();
  }"""

new_switch = """  // Special cases when entering tabs
  if (targetId === "lab-section") {
    updateDbLabStatus();
  } else if (targetId === "leetcode-section") {
    if (!leetcodeQuestions || leetcodeQuestions.length === 0) {
      loadLeetcodeQuestions();
    } else {
      filterLeetcodeQuestions();
    }
  }"""

if old_switch in content:
    content = content.replace(old_switch, new_switch)
    print("Patched switchTab")
else:
    print("WARNING: old_switch not found")

# 3. Patch LEETCODE 100 CONTROLLER section
target_section_start = "/* ==========================================\n   6. LEETCODE 100 CONTROLLER\n   ========================================== */"
target_section_end = "/* ==========================================\n   MARKDOWN PARSING (FALLBACK HELPER)\n   ========================================== */"

start_idx = content.find(target_section_start)
end_idx = content.find(target_section_end)

if start_idx != -1 and end_idx != -1:
    new_controller = f"""/* ==========================================
   6. LEETCODE 100 CONTROLLER
   ========================================== */
const LEETCODE_FALLBACK_QUESTIONS = {fallback_json};

async function loadLeetcodeQuestions() {{
  try {{
    const res = await authenticatedFetch(`${{API_URL}}/api/leetcode/questions`);
    if (res.ok) {{
      leetcodeQuestions = await res.json();
    }} else {{
      leetcodeQuestions = await fetchCsvLeetcodeFallback();
    }}
  }} catch (err) {{
    console.error("Failed to load LeetCode questions from API:", err);
    leetcodeQuestions = await fetchCsvLeetcodeFallback();
  }}

  // Populate Pattern Select Dropdown
  const patternSelect = document.querySelector('#leetcode-pattern-select');
  if (patternSelect) {{
    const currentVal = patternSelect.value || "all";
    patternSelect.innerHTML = '<option value="all">All Patterns</option>';
    
    const uniquePatterns = [...new Set(leetcodeQuestions.map(q => q.pattern))].sort();
    uniquePatterns.forEach(p => {{
      const opt = document.createElement('option');
      opt.value = p;
      opt.textContent = p;
      patternSelect.appendChild(opt);
    }});
    
    patternSelect.value = uniquePatterns.includes(currentVal) ? currentVal : "all";
  }}
  
  // Calculate and display statistics
  updateLeetcodeStats();
  
  // Initial Render
  filterLeetcodeQuestions();
}}

async function fetchCsvLeetcodeFallback() {{
  try {{
    const res = await fetch(`${{API_URL}}/leetcode-questions.csv`);
    if (res.ok) {{
      const text = await res.text();
      const parsed = parseCsvLeetcodeText(text);
      if (parsed && parsed.length > 0) return parsed;
    }}
  }} catch (e) {{
    console.error("CSV fetch error, using embedded dataset:", e);
  }}
  return LEETCODE_FALLBACK_QUESTIONS;
}}

function parseCsvLeetcodeText(csvText) {{
  const lines = csvText.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
  if (lines.length <= 1) return LEETCODE_FALLBACK_QUESTIONS;
  
  const results = [];
  for (let i = 1; i < lines.length; i++) {{
    const line = lines[i];
    const cols = line.match(/(".*?"|[^",\\s]+)(?=\\s*,|\\s*$)/g) || line.split(',');
    const cleanCols = cols.map(c => c.replace(/^"|"$/g, '').trim());
    if (cleanCols.length >= 6) {{
      const qid = cleanCols[0];
      const name = cleanCols[1];
      const pattern = cleanCols[2];
      const diff = cleanCols[3];
      const companies = cleanCols[4];
      const solved = cleanCols[5].toLowerCase() === 'solved';
      const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
      
      results.push({{
        id: qid,
        name: name,
        pattern: pattern,
        difficulty: diff,
        companies: companies,
        leetcode_url: `https://leetcode.com/problems/${{slug}}/`,
        solved: solved
      }});
    }}
  }}
  return results.length > 0 ? results : LEETCODE_FALLBACK_QUESTIONS;
}}

function updateLeetcodeStats() {{
  const total = leetcodeQuestions.length;
  const solvedCount = leetcodeQuestions.filter(q => q.solved).length;
  const statEl = document.querySelector('#leetcode-solved-stat');
  if (statEl) statEl.textContent = solvedCount;
  const barEl = document.querySelector('#leetcode-progress-bar');
  if (barEl) {{
    const percentage = total > 0 ? (solvedCount / total) * 100 : 0;
    barEl.style.width = `${{percentage}}%`;
  }}
}}

function renderLeetcodeQuestions(listToRender = leetcodeQuestions) {{
  const tbody = document.querySelector('#leetcode-table-body');
  if (!tbody) return;
  tbody.innerHTML = "";
  
  if (!listToRender || listToRender.length === 0) {{
    tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 30px; color: #666; font-weight: 500;">No matching LeetCode problems found.</td></tr>`;
    return;
  }}
  
  listToRender.forEach(q => {{
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${{q.id}}</td>
      <td>
        <a href="${{q.leetcode_url}}" target="_blank">
          ${{q.name}} <i>↗</i>
        </a>
      </td>
      <td><span class="pattern-badge">${{q.pattern}}</span></td>
      <td><span class="difficulty-badge ${{q.difficulty.toLowerCase()}}">${{q.difficulty}}</span></td>
      <td><div class="companies-text" title="${{q.companies}}">${{q.companies}}</div></td>
      <td style="text-align: center;">
        <button class="solved-btn ${{q.solved ? 'active' : ''}}" onclick="toggleLeetcodeSolved('${{q.id}}', ${{!q.solved}})">
          ${{q.solved ? 'Solved' : 'Unsolved'}}
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  }});
}}

function filterLeetcodeQuestions() {{
  const searchEl = document.querySelector('#leetcode-search-input');
  const diffEl = document.querySelector('#leetcode-difficulty-select');
  const solvedEl = document.querySelector('#leetcode-solved-select');
  const patternEl = document.querySelector('#leetcode-pattern-select');

  const searchVal = searchEl ? searchEl.value.toLowerCase().trim() : "";
  const diffVal = diffEl ? diffEl.value : "all";
  const solvedVal = solvedEl ? solvedEl.value : "all";
  const patternVal = patternEl ? patternEl.value : "all";
  
  const filtered = leetcodeQuestions.filter(q => {{
    const matchesSearch = !searchVal || 
      q.name.toLowerCase().includes(searchVal) || 
      q.pattern.toLowerCase().includes(searchVal) || 
      q.companies.toLowerCase().includes(searchVal);
      
    const matchesDiff = diffVal === 'all' || q.difficulty.toLowerCase() === diffVal;
    
    const matchesSolved = solvedVal === 'all' || 
      (solvedVal === 'solved' ? q.solved : !q.solved);
      
    const matchesPattern = patternVal === 'all' || q.pattern === patternVal;
    
    return matchesSearch && matchesDiff && matchesSolved && matchesPattern;
  }});
  
  renderLeetcodeQuestions(filtered);
}}

async function toggleLeetcodeSolved(questionId, solvedState) {{
  const question = leetcodeQuestions.find(q => q.id === questionId);
  if (question) {{
    question.solved = solvedState;
  }}
  updateLeetcodeStats();
  filterLeetcodeQuestions();

  try {{
    const res = await authenticatedFetch(`${{API_URL}}/api/leetcode/questions/${{questionId}}/toggle`, {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{ solved: solvedState }})
    }});
    
    if (res.ok) {{
      const data = await res.json();
      if (currentUser && data.readiness_score !== undefined) {{
        currentUser.readiness_score = data.readiness_score;
        updateDashboardMetrics();
      }}
    }}
    showToast(`LeetCode #${{questionId}} marked as ${{solvedState ? 'Solved' : 'Unsolved'}}`);
  }} catch (err) {{
    showToast(`LeetCode #${{questionId}} marked as ${{solvedState ? 'Solved' : 'Unsolved'}} (Offline)`);
  }}
}}

"""
    content = content[:start_idx] + new_controller + content[end_idx:]
    print("Successfully replaced LeetCode controller block")
else:
    print("ERROR: Section start or end not found!")

with open("script.js", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated script.js file successfully.")
