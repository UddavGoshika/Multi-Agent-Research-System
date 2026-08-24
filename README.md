<div align="center">

# 🧠 Multi-Agent Research System

### **From a question → to web research → to verified intelligence → to a polished report.**

A production-shaped **multi-agent LLM research pipeline** where specialized AI agents collaborate to plan research, search the live web, analyze evidence, and generate a structured report — while streaming the entire mission to a real-time **AI Mission Control** dashboard.

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Streaming-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![LLM](https://img.shields.io/badge/LLM-LiteLLM-6C63FF?style=for-the-badge)](https://github.com/BerriAI/litellm)
[![Search](https://img.shields.io/badge/Web_Search-DuckDuckGo-DE5833?style=for-the-badge\&logo=duckduckgo\&logoColor=white)](https://duckduckgo.com/)
[![Tests](https://img.shields.io/badge/Tests-pytest-0A9EDC?style=for-the-badge\&logo=pytest\&logoColor=white)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

### 🔎 Research  →  🧠 Analyze  →  ✍️ Synthesize  →  📚 Deliver

<br/>

**[🚀 Live Demo](#-live-demo)**    **[🏗️ Architecture](#️-architecture)**    **[⚡ Quick Start](#-quick-start)**    **[🧪 Testing](#-testing)**

</div>

---

# 🌌 Welcome to Mission Control

What happens when you give an AI a difficult research question?

Instead of asking one model to:

> Search → Think → Write

this system divides the mission among **specialized agents**.

```text
                         👤 USER
                           │
                           │ Research Question
                           ▼
                  ┌──────────────────┐
                  │   🧠 PLANNER     │
                  │                  │
                  │ Break question   │
                  │ into subtopics   │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  🔎 RESEARCHER   │
                  │                  │
                  │ Search live web  │
                  │ Gather evidence  │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │   📊 ANALYST     │
                  │                  │
                  │ Compare evidence │
                  │ Find insights    │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │    ✍️ WRITER     │
                  │                  │
                  │ Build final      │
                  │ research report  │
                  └────────┬─────────┘
                           │
                           ▼
                     📄 FINAL REPORT
```

The interesting part isn't simply that an LLM generates text.

The interesting part is the **system around the LLM**:

> **Specialized agents + real tools + structured handoffs + streaming execution + provider abstraction + testing + deployment.**

---

# 🚀 Live Demo

> ### 🌐 Try the system
>
> 🔗 **[Add your deployed URL here]**
>
> ### 🎥 20–30 Second Walkthrough
>
> ▶️ **[Add your demo video / GIF here]**

### 💡 Try asking it:

```text
"What are the major trends shaping humanoid robotics in 2026?"
```

or:

```text
"Compare the current AI chip ecosystems of NVIDIA, AMD and Google."
```

or:

```text
"How is AI changing software engineering?"
```

Then watch the mission unfold:

```text
🟢 Planner
      ↓
🔵 Researcher
      ↓
🟣 Analyst
      ↓
🟡 Writer
      ↓
✨ Report Ready
```

---

# ✨ Why This Isn't Just Another AI Chatbot

A typical portfolio chatbot looks like:

```text
User
 │
 ▼
Prompt
 │
 ▼
LLM
 │
 ▼
Answer
```

This project looks more like:

```text
                        USER
                          │
                          ▼
                   🧠 ORCHESTRATOR
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          PLANNER      RESEARCHER    ANALYST
             │            │            │
             │            ▼            │
             │       🌐 WEB SEARCH     │
             │            │            │
             └────────────┼────────────┘
                          ▼
                       WRITER
                          │
                          ▼
                    📚 REPORT
```

### What makes it interesting?

| Capability            | This Project                | Typical AI Demo         |
| --------------------- | --------------------------- | ----------------------- |
| 🤖 Agent architecture | 4 specialized agents        | 1 chatbot               |
| 🧩 Responsibilities   | Typed agent contracts       | One giant prompt        |
| 🌐 External tools     | Live web search             | No tools                |
| 📚 Grounding          | Retrieved evidence          | Possible hallucinations |
| ⚡ Streaming           | Server-Sent Events          | Blocking response       |
| 🎛️ Observability     | Live Mission Control UI     | Spinner                 |
| 🧠 LLM abstraction    | LiteLLM                     | Single provider         |
| 🧪 Testing            | Mocked deterministic agents | Manual testing          |
| 🐳 Deployment         | Docker + Render             | Localhost only          |
| 🔀 Extensibility      | Critic, branching, memory   | Hard-coded chain        |

---

# 🏗️ Architecture

```text
                       🌐 BROWSER
                           │
                           │
                    GET /api/research
                           │
                           ▼
                 ┌────────────────────┐
                 │    ⚡ FastAPI       │
                 │                    │
                 │ StreamingResponse  │
                 │       + SSE        │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │   🎯 ORCHESTRATOR  │
                 │                    │
                 │ Async Generator    │
                 │ Context Manager    │
                 └─────────┬──────────┘
                           │
                           ▼

      ┌──────────────────────────────────────────────────┐
      │              🤖 AGENT PIPELINE                   │
      │                                                  │
      │  ┌──────────┐     ┌────────────┐                │
      │  │ 🧠       │     │ 🔎         │                │
      │  │ PLANNER  │ ──► │ RESEARCHER │                │
      │  └──────────┘     └─────┬──────┘                │
      │                         │                        │
      │                         ▼                        │
      │                   🌐 WEB SEARCH                  │
      │                         │                        │
      │                         ▼                        │
      │                  ┌────────────┐                  │
      │                  │ 📊 ANALYST │                  │
      │                  └─────┬──────┘                  │
      │                        │                         │
      │                        ▼                         │
      │                  ┌────────────┐                  │
      │                  │ ✍️ WRITER  │                  │
      │                  └─────┬──────┘                  │
      │                        │                         │
      └────────────────────────┼─────────────────────────┘
                               │
                               ▼
                         📄 FINAL REPORT
```

---

# 🧠 Meet the Research Team

Every agent has **one job**.

That's intentional.

Instead of building one enormous prompt that tries to reason about everything, the system uses focused workers with clear inputs and outputs.

---

## 🧠 01 — Planner

### Mission: **Turn the question into a research strategy.**

The Planner receives the user's topic and creates a structured research plan.

For example:

```text
Question:
"How is generative AI changing software engineering?"

                 │
                 ▼

            🧠 PLANNER
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
   Developer   Tooling   Economics
   workflow    changes   impact
        │        │        │
        └────────┼────────┘
                 ▼
          Research Plan
```

It determines:

* 🔹 Important sub-questions
* 🔹 Research areas
* 🔹 What evidence is needed
* 🔹 How the Researcher should investigate the topic

---

# 🔎 02 — Researcher

### Mission: **Find evidence on the live web.**

This is where the system moves beyond a pure LLM pipeline.

The Researcher has access to a real search tool:

```text
web_search()
```

The flow becomes:

```text
Research Plan
      │
      ▼
🔎 Search Query
      │
      ▼
🌐 Live Web
      │
      ▼
📄 Retrieved Sources
      │
      ▼
🧠 LLM
      │
      ▼
Structured Findings
```

The agent doesn't simply ask the LLM:

> "Tell me about this topic."

Instead, it gathers external evidence and passes that evidence into the analysis pipeline.

---

# 📊 03 — Analyst

### Mission: **Turn raw research into meaningful insights.**

The Analyst receives the Researcher's findings and attempts to:

* 🔍 Identify patterns
* ⚖️ Compare conflicting evidence
* 🧩 Connect findings
* 🚨 Detect gaps
* 📌 Extract important conclusions
* 📝 Prepare evidence for the Writer

Conceptually:

```text
                 🔎 RESEARCHER
                       │
                       ▼
              ┌──────────────────┐
              │ Raw Findings     │
              │                  │
              │ Source A         │
              │ Source B         │
              │ Source C         │
              │ Source D         │
              └────────┬─────────┘
                       │
                       ▼
                 📊 ANALYST
                       │
                       ▼
              ┌──────────────────┐
              │ Key Insights     │
              │                  │
              │ • Pattern 1      │
              │ • Pattern 2      │
              │ • Comparison     │
              │ • Caveat         │
              └──────────────────┘
```

---

# ✍️ 04 — Writer

### Mission: **Transform the analysis into a polished research report.**

The Writer receives the structured analytical context and produces the final Markdown report.

Output can include:

* 📌 Executive summary
* 🔍 Key findings
* 📊 Detailed analysis
* 💡 Conclusions
* 📚 Source references

The Writer isn't responsible for doing the research.

It focuses on **communication and synthesis**.

That's an important separation of concerns.

---

# 🔄 Agent Handoffs

The agents communicate through a shared context.

Each agent follows a simple contract:

```python
run(context) -> partial_update
```

Conceptually:

```text
Planner
  │
  │ plan
  ▼
Shared Context
  │
  ▼
Researcher
  │
  │ findings
  ▼
Shared Context
  │
  ▼
Analyst
  │
  │ analysis
  ▼
Shared Context
  │
  ▼
Writer
  │
  │ report
  ▼
Final Result
```

This makes each worker:

* 🧩 Small
* 🧪 Testable
* 🔄 Replaceable
* 🧠 Easy to reason about

---

# ⚡ Real-Time Mission Control

The entire pipeline is observable.

Instead of waiting 30 seconds and receiving:

> "Here's your report."

the browser receives events as the system works.

### Event flow

```text
                    BACKEND
                       │
                       ▼
                Agent starts
                       │
                       ▼
                 SSE Event
                       │
                       ▼
                    BROWSER
                       │
                       ▼
              Mission Control UI
```

Example events:

```json
{
  "type": "agent_start",
  "agent": "researcher"
}
```

```json
{
  "type": "agent_done",
  "agent": "researcher"
}
```

```json
{
  "type": "final",
  "report": "..."
}
```

---

# 📡 Why Server-Sent Events?

This project uses **SSE rather than WebSockets** because the primary communication pattern is:

```text
SERVER ───────────────► CLIENT
```

The browser doesn't need a persistent bidirectional command channel.

SSE gives us:

* ⚡ Simple streaming
* 🌐 Native browser support
* 🔄 Automatic reconnection behavior
* 🪶 Less infrastructure than WebSockets
* 📦 Easy integration with FastAPI

Frontend:

```javascript
const source = new EventSource("/api/research?topic=AI");

source.onmessage = (event) => {
    const data = JSON.parse(event.data);
    updateMissionControl(data);
};
```

Backend:

```python
return StreamingResponse(
    orchestrator.run(topic),
    media_type="text/event-stream"
)
```

Simple, readable, and appropriate for this architecture.

---

# 🌐 Real Web Research

The Researcher uses a live web search tool powered by DuckDuckGo.

```text
                 🔎 Researcher
                       │
                       ▼
                web_search()
                       │
                       ▼
              🌐 DuckDuckGo
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
           Source A  Source B  Source C
              │        │        │
              └────────┼────────┘
                       ▼
                 🧠 LLM
                       │
                       ▼
                Findings
```

This makes the system substantially more useful than asking a model to rely exclusively on its training knowledge.

---

# 🧠 Provider-Agnostic LLM Layer

The project uses **LiteLLM** to avoid coupling the entire application to one model provider.

You can switch between providers through configuration.

```text
                    🧠 Agent
                       │
                       ▼
                  LLM Client
                       │
                       ▼
                    LiteLLM
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       OpenAI      Anthropic       Groq
                                     │
                                  Ollama
```

The orchestration layer doesn't need to care which model is underneath.

That's an important architectural decision because:

> **Model providers change faster than application architecture should.**

---

# 🧪 Testing Strategy

The project doesn't require a paid LLM API key just to run tests.

The LLM client is mocked.

```text
                 🧪 pytest
                    │
                    ▼
             Agent Under Test
                    │
                    ▼
              Mock LLM Client
                    │
                    ▼
             Deterministic Result
```

This makes the suite:

* ⚡ Fast
* 💰 Free
* 🔁 Repeatable
* 🤖 CI-friendly

Run:

```bash
pytest tests/ -v
```

---

# 🧰 API

## Research Endpoint

```http
GET /api/research?topic=<topic>
```

Optional model override:

```http
GET /api/research?topic=<topic>&model=<model>
```

The endpoint returns:

```text
Content-Type: text/event-stream
```

Possible events:

```text
start
agent_start
agent_done
agent_error
final
fatal
```

### Example lifecycle

```text
start
  ↓
agent_start: planner
  ↓
agent_done: planner
  ↓
agent_start: researcher
  ↓
agent_done: researcher
  ↓
agent_start: analyst
  ↓
agent_done: analyst
  ↓
agent_start: writer
  ↓
agent_done: writer
  ↓
final
```

---

# 🎨 Mission Control UI

The frontend is intentionally built without React, Vue, or another frontend framework.

Why?

Because this is a portfolio project.

A reviewer should be able to open:

```text
static/
├── index.html
├── style.css
└── script.js
```

and understand the entire frontend quickly.

The interface behaves like a small AI research operations center:

```text
┌──────────────────────────────────────────────────────────────┐
│ 🧠 AI RESEARCH MISSION CONTROL                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  RESEARCH TOPIC                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ How is AI transforming software engineering?           │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│                    [ 🚀 START RESEARCH ]                     │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   🧠                🔎                 📊              ✍️     │
│ PLANNER ─────────► RESEARCHER ──────► ANALYST ──────► WRITER │
│   🟢                  🔵                 ⚪              ⚪    │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 📡 LIVE MISSION LOG                                          │
│                                                              │
│ 10:41:02  🧠 Planner started                                 │
│ 10:41:05  🧠 Research plan generated                        │
│ 10:41:06  🔎 Researcher started                              │
│ 10:41:10  🌐 Searching the web...                            │
│ 10:41:13  📚 8 sources retrieved                             │
│ 10:41:16  📊 Analyst started                                 │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 📄 FINAL REPORT                                              │
│                                                              │
│  Research findings appear here...                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

# 🗺️ End-to-End Execution

Here's what happens after the user presses **Start Research**.

```text
      👤 USER
        │
        │ "Research quantum computing"
        ▼
   🧠 PLANNER
        │
        │ Break into subtopics
        ▼
   📋 RESEARCH PLAN
        │
        ▼
   🔎 RESEARCHER
        │
        ├──────────────► 🌐 Web Search
        │
        ├──────────────► 🌐 Web Search
        │
        └──────────────► 🌐 Web Search
        │
        ▼
   📚 FINDINGS
        │
        ▼
   📊 ANALYST
        │
        ▼
   🧠 SYNTHESIS
        │
        ▼
   ✍️ WRITER
        │
        ▼
   📄 MARKDOWN REPORT
        │
        ▼
   👤 USER
```

Every major transition is streamed to the browser.

---

# 📦 Project Structure

```text
multi-agent-research-system/
│
├── 📁 app/
│   │
│   ├── 🤖 agents/
│   │   ├── base.py
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   ├── analyst.py
│   │   └── writer.py
│   │
│   ├── 🔧 tools/
│   │   └── web_search.py
│   │
│   ├── 🧠 llm_client.py
│   │
│   ├── 🎯 orchestrator.py
│   │
│   └── ⚡ main.py
│
├── 📁 static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── 📁 tests/
│   └── pytest suite
│
├── 🐳 Dockerfile
├── 🚀 render.yaml
├── 📋 requirements.txt
├── 🔐 .env.example
└── 📄 LICENSE
```

---

# 🧱 Technology Stack

| Layer        | Technology    | Why it exists               |
| ------------ | ------------- | --------------------------- |
| ⚡ Backend    | FastAPI       | Async API + streaming       |
| 📡 Transport | SSE           | Live server → client events |
| 🤖 Agents    | Custom Python | Clear orchestration         |
| 🧠 LLM       | LiteLLM       | Provider abstraction        |
| 🌐 Search    | DuckDuckGo    | Free live research          |
| 🎨 Frontend  | Vanilla JS    | Zero build complexity       |
| 🧪 Tests     | pytest        | Deterministic testing       |
| 🐳 Container | Docker        | Reproducible deployment     |
| ☁️ Hosting   | Render        | Simple public deployment    |

---

# ⚡ Quick Start

## 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd multi-agent-research-system
```

---

## 2️⃣ Create a virtual environment

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure your LLM

```bash
cp .env.example .env
```

Then configure one provider.

For example:

```env
GROQ_API_KEY=your_api_key_here
```

You can also configure another supported provider through the LiteLLM layer.

---

## 5️⃣ Start the application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

---

# ☁️ Deploy

## 🟣 Option A — Render

A `render.yaml` is included.

### Deployment flow

```text
GitHub
  │
  ▼
Render
  │
  ▼
render.yaml
  │
  ▼
Environment Variables
  │
  ▼
Docker Build
  │
  ▼
🚀 Deployment
  │
  ▼
🌐 Public Research System
```

### Steps

1. Push the repository to GitHub.
2. Create a new Render Blueprint.
3. Connect your repository.
4. Add your LLM API key.
5. Deploy.
6. Copy the public URL into the README.

---

# 🐳 Docker

Build:

```bash
docker build -t agent-research .
```

Run:

```bash
docker run \
  -p 8000:8000 \
  --env-file .env \
  agent-research
```

Then visit:

```text
http://localhost:8000
```

---

# 🔐 Environment Variables

Example:

```env
MODEL_NAME=groq/llama-3.3-70b-versatile

GROQ_API_KEY=your_key_here
```

Keep secrets out of Git.

```text
.env
   🚫
   │
   └── never commit

.env.example
   ✅
   │
   └── safe configuration template
```

---

# 🧪 Testing

Run:

```bash
pytest tests/ -v
```

No paid LLM API is required because the model layer is mocked.

### Testing philosophy

The goal isn't just:

> "Does the model give a good answer?"

Instead, test the system around the model:

```text
🧪 Agent Input
      │
      ▼
🧠 Agent Logic
      │
      ▼
🤖 Mocked LLM
      │
      ▼
📦 Structured Output
      │
      ▼
✅ Assertions
```

This makes failures reproducible and CI-friendly.

---

# 🔮 Future Roadmap

The current sequential architecture is intentionally simple.

There are several natural paths to evolve it.

---

## 🧐 Critic Agent

Add a fifth agent:

```text
Planner
   ↓
Researcher
   ↓
Analyst
   ↓
Writer
   ↓
🧐 Critic
   │
   ├── ✅ Good → Return
   │
   └── ❌ Weak → Research again
```

The Critic could check:

* Unsupported claims
* Missing sources
* Contradictions
* Weak evidence
* Citation coverage

---

# 🔀 Conditional Agent Graph

Instead of always executing:

```text
Planner → Researcher → Analyst → Writer
```

move toward:

```text
                 Planner
                    │
                    ▼
               Researcher
                    │
                    ▼
                 Analyst
                    │
             ┌──────┴──────┐
             │             │
          Enough?        Missing?
             │             │
             ▼             ▼
           Writer      Researcher
                           │
                           └──────► Analyst
```

This would make the system adaptive rather than strictly sequential.

---

# 🧠 Persistent Research Memory

Add a vector store or other retrieval layer:

```text
             New Research
                  │
                  ▼
             Memory Search
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
 Existing Knowledge     New Research
        │                   │
        └─────────┬─────────┘
                  ▼
              Analysis
```

Repeated research topics wouldn't necessarily need to start from zero.

---

# ✨ Token Streaming

Today, the Writer produces the final report as an agent result.

A future version could stream the actual report generation token-by-token:

```text
✍️ Writer

Generating report...

"The current landscape of artificial
intelligence suggests that..."
```

This would make the UI feel even more alive.

---

# 🔐 Production Hardening

For a public deployment, I'd add:

* 🔑 Authentication
* 🚦 Rate limiting
* 🛡️ Request validation
* 📊 Usage metrics
* 🧾 Persistent research history
* 🔒 API key protection
* 🗄️ Database persistence
* 📈 Observability
* 🧹 Search result sanitization

---

# 💼 Interview Talking Points

This project is designed to give you real engineering conversations.

### 🧠 "Why multiple agents?"

Because each stage has a different responsibility.

The Planner optimizes **task decomposition**.

The Researcher optimizes **information retrieval**.

The Analyst optimizes **reasoning over evidence**.

The Writer optimizes **communication**.

This creates clearer contracts and makes individual components easier to test and replace.

---

### 🌐 "Why use a search tool?"

Because an LLM's internal knowledge is not guaranteed to be current.

The Researcher can retrieve fresh evidence before analysis.

---

### 📡 "Why SSE instead of WebSockets?"

The dominant communication pattern is server → client.

SSE provides a lightweight, browser-native streaming mechanism without requiring bidirectional socket infrastructure.

---

### 🧠 "Why LiteLLM?"

Because the application shouldn't be architecturally coupled to one LLM vendor.

The model is an implementation detail behind the LLM client.

---

### 🧪 "Why mock the LLM?"

LLMs are nondeterministic and expensive compared with normal unit tests.

Mocking gives fast, deterministic tests while keeping integration testing separate.

---

### 🔀 "How would you improve the pipeline?"

I'd add a Critic agent and conditional execution.

If the Critic detects weak evidence, the Researcher could automatically perform another search cycle.

---

# 🎯 What This Project Demonstrates

This project showcases far more than prompt engineering.

```text
                 🧠 LLM ENGINEERING
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Agents         Tools       Structured IO
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                 🎯 ORCHESTRATION
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
        📡 Streaming          🌐 Web Search
             │                     │
             └──────────┬──────────┘
                        ▼
                  🧪 TESTING
                        │
                        ▼
                  🐳 DEPLOYMENT
```

### Skills demonstrated

* 🐍 Python
* ⚡ FastAPI
* 🤖 Multi-agent architecture
* 🧠 LLM integration
* 🌐 Tool calling
* 🔎 Web research
* 📡 Server-Sent Events
* 🔄 Async programming
* 📦 Structured agent contracts
* 🧪 Automated testing
* 🐳 Docker
* ☁️ Cloud deployment
* 🏗️ Backend architecture
* 🎨 Real-time UI design

---

# 📸 Screenshots

Add your real screenshots here once the UI is finished.

Recommended images:

```text
docs/
├── 🖥️ mission-control.png
├── 🔎 research-progress.png
├── 📊 agent-pipeline.png
└── 📄 final-report.png
```

### Suggested README layout

```markdown
## 🖥️ Mission Control

![Mission Control](docs/mission-control.png)

## 🔎 Live Research

![Research](docs/research-progress.png)

## 📄 Final Report

![Report](docs/final-report.png)
```

A GIF showing the pipeline progressing is especially valuable because the **streaming behavior is one of the project's strongest differentiators**.

---

# 🎥 Recommended Portfolio Demo

Keep the demo around **20–30 seconds**.

### 00–04 sec

Enter:

```text
"How is generative AI changing software development?"
```

### 04–08 sec

Show:

```text
🧠 Planner
```

breaking the topic into research questions.

### 08–14 sec

Show:

```text
🔎 Researcher
```

performing live searches.

### 14–18 sec

Show:

```text
📊 Analyst
```

turning sources into insights.

### 18–24 sec

Show:

```text
✍️ Writer
```

generating the report.

### Final frame

```text
┌─────────────────────────────┐
│ 📚 Research Complete        │
│                             │
│ 8 sources                   │
│ 4 agents                    │
│ 1 synthesized report        │
│                             │
│       ✨ Mission Complete   │
└─────────────────────────────┘
```

---

# 📄 Resume Bullet

> **Built and deployed a multi-agent LLM research system using FastAPI, SSE streaming, LiteLLM, and live web search, orchestrating specialized Planner, Researcher, Analyst, and Writer agents to transform research questions into evidence-grounded reports; added mocked-LLM testing and containerized cloud deployment.**

### Shorter version

> **Built a multi-agent AI research platform with FastAPI, SSE, LiteLLM, and live web search, using specialized planning, research, analysis, and writing agents with real-time execution streaming.**

---

# 🏆 The Big Idea

This project demonstrates an important shift:

```text
             ❌ OLD
        "Ask the AI a question"
                 │
                 ▼
              Answer


             ✅ THIS
        "Build a system around AI"
                 │
                 ▼
       ┌────────────────────┐
       │      Planner       │
       ├────────────────────┤
       │     Researcher     │
       ├────────────────────┤
       │      Analyst       │
       ├────────────────────┤
       │       Writer       │
       ├────────────────────┤
       │    Search Tools    │
       ├────────────────────┤
       │    Orchestrator    │
       ├────────────────────┤
       │   Live Streaming   │
       ├────────────────────┤
       │      Testing       │
       └────────────────────┘
                 │
                 ▼
          📚 RESEARCH SYSTEM
```

The goal isn't to make an AI that simply **talks**.

The goal is to build an AI system that can **plan, use tools, reason over evidence, collaborate through specialized stages, expose its execution, and produce a useful artifact.**

---

# 📜 License

MIT License.

See [`LICENSE`](LICENSE) for details.

---

<div align="center">

## 🧠 Research Smarter.

## 🔎 Search Deeper.

## 📊 Think in Stages.

## ✍️ Deliver Better.

<br/>

**Built with Python · FastAPI · LiteLLM · SSE · AI Agents**

<br/>

⭐ **Star the repository if you found the architecture useful.**

</div>
