import base64
import re

class EmailParser:
    @staticmethod
    def get_message_ids(service, query="newer_than:1d"):
        results = service.users().messages().list(
            userId="me",
            q=query
        ).execute()

        return results.get("messages", [])
    
    @staticmethod
    def get_email(service, msg_id):
        msg = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

        return msg
    
    @staticmethod
    def parse_email(msg):
        headers = msg["payload"]["headers"]

        def get_header(name):
            return next((h["value"] for h in headers if h["name"] == name), None)

        subject = get_header("Subject")
        sender = get_header("From")
        date = get_header("Date")

        body_raw = EmailCleaner.extract_body(msg["payload"])
        body_clean = EmailCleaner.clean_body(body_raw)

        snippet = msg.get("snippet", "")

        return {
            "id": msg["id"],
            "thread_id": msg["threadId"],
            "subject": subject,
            "sender": sender,
            "date": date,
            "snippet": snippet,
            "body": body_clean,
            "raw_body": body_raw
        }
    
    def fetch_last_24h_emails(self, service):
        messages = self.get_message_ids(service)

        emails = []

        for m in messages:
            full = self.get_email(service, m["id"])
            parsed = self.parse_email(full)
            emails.append(parsed)

        return emails
    
class EmailCleaner:
    @staticmethod
    def extract_body(payload):
        return EmailCleaner.find_text(payload) or ""
    
    @staticmethod
    def find_text(part):
        if "parts" in part:
            for p in part["parts"]:
                result = EmailCleaner.find_text(p)
                if result:
                    return result

        if part.get("mimeType") == "text/plain":
            data = part["body"].get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

        return None
    
    @staticmethod
    def clean_body(text):
        if not text:
            return ""

        # remove reply chains
        text = re.split(r"On .* wrote:", text)[0]

        # remove forwarded headers
        text = re.split(r"-----Original Message-----", text)[0]

        # remove excessive whitespace
        text = re.sub(r"\n\s*\n", "\n\n", text)

        # strip signatures (basic heuristic)
        text = re.split(r"--\s", text)[0]

        return text.strip()