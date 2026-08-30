const STORAGE_KEY = "nearmeos-launchbase-v1";
const SETTINGS_KEY = "nearmeos-launchbase-settings-v1";

const state = {
  data: null,
  progress: {},
  filterStatus: "all",
  query: "",
  activeId: null,
};

const els = {
  board: document.getElementById("board"),
  metrics: document.getElementById("metrics"),
  search: document.getElementById("search"),
  statusFilters: document.getElementById("status-filters"),
  saveHint: document.getElementById("save-hint"),
  settingsDialog: document.getElementById("settings-dialog"),
  projectDialog: document.getElementById("project-dialog"),
  btnSettings: document.getElementById("btn-settings"),
  btnExport: document.getElementById("btn-export"),
  btnImport: document.getElementById("btn-import"),
  importFile: document.getElementById("import-file"),
  btnCopyEnv: document.getElementById("btn-copy-env"),
  bcAccount: document.getElementById("bc-account"),
  bcToken: document.getElementById("bc-token"),
  bcUa: document.getElementById("bc-ua"),
  dlgType: document.getElementById("dlg-type"),
  dlgName: document.getElementById("dlg-name"),
  dlgMeta: document.getElementById("dlg-meta"),
  dlgBar: document.getElementById("dlg-bar"),
  dlgCount: document.getElementById("dlg-count"),
  dlgGroups: document.getElementById("dlg-groups"),
  dlgUrl: document.getElementById("dlg-url"),
  dlgPr: document.getElementById("dlg-pr"),
  dlgClose: document.getElementById("dlg-close"),
  dlgReset: document.getElementById("dlg-reset"),
};

function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

function saveProgress() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.progress));
  els.saveHint.textContent = `Saved ${new Date().toLocaleTimeString()}`;
}

function loadSettings() {
  try {
    return JSON.parse(localStorage.getItem(SETTINGS_KEY) || "{}");
  } catch {
    return {};
  }
}

function saveSettings(settings) {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

function ensureProjectProgress(projectId) {
  if (!state.progress[projectId]) {
    state.progress[projectId] = { done: {}, statusOverride: null };
  }
  return state.progress[projectId];
}

function checklistStats(projectId) {
  const template = state.data.checklistTemplate;
  const doneMap = ensureProjectProgress(projectId).done;
  const total = template.length;
  const done = template.filter((item) => doneMap[item.id]).length;
  return { done, total, pct: total ? Math.round((done / total) * 100) : 0 };
}

function effectiveStatus(project) {
  const override = ensureProjectProgress(project.id).statusOverride;
  if (override) return override;
  const { pct } = checklistStats(project.id);
  if (project.status === "live") return "live";
  if (pct >= 100) return "ready";
  return project.status || "staging";
}

function deriveStatusOverride(projectId) {
  const { pct } = checklistStats(projectId);
  const current = ensureProjectProgress(projectId);
  if (pct >= 100 && current.statusOverride !== "live") {
    current.statusOverride = "ready";
  } else if (pct < 100 && current.statusOverride === "ready") {
    current.statusOverride = null;
  }
}

function renderMetrics(projects) {
  const total = projects.length;
  let ready = 0;
  let live = 0;
  let checks = 0;
  let checksDone = 0;

  for (const project of projects) {
    const status = effectiveStatus(project);
    if (status === "ready") ready += 1;
    if (status === "live") live += 1;
    const stats = checklistStats(project.id);
    checks += stats.total;
    checksDone += stats.done;
  }

  els.metrics.innerHTML = `
    <div class="metric"><strong>${total}</strong><span>Projects</span></div>
    <div class="metric amber"><strong>${ready}</strong><span>Ready to launch</span></div>
    <div class="metric green"><strong>${live}</strong><span>Marked live</span></div>
    <div class="metric sky"><strong>${checksDone}/${checks}</strong><span>Checklist items</span></div>
  `;
}

function projectMatches(project) {
  const status = effectiveStatus(project);
  if (state.filterStatus !== "all" && status !== state.filterStatus) return false;
  if (!state.query) return true;
  const hay = [project.name, project.client, project.type, project.notes, project.url]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
  return hay.includes(state.query);
}

function renderBoard() {
  const projects = state.data.projects.filter(projectMatches);
  renderMetrics(state.data.projects);

  if (!projects.length) {
    els.board.innerHTML = `<p class="hint">No projects match this filter.</p>`;
    return;
  }

  els.board.innerHTML = "";
  for (const project of projects) {
    const stats = checklistStats(project.id);
    const status = effectiveStatus(project);
    const card = document.createElement("button");
    card.type = "button";
    card.className = "project";
    card.dataset.id = project.id;
    card.innerHTML = `
      <div class="project-top">
        <div>
          <h3>${escapeHtml(project.name)}</h3>
          <p class="sub">${escapeHtml(project.client)} · ${escapeHtml(project.type)}</p>
        </div>
        <span class="badge ${status}">${status}</span>
      </div>
      <p class="notes">${escapeHtml(project.notes || "")}</p>
      <div class="progress-row">
        <div class="bar"><span style="width:${stats.pct}%"></span></div>
        <div class="progress-meta">
          <span>${stats.done}/${stats.total} done</span>
          <span>${stats.pct}%</span>
        </div>
      </div>
      <div class="project-links">
        <a href="${escapeAttr(project.url)}" target="_blank" rel="noopener" data-stop>Staging</a>
        ${project.pr ? `<a href="${escapeAttr(project.pr)}" target="_blank" rel="noopener" data-stop>PR</a>` : ""}
        ${project.pages ? `<span class="sub">${project.pages} pages</span>` : ""}
      </div>
    `;
    card.addEventListener("click", (event) => {
      if (event.target.closest("[data-stop]")) return;
      openProject(project.id);
    });
    els.board.appendChild(card);
  }
}

function openProject(projectId) {
  const project = state.data.projects.find((p) => p.id === projectId);
  if (!project) return;
  state.activeId = projectId;

  const stats = checklistStats(projectId);
  const status = effectiveStatus(project);
  const doneMap = ensureProjectProgress(projectId).done;

  els.dlgType.textContent = `${project.type} · ${status}`;
  els.dlgName.textContent = project.name;
  els.dlgMeta.textContent = `${project.client}${project.pages ? ` · ~${project.pages} pages` : ""} — ${project.notes || ""}`;
  els.dlgBar.style.width = `${stats.pct}%`;
  els.dlgCount.textContent = `${stats.done} of ${stats.total} checklist items complete`;
  els.dlgUrl.href = project.url;
  if (project.pr) {
    els.dlgPr.href = project.pr;
    els.dlgPr.hidden = false;
  } else {
    els.dlgPr.hidden = true;
  }

  const groups = new Map();
  for (const item of state.data.checklistTemplate) {
    if (!groups.has(item.group)) groups.set(item.group, []);
    groups.get(item.group).push(item);
  }

  els.dlgGroups.innerHTML = "";
  for (const [group, items] of groups) {
    const section = document.createElement("section");
    section.className = "group";
    section.innerHTML = `<h4>${escapeHtml(group)}</h4>`;
    for (const item of items) {
      const row = document.createElement("div");
      const checked = Boolean(doneMap[item.id]);
      row.className = `todo${checked ? " done" : ""}`;
      const inputId = `${projectId}-${item.id}`;
      row.innerHTML = `
        <input type="checkbox" id="${inputId}" ${checked ? "checked" : ""} />
        <label for="${inputId}">${escapeHtml(item.label)}</label>
      `;
      row.querySelector("input").addEventListener("change", (event) => {
        const prog = ensureProjectProgress(projectId);
        if (event.target.checked) prog.done[item.id] = true;
        else delete prog.done[item.id];
        deriveStatusOverride(projectId);
        saveProgress();
        openProject(projectId);
        renderBoard();
      });
      section.appendChild(row);
    }
    els.dlgGroups.appendChild(section);
  }

  if (!els.projectDialog.open) els.projectDialog.showModal();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll("'", "&#39;");
}

function exportProgress() {
  const payload = {
    exportedAt: new Date().toISOString(),
    progress: state.progress,
    settings: (() => {
      const s = loadSettings();
      return { accountId: s.accountId || "", userAgent: s.userAgent || "" };
    })(),
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `launch-base-progress-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

async function importProgress(file) {
  const text = await file.text();
  const parsed = JSON.parse(text);
  if (!parsed || typeof parsed !== "object" || !parsed.progress) {
    throw new Error("Invalid progress file");
  }
  state.progress = parsed.progress;
  saveProgress();
  renderBoard();
  if (state.activeId) openProject(state.activeId);
}

function bindEvents() {
  els.search.addEventListener("input", () => {
    state.query = els.search.value.trim().toLowerCase();
    renderBoard();
  });

  els.statusFilters.addEventListener("click", (event) => {
    const btn = event.target.closest("[data-status]");
    if (!btn) return;
    state.filterStatus = btn.dataset.status;
    for (const chip of els.statusFilters.querySelectorAll(".chip")) {
      chip.classList.toggle("active", chip === btn);
    }
    renderBoard();
  });

  els.btnSettings.addEventListener("click", () => {
    const settings = loadSettings();
    els.bcAccount.value = settings.accountId || "";
    els.bcToken.value = settings.token || "";
    els.bcUa.value = settings.userAgent || "NearMeOS LaunchBase (ops@racecomputerservices.com)";
    els.settingsDialog.showModal();
  });

  document.getElementById("settings-form").addEventListener("submit", (event) => {
    const submitter = event.submitter;
    if (submitter && submitter.value === "cancel") return;
    saveSettings({
      accountId: els.bcAccount.value.trim(),
      token: els.bcToken.value.trim(),
      userAgent: els.bcUa.value.trim(),
    });
  });

  els.btnCopyEnv.addEventListener("click", async () => {
    const settings = {
      accountId: els.bcAccount.value.trim(),
      token: els.bcToken.value.trim(),
      userAgent: els.bcUa.value.trim(),
    };
    const snippet = [
      `export BASECAMP_ACCOUNT_ID="${settings.accountId}"`,
      `export BASECAMP_ACCESS_TOKEN="${settings.token}"`,
      `export BASECAMP_USER_AGENT="${settings.userAgent || "NearMeOS LaunchBase (you@example.com)"}"`,
      "python scripts/basecamp_sync.py --dry-run",
    ].join("\n");
    await navigator.clipboard.writeText(snippet);
    els.btnCopyEnv.textContent = "Copied";
    setTimeout(() => {
      els.btnCopyEnv.textContent = "Copy env snippet";
    }, 1600);
  });

  els.btnExport.addEventListener("click", exportProgress);
  els.btnImport.addEventListener("click", () => els.importFile.click());
  els.importFile.addEventListener("change", async () => {
    const file = els.importFile.files?.[0];
    if (!file) return;
    try {
      await importProgress(file);
    } catch (error) {
      alert(`Import failed: ${error.message || error}`);
    } finally {
      els.importFile.value = "";
    }
  });

  els.dlgClose.addEventListener("click", () => els.projectDialog.close());
  els.projectDialog.addEventListener("click", (event) => {
    if (event.target === els.projectDialog) els.projectDialog.close();
  });

  els.dlgReset.addEventListener("click", () => {
    if (!state.activeId) return;
    if (!confirm("Reset this project's checklist?")) return;
    state.progress[state.activeId] = { done: {}, statusOverride: null };
    saveProgress();
    openProject(state.activeId);
    renderBoard();
  });
}

async function main() {
  const response = await fetch("./data/projects.json", { cache: "no-store" });
  if (!response.ok) throw new Error("Could not load projects.json");
  state.data = await response.json();
  state.progress = loadProgress();
  bindEvents();
  renderBoard();
}

main().catch((error) => {
  els.board.innerHTML = `<p class="hint">Failed to load dashboard: ${escapeHtml(error.message || String(error))}</p>`;
});
