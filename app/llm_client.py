"""
LLM client abstraction.

Uses litellm so the exact same code can call OpenAI, Anthropic, Groq,
or a local Ollama model just by changing environment variables.
This keeps the project runnable by anyone reviewing it (recruiter,
interviewer) regardless of which provider they have a key for.
"""
import os
import json
import logging
from typing import Optional

import litellm

logger = logging.getLogger("llm_client")

# Which model to call. Examples:
#   "groq/llama-3.3-70b-versatile"   (free tier, great for demos)
#   "gpt-4o-mini"
#   "claude-haiku-4-5-20251001"
#   "ollama/llama3"                  (fully local, no key needed)
DEFAULT_MODEL = os.getenv("MODEL_NAME", "groq/llama-3.3-70b-versatile")


class LLMClient:
    def __init__(self, model: Optional[str] = None):
        self.model = model or DEFAULT_MODEL

    async def complete(self, system: str, user: str, json_mode: bool = False) -> str:
        """Single-turn completion. Returns raw text content."""
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        kwargs = {}
        if json_mode:
            # litellm normalizes this across providers that support it;
            # providers that don't support it silently ignore the kwarg.
            kwargs["response_format"] = {"type": "json_object"}

        try:
            response = await litellm.acompletion(
                model=self.model,
                messages=messages,
                temperature=0.4,
                max_tokens=1200,
                **kwargs,
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise RuntimeError(
                f"LLM call failed for model '{self.model}'. "
                f"Check that the matching API key env var is set. Original error: {e}"
            )

    async def complete_json(self, system: str, user: str) -> dict:
        """Completion that attempts to parse JSON, with a repair fallback."""
        raw = await self.complete(system, user, json_mode=True)
        raw = raw.strip()
        # Strip markdown code fences if the model added them anyway.
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:]
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Ask the model to fix its own output once before giving up.
            fix_prompt = f"This is not valid JSON, return ONLY valid JSON for it:\n{raw}"
            raw2 = await self.complete("You fix malformed JSON. Return only JSON.", fix_prompt)
            return json.loads(raw2.strip().strip("`"))
