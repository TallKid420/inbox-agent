from ai.robust_classifier import RobustClassifier
from ai.llm.manager import LLMManager
from services.scan_service import ScanService


def main():
    llm = LLMManager(provider_name="ollama")
    classifier = RobustClassifier(llm)
    scan_service = ScanService(llm=llm, classifier=classifier)
    scan_service.run()


if __name__ == "__main__":
    main()