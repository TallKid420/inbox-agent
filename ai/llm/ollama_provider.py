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
Return ONLY JSON.

Subject: {subject}
Sender: {sender}
Body:
{body[:6000]}

Fields:
importance_score, urgency, needs_reply, category, summary
"""

        resp = self.llm.invoke(prompt)

        return json.loads(resp.content)