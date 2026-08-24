from app.agents.base import BaseAgent

SYSTEM_PROMPT = """You are a research planning agent. Given a topic, break it
down into 3 to 5 specific, non-overlapping sub-questions that together give
a thorough understanding of the topic. Return ONLY JSON in this exact shape:
{"sub_questions": ["...", "...", "..."]}"""


class PlannerAgent(BaseAgent):
    name = "planner"
    role = "Breaks the research topic into focused sub-questions"

    async def run(self, context: dict) -> dict:
        topic = context["topic"]
        data = await self.llm.complete_json(
            SYSTEM_PROMPT, f"Topic: {topic}"
        )
        sub_questions = data.get("sub_questions", [])[:5]
        if not sub_questions:
            sub_questions = [topic]
        return {"sub_questions": sub_questions}
