from utils.logger import setup_logger

log = setup_logger("app")

log.info("Starting Email Agent System...")

from services.scan_service import ScanService
from services.scheduler import ScanScheduler
from ai.llm.manager import LLMManager
from ai.robust_classifier import RobustClassifier
import time



def main():
    log.info("Initializing LLM...")
    llm = LLMManager(provider_name="ollama")
    classifier = RobustClassifier(llm)

    scan_service = ScanService(llm=llm, classifier=classifier)
    
    scheduler = ScanScheduler(scan_service)
    scheduler.start()

    log.info("Inbox Agent scheduler running. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        log.info("Scheduler stopped.")


if __name__ == "__main__":
    main()