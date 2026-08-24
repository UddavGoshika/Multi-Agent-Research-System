"""
Tests use a fake LLM client so the whole pipeline is testable without
any API key or network access to an LLM provider — only the (mocked)
web search is stubbed too, keeping the suite fast and deterministic.
"""
import pytest
from unittest.mock import AsyncMock, patch

from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearcherAgent
from app.agents.analyst import AnalystAgent
from app.agents.writer import WriterAgent


class FakeLLM:
    """Stands in for LLMClient; returns canned responses per call type."""

    async def complete_json(self, system, user):
        if "sub_questions" in system:
            return {"sub_questions": ["What is X?", "Why does X matter?"]}
        if "key_insights" in system:
            return {
                "key_insights": ["Insight A", "Insight B"],
                "gaps_or_contradictions": ["Gap A"],
                "synthesis": "Overall synthesis paragraph.",
            }
        return {}

    async def complete(self, system, user, json_mode=False):
        return "This is a summarized answer based on the given sources."


@pytest.mark.asyncio
async def test_planner_returns_sub_questions():
    agent = PlannerAgent(FakeLLM())
    result = await agent.run({"topic": "quantum computing"})
    assert "sub_questions" in result
    assert len(result["sub_questions"]) == 2


@pytest.mark.asyncio
async def test_researcher_produces_findings_with_sources():
    fake_results = [
        {"title": "Doc 1", "url": "https://example.com/1", "snippet": "..."},
    ]
    with patch("app.agents.researcher.web_search", new=AsyncMock(return_value=fake_results)):
        agent = ResearcherAgent(FakeLLM())
        result = await agent.run(
            {"topic": "quantum computing", "sub_questions": ["What is X?"]}
        )
    assert len(result["findings"]) == 1
    assert result["findings"][0]["sources"][0]["url"] == "https://example.com/1"


@pytest.mark.asyncio
async def test_analyst_returns_structured_analysis():
    agent = AnalystAgent(FakeLLM())
    result = await agent.run(
        {
            "topic": "quantum computing",
            "findings": [{"question": "What is X?", "summary": "X is ..."}],
        }
    )
    assert "key_insights" in result["analysis"]
    assert len(result["analysis"]["key_insights"]) == 2


@pytest.mark.asyncio
async def test_writer_includes_sources_section():
    agent = WriterAgent(FakeLLM())
    result = await agent.run(
        {
            "topic": "quantum computing",
            "findings": [
                {
                    "question": "What is X?",
                    "summary": "X is ...",
                    "sources": [{"title": "Doc 1", "url": "https://example.com/1"}],
                }
            ],
            "analysis": {
                "key_insights": ["A"],
                "gaps_or_contradictions": [],
                "synthesis": "Synth.",
            },
        }
    )
    assert "## Sources" in result["report"]
    assert "https://example.com/1" in result["report"]
