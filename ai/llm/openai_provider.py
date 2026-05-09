# ai/llm/openai_provider.py
from ai.llm.base import BaseLLMProvider
import json

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, model="gpt-4o-mini"):
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        
        self.llm = ChatOpenAI(model=model, temperature=0)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an email classification engine. Output JSON only."),
            ("user",
             """
Subject: {subject}
Sender: {sender}
Body:
{body}

Return JSON:
importance_score, urgency, needs_reply, category, reason, summary
             """)
        ])

        self.chain = self.prompt | self.llm

    def classify_email(self, subject, sender, body):
        resp = self.chain.invoke({
            "subject": subject,
            "sender": sender,
            "body": body[:6000]
        })

        return json.loads(resp.content)