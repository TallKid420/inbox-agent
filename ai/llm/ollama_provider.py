from ai.llm.base import BaseLLMProvider
from config.settings import Settings
import json


class OllamaProvider(BaseLLMProvider):
    def __init__(self, model=None, base_url=None):
        from langchain_ollama import ChatOllama

        self.llm = ChatOllama(
            model=model or Settings.OLLAMA_MODEL,
            base_url=base_url or Settings.OLLAMA_ENDPOINT,
            temperature=0
        )

    def classify_email(self, subject, sender, body):
        prompt = f"""
Return ONLY valid JSON.

Subject: {subject}
Sender: {sender}
Body:
{body[:6000]}

You MUST include ALL fields:
- importance_score (float 0-1)
- urgency (low, medium, high)
- needs_reply (true/false)
- category (promo, security, billing, personal, work, other)
- summary (string)
- reason (string explaining classification)

Do NOT omit any field.
Do NOT wrap in markdown.
"""

        resp = self.llm.invoke(prompt)

        return json.loads(resp.content)