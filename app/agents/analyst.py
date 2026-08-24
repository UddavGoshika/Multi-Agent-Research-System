from app.agents.base import BaseAgent

SYSTEM_PROMPT = """You are an analyst agent. You receive research findings
(question + summary pairs) about a topic. Identify: (1) the key insights,
(2) any contradictions or open questions across the findings, (3) how the
findings relate to each other. Return ONLY JSON in this exact shape:
{"key_insights": ["...", "..."], "gaps_or_contradictions": ["..."], "synthesis": "2-3 sentence paragraph"}"""


class AnalystAgent(BaseAgent):
    name = "analyst"
    role = "Synthesizes research findings into structured insights"

    async def run(self, context: dict) -> dict:
        findings = context["findings"]
        findings_text = "\n\n".join(
            f"Q: {f['question']}\nA: {f['summary']}" for f in findings
        )
        data = await self.llm.complete_json(
            SYSTEM_PROMPT, f"Topic: {context['topic']}\n\nFindings:\n{findings_text}"
        )
        return {"analysis": data}
