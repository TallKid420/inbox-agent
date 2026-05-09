import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Ollama
    OLLAMA_ENDPOINT = os.getenv("Ollama_Endpoint", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("Ollama_Model", "llama3")