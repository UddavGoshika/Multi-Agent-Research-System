# 🧠 Multi-Agent Research System

A **multi-agent LLM pipeline** — Planner → Researcher → Analyst → Writer — that
researches any topic on the live web and streams its progress in real time to
a "mission control" style UI. Built to demonstrate practical agentic AI
engineering: agent orchestration, tool-use, structured LLM outputs, and a
production-shaped FastAPI service — not a notebook demo.

**Live demo:** _add your deployed URL here after following [Deploy](#deploy-get-a-live-link-in-5-minutes) below_
**Video/GIF walkthrough:** _add a 20s screen recording here — this matters more than the live link for recruiters skimming your repo_

---

## Why this project

Most "AI chatbot" portfolio projects are a thin LangChain wrapper around one
prompt. This one is built the way a real agentic system is structured:

- **Multiple specialized agents**, each with one job and a typed contract in/out — not one giant prompt.
- **Real tool-use**: the Researcher agent calls a live web search tool and grounds its output in retrieved sources (not hallucinated citations).
- **Streaming orchestration**: agent state is pushed to the client live via Server-Sent Events, so the pipeline's execution is observable, not a black box.
- **Provider-agnostic LLM layer** (via `litellm`): swap OpenAI / Anthropic / Groq / a local Ollama model with one env var — shows you understand LLM infra isn't tied to one vendor.
- **Tested**: agents are unit-tested with a mocked LLM client, so the suite runs in CI without needing a paid API key.
- **Deployable**: Dockerfile + one-click Render config included.

## Architecture

```
                POST /api/research?topic=...
                         │
                         ▼
                 ┌───────────────┐
                 │  Orchestrator │  (async generator, streams SSE events)
                 └───────┬───────┘
                         │
      ┌──────────┬───────┴───────┬───────────┐
      ▼          ▼               ▼           ▼
  ┌────────┐ ┌───────────┐  ┌─────────┐  ┌────────┐
  │Planner │→│Researcher │→ │ Analyst │→ │ Writer │
  └────────┘ └─────┬─────┘  └─────────┘  └────────┘
   sub-Qs          │ web_search() tool        │
                    ▼ (DuckDuckGo, no key)     ▼
              grounded findings          final markdown report
                                          + deduped source list
```

Each agent is a small class (`app/agents/*.py`) with a single `run(context)`
method: it reads what it needs from the shared context dict, does its job,
and returns a partial update. The orchestrator (`app/orchestrator.py`) drives
them in sequence and yields a progress event before/after each one — that's
what powers the live "stations" UI.

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| Backend | FastAPI + `StreamingResponse` (SSE) | async-native, streams agent progress live without websockets complexity |
| LLM layer | `litellm` | one interface across OpenAI/Anthropic/Groq/Ollama — a real design decision recruiters recognize |
| Search tool | `duckduckgo-search` | free, no API key — anyone can clone and run the demo immediately |
| Frontend | Vanilla HTML/CSS/JS + `EventSource` | no build step, easy for a reviewer to read top to bottom in 2 minutes |
| Tests | `pytest` + `pytest-asyncio` + mocked LLM | deterministic, no API cost to run CI |
| Deploy | Docker + Render | free tier, one-click |

## Run it locally

```bash
git clone <your-repo-url>
cd multi-agent-research-system
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env: uncomment ONE provider and set its key.
# Cheapest way to try it: create a free Groq API key at https://console.groq.com/keys

uvicorn app.main:app --reload
# open http://localhost:8000
```

Run the tests (no API key needed — the LLM is mocked):

```bash
pytest tests/ -v
```

## Deploy — get a live link in 5 minutes

**Option A — Render (recommended, free tier, `render.yaml` included):**
1. Push this repo to your GitHub.
2. Go to [render.com](https://render.com) → New → Blueprint → connect your repo. Render reads `render.yaml` automatically.
3. When prompted, paste your `GROQ_API_KEY` (or swap `MODEL_NAME`/keys for OpenAI/Anthropic).
4. Deploy. You get a public `https://your-app.onrender.com` URL — put it at the top of this README and on your resume/LinkedIn.

**Option B — Railway / Fly.io:** both auto-detect the included `Dockerfile` — connect the repo and set the same env vars from `.env.example`.

**Option C — Any VPS:** `docker build -t agent-research . && docker run -p 8000:8000 --env-file .env agent-research`

## API

```
GET /api/research?topic=<topic>&model=<optional override>
```
Returns a `text/event-stream` of JSON events: `start`, `agent_start`,
`agent_done`, `agent_error`, `final` (contains the full markdown report),
`fatal`. See `static/script.js` for a full consumer example.

## Project structure

```
app/
  agents/          planner.py, researcher.py, analyst.py, writer.py, base.py
  tools/           web_search.py
  llm_client.py    provider-agnostic LLM wrapper (litellm)
  orchestrator.py  runs agents, streams SSE progress
  main.py          FastAPI app + routes
static/            index.html, style.css, script.js (mission-control UI)
tests/             pytest suite, mocked LLM
Dockerfile, render.yaml, requirements.txt, .env.example
```

## Possible extensions (good talking points in interviews)

- Add a **critic/reviewer agent** that checks the Writer's report against the Analyst's findings for unsupported claims before returning it.
- Swap the sequential pipeline for a **graph with conditional branching** (e.g. LangGraph) — re-run Researcher if the Analyst flags a gap.
- Add **persistent memory** (e.g. a vector store) so repeated topics don't re-research from scratch.
- Add **streaming token-level output** from the Writer agent instead of waiting for the full report.
- Add **rate limiting / auth** for a public-facing deployment.

## How to describe this on your resume

> Built and deployed a multi-agent LLM research system (FastAPI, SSE streaming,
> provider-agnostic LLM layer via litellm) where specialized agents plan,
> search the live web, synthesize findings, and generate cited reports;
> included a mocked-LLM test suite and one-click cloud deployment.

## License

MIT — see [LICENSE](LICENSE).
