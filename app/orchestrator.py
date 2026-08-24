"""
Orchestrator: drives the four agents in sequence, streaming a status
event before and after each agent runs so the frontend can render a
live "mission control" view of the multi-agent system at work.

The pipeline is intentionally sequential (planner -> researcher ->
analyst -> writer) because each stage depends on the previous one's
output — this is a real dependency graph, not artificial staging.
"""
import json
import logging
import time
from typing import AsyncGenerator

from app.llm_client import LLMClient
from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearcherAgent
from app.agents.analyst import AnalystAgent
from app.agents.writer import WriterAgent

logger = logging.getLogger("orchestrator")


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event)}\n\n"


async def run_pipeline(topic: str, model: str | None = None) -> AsyncGenerator[str, None]:
    llm = LLMClient(model=model)
    context = {"topic": topic}

    agents = [
        PlannerAgent(llm),
        ResearcherAgent(llm),
        AnalystAgent(llm),
        WriterAgent(llm),
    ]

    yield _sse({"type": "start", "topic": topic, "model": llm.model})

    try:
        for agent in agents:
            yield _sse({"type": "agent_start", "agent": agent.name, "role": agent.role})
            t0 = time.time()
            try:
                update = await agent.run(context)
            except Exception as e:
                logger.exception(f"Agent {agent.name} failed")
                yield _sse({"type": "agent_error", "agent": agent.name, "error": str(e)})
                yield _sse({"type": "fatal", "error": f"{agent.name} failed: {e}"})
                return
            context.update(update)
            elapsed = round(time.time() - t0, 2)
            yield _sse(
                {
                    "type": "agent_done",
                    "agent": agent.name,
                    "elapsed_seconds": elapsed,
                    "preview": _preview_for(agent.name, update),
                }
            )

        yield _sse({"type": "final", "report": context["report"], "topic": topic})

    except Exception as e:
        logger.exception("Pipeline failed")
        yield _sse({"type": "fatal", "error": str(e)})


def _preview_for(agent_name: str, update: dict) -> str:
    """Small human-readable preview of each agent's output for the live log."""
    if agent_name == "planner":
        return f"{len(update.get('sub_questions', []))} sub-questions generated"
    if agent_name == "researcher":
        return f"{len(update.get('findings', []))} findings gathered"
    if agent_name == "analyst":
        insights = update.get("analysis", {}).get("key_insights", [])
        return f"{len(insights)} key insights extracted"
    if agent_name == "writer":
        return "Final report drafted"
    return ""
