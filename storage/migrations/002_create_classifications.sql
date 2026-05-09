CREATE TABLE IF NOT EXISTS classifications (
    email_id TEXT PRIMARY KEY,
    importance_score REAL,
    urgency TEXT,
    needs_reply INTEGER,
    category TEXT,
    summary TEXT,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(email_id) REFERENCES emails(id)
);