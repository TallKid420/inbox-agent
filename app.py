print("Importing Packages")

from services.gmail_service import GmailService
from services.email_parser import EmailParser
from ai.llm.manager import LLMManager

print("Packages Imported")

def main():
    # 1. Authenticate Gmail
    gmail = GmailService()
    service = gmail.authenticate()

    print("Connected to Gmail API successfully.")

    # 2. Fetch emails
    parser = EmailParser()
    emails = parser.fetch_last_24h_emails(service)

    print(f"\nFetched {len(emails)} emails\n")

    # 3. Load LLM (swap provider here)
    llm = LLMManager(
        provider_name="ollama",
    )

    # 4. Process each email
    for i, email in enumerate(emails, start=1):
        try:
            result = llm.classify_email(
                subject=email.get("subject", ""),
                sender=email.get("sender", ""),
                body=email.get("body", "")
            )

            print(f"\n================== EMAIL {i}/{len(emails)} ==================")
            print(f"Subject: {email.get('subject')}")
            print(f"Sender: {email.get('sender')}")
            print(f"Urgency: {result.get('urgency')}")
            print(f"Score: {result.get('importance_score')}")
            print(f"Needs Reply: {result.get('needs_reply')}")
            print(f"Category: {result.get('category')}")
            print(f"Summary: {result.get('summary')}")

        except Exception as e:
            print(f"\n================== EMAIL {i}/{len(emails)} ==================")
            print(f"Subject: {email.get('subject')}")
            print("ERROR processing email:", str(e))


if __name__ == "__main__":
    main()