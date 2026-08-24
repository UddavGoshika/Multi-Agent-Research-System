from app.agents.base import BaseAgent
from app.tools.web_search import web_search

SYSTEM_PROMPT = """You are a research agent. You are given a question and a
set of raw web search results (title, url, snippet). Write a concise,
factual summary (3-5 sentences) that answers the question using ONLY the
provided snippets. After the summary, do not invent sources beyond the
ones given."""


class ResearcherAgent(BaseAgent):
    name = "researcher"
    role = "Searches the web and summarizes findings for each sub-question"

    async def run(self, context: dict) -> dict:
        sub_questions = context["sub_questions"]
        findings = []

        for question in sub_questions:
            results = await web_search(question, max_results=5)
            sources_text = "\n".join(
                f"- {r['title']} ({r['url']}): {r['snippet']}" for r in results
            ) or "No search results found."

            summary = await self.llm.complete(
                SYSTEM_PROMPT,
                f"Question: {question}\n\nSearch results:\n{sources_text}",
            )

            findings.append(
                {
                    "question": question,
                    "summary": summary,
                    "sources": [{"title": r["title"], "url": r["url"]} for r in results],
                }
            )

        return {"findings": findings}
