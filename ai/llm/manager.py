from ai.llm.openai_provider import OpenAIProvider
from ai.llm.ollama_provider import OllamaProvider
from config.settings import Settings


class LLMManager:
    def __init__(self, provider_name="ollama", model=None, base_url=None):

        self.provider_name = provider_name

        if provider_name == "ollama":
            self.provider = OllamaProvider(
                model=model or Settings.OLLAMA_MODEL,
                base_url=base_url or Settings.OLLAMA_ENDPOINT
            )

        elif provider_name == "openai":
            self.provider = OpenAIProvider(model=model)

        else:
            raise ValueError(f"Unknown provider: {provider_name}")

    def classify_email(self, subject, sender, body):
        return self.provider.classify_email(subject, sender, body)