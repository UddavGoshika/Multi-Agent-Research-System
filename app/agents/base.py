from abc import ABC, abstractmethod
from app.llm_client import LLMClient


class BaseAgent(ABC):
    """
    Every agent in the system is a thin, single-responsibility unit:
    it receives the shared `context` dict, does its one job, and
    returns a partial update to merge back into the context.

    Keeping agents this small is deliberate: it makes the orchestrator
    easy to reason about, easy to test (mock the LLM, assert on output
    shape), and easy to extend with a new agent without touching the
    others — the kind of design a reviewer can read in two minutes.
    """

    name: str = "agent"
    role: str = ""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    @abstractmethod
    async def run(self, context: dict) -> dict:
        ...
