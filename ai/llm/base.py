from abc import ABC, abstractmethod
from typing import Dict


class BaseLLMProvider(ABC):
    """
    Abstract interface for all LLM providers.
    Ensures consistent output format across OpenAI, Ollama, Anthropic, etc.
    """

    @abstractmethod
    def classify_email(self, subject: str, sender: str, body: str) -> Dict:
        """
        Returns a structured email classification.

        Expected schema:
        {
            "importance_score": float,
            "urgency": str,          # low | medium | high
            "needs_reply": bool,
            "category": str,         # promo | security | billing | work | personal | other
            "summary": str,
            "reason": str
        }
        """
        pass