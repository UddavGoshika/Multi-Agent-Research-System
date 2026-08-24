from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=300)
    model: str | None = None  # optional override, e.g. "gpt-4o-mini"
