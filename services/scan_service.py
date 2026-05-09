from storage.db import Database
from ai.robust_classifier import RobustClassifier
from services.gmail_service import GmailService
from services.email_parser import EmailParser
from ai.llm.manager import LLMManager
from utils.logger import setup_logger


class ScanService:
    def __init__(self, llm, classifier):
        self.log = setup_logger("scan_service")

        self.llm = llm
        self.classifier = classifier
        self.db = Database()

        self.gmail = GmailService()

    def run(self):
        self.log.info("Starting email scan...")

        service = self.gmail.authenticate()

        emails = EmailParser().fetch_last_24h_emails(service)

        self.log.info(f"Fetched {len(emails)} emails")

        for email in emails:

            is_new = self.db.insert_email(email)

            if not is_new:
                continue
            
            try:
                result = self.classifier.classify_email(
                    subject=email.get("subject", ""),
                    sender=email.get("sender", ""),
                    body=email.get("body", "")
                )

                self.db.insert_classification(email["id"], result)

                self.log.info(f"Processed: {email.get('subject')}")

            except Exception as e:
                self.log.exception(f"Failed processing email {email.get('id')}: {e}")

        self.log.info("Scan complete")