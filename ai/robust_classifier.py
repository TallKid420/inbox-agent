import json
import time
import traceback
from ai.models import EmailClassification


class RobustClassifier:
    def __init__(self, provider, max_retries=3):
        self.provider = provider
        self.max_retries = max_retries

    def _safe_parse(self, raw_text: str):
        """
        Extract JSON even if LLM wraps it in text/code fences
        """
        try:
            return json.loads(raw_text)
        except:
            # fallback extraction
            start = raw_text.find("{")
            end = raw_text.rfind("}")

            if start != -1 and end != -1:
                return json.loads(raw_text[start:end+1])

            raise ValueError("No valid JSON found")

    def classify_email(self, subject, sender, body):
        last_error = None
        last_trace = None

        for attempt in range(self.max_retries):
            try:
                raw = self.provider.classify_email(subject, sender, body)

                # Some providers return object, others string
                if isinstance(raw, dict):
                    data = raw
                else:
                    data = self._safe_parse(raw.content if hasattr(raw, "content") else raw)

                # Validate with Pydantic
                return EmailClassification(**data).model_dump()

            except Exception as e:
                last_error = str(e)
                last_trace = traceback.format_exc()
                time.sleep(0.5 * (attempt + 1))  # simple backoff

        # 🧯 FINAL FALLBACK (never crash pipeline)
        return {
            "importance_score": 0.0,
            "urgency": "low",
            "needs_reply": False,
            "category": "other",
            "summary": "Failed to classify email due to LLM error.",
            "reason": f"fallback_triggered: {str(last_error)}",

            "llm_error": last_error,
            "llm_trace": last_trace,
            "attempts": self.max_retries
        }
        