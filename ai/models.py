from pydantic import BaseModel
from typing import Literal, Optional


class EmailClassification(BaseModel):
    importance_score: float
    urgency: Literal["low", "medium", "high"]
    needs_reply: bool
    category: str
    summary: str
    reason: Optional[str] = "not provided"