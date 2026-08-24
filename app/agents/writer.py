from app.agents.base import BaseAgent

SYSTEM_PROMPT = """You are a writer agent. You are given a topic, structured
research findings, and an analysis. Write a polished, well-organized report
in Markdown: a short intro, headed sections per key theme, and a closing
takeaway. Keep it factual and grounded only in the given findings/analysis.
Do not fabricate facts. Do not include a sources section — that is added
separately."""


class WriterAgent(BaseAgent):
    name = "writer"
    role = "Writes the final polished report from findings and analysis"

    async def run(self, context: dict) -> dict:
        findings = context["findings"]
        analysis = context["analysis"]
        findings_text = "\n\n".join(
            f"Q: {f['question']}\nA: {f['summary']}" for f in findings
        )

        user_prompt = (
            f"Topic: {context['topic']}\n\n"
            f"Findings:\n{findings_text}\n\n"
            f"Key insights: {analysis.get('key_insights')}\n"
            f"Gaps/contradictions: {analysis.get('gaps_or_contradictions')}\n"
            f"Synthesis: {analysis.get('synthesis')}"
        )

        report_body = await self.llm.complete(SYSTEM_PROMPT, user_prompt)

        # Append a deduplicated sources section built directly from data,
        # not the model, so citations are always accurate.
        seen = set()
        source_lines = []
        for f in findings:
            for s in f["sources"]:
                if s["url"] and s["url"] not in seen:
                    seen.add(s["url"])
                    source_lines.append(f"- [{s['title']}]({s['url']})")

        sources_md = "\n".join(source_lines) if source_lines else "- No sources retrieved."
        full_report = f"{report_body}\n\n## Sources\n{sources_md}"

        return {"report": full_report}
