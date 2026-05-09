import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path: str = "storage/emails.db"):

        Path("storage").mkdir(exist_ok=True)

        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

        self.run_migrations()

    def run_migrations(self):
        migration_dir = Path("storage/migrations")

        if not migration_dir.exists():
            return

        cursor = self.conn.cursor()

        for file in sorted(migration_dir.glob("*.sql")):
            with open(file, "r", encoding="utf-8") as f:
                sql = f.read()
                cursor.executescript(sql)

        self.conn.commit()

    def insert_email(self, email: dict) -> bool:
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO emails (
                    id, thread_id, subject, sender, body, snippet, date
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                email["id"],
                email.get("thread_id"),
                email.get("subject"),
                email.get("sender"),
                email.get("body"),
                email.get("snippet"),
                email.get("date"),
            ))

            self.conn.commit()
            return True

        except sqlite3.IntegrityError:
            # already exists (duplicate email)
            return False
        
    def insert_classification(self, email_id: str, result: dict):
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO classifications (
                email_id,
                importance_score,
                urgency,
                needs_reply,
                category,
                summary,
                reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            email_id,
            result.get("importance_score"),
            result.get("urgency"),
            int(result.get("needs_reply", False)),
            result.get("category"),
            result.get("summary"),
            result.get("reason"),
        ))

        self.conn.commit()