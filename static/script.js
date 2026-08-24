const form = document.getElementById("research-form");
const topicInput = document.getElementById("topic");
const submitBtn = document.getElementById("submit-btn");
const logEl = document.getElementById("log");
const reportEl = document.getElementById("report");
const statusBadge = document.getElementById("status-badge");
const modelBadge = document.getElementById("model-badge");
const stations = document.querySelectorAll(".station");

document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach((t) => t.classList.add("hidden"));
    btn.classList.add("active");
    document.getElementById("tab-" + btn.dataset.tab).classList.remove("hidden");
  });
});

function setStation(agentName, state) {
  const station = document.querySelector(`.station[data-agent="${agentName}"]`);
  if (!station) return;
  station.classList.remove("running", "done", "error");
  if (state) station.classList.add(state);
  const statusEl = station.querySelector('[data-role="status"]');
  statusEl.textContent = state === "running" ? "running…" : state === "done" ? "done" : state === "error" ? "error" : "pending";
}

function resetStations() {
  stations.forEach((s) => {
    s.classList.remove("running", "done", "error");
    s.querySelector('[data-role="status"]').textContent = "pending";
  });
}

function appendLog(text, cls = "") {
  const line = document.createElement("div");
  line.className = "log-line " + cls;
  const ts = new Date().toLocaleTimeString();
  line.innerHTML = `<span class="ts">${ts}</span>${text}`;
  logEl.appendChild(line);
  logEl.scrollTop = logEl.scrollHeight;
}

function renderMarkdown(md) {
  // Minimal, dependency-free markdown rendering: headings, bold, links, lists.
  let html = md
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  html = html
    .replace(/^### (.*$)/gim, "<h3>$1</h3>")
    .replace(/^## (.*$)/gim, "<h2>$1</h2>")
    .replace(/^# (.*$)/gim, "<h1>$1</h1>")
    .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")
    .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    .replace(/^- (.*$)/gim, "<li>$1</li>");

  html = html.replace(/(<li>.*<\/li>\n?)+/g, (match) => `<ul>${match}</ul>`);
  html = html
    .split("\n\n")
    .map((block) => (/^<(h1|h2|h3|ul)/.test(block.trim()) ? block : `<p>${block}</p>`))
    .join("\n");

  return html;
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const topic = topicInput.value.trim();
  if (!topic) return;

  logEl.innerHTML = "";
  reportEl.innerHTML = '<p class="placeholder">Working… the report will appear here once the writer agent finishes.</p>';
  resetStations();
  submitBtn.disabled = true;
  statusBadge.textContent = "running";
  statusBadge.className = "badge badge-live running";

  const url = `/api/research?topic=${encodeURIComponent(topic)}`;
  const source = new EventSource(url);

  source.onmessage = (event) => {
    const data = JSON.parse(event.data);

    switch (data.type) {
      case "start":
        modelBadge.textContent = `model: ${data.model}`;
        appendLog(`Pipeline started for: <b>${data.topic}</b>`, "event-start");
        break;
      case "agent_start":
        setStation(data.agent, "running");
        appendLog(`<b>${data.agent}</b> started — ${data.role}`, "event-agent_start");
        break;
      case "agent_done":
        setStation(data.agent, "done");
        appendLog(`<b>${data.agent}</b> done in ${data.elapsed_seconds}s — ${data.preview}`, "event-agent_done");
        break;
      case "agent_error":
        setStation(data.agent, "error");
        appendLog(`<b>${data.agent}</b> error: ${data.error}`, "event-agent_error");
        break;
      case "final":
        reportEl.innerHTML = renderMarkdown(data.report);
        document.querySelector('.tab-btn[data-tab="report"]').click();
        statusBadge.textContent = "done";
        statusBadge.className = "badge badge-live done";
        submitBtn.disabled = false;
        source.close();
        break;
      case "fatal":
        appendLog(`Pipeline failed: ${data.error}`, "event-fatal");
        statusBadge.textContent = "error";
        statusBadge.className = "badge badge-live error";
        submitBtn.disabled = false;
        source.close();
        break;
    }
  };

  source.onerror = () => {
    appendLog("Connection closed or errored.", "event-fatal");
    submitBtn.disabled = false;
    source.close();
  };
});
