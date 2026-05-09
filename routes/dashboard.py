import threading

from flask import Blueprint, redirect, render_template, url_for, flash

from ai.llm.manager import LLMManager
from ai.robust_classifier import RobustClassifier
from services.scan_service import ScanService
from storage.db import Database


dashboard_bp = Blueprint("dashboard", __name__)


def build_scan_service():
    llm = LLMManager(provider_name="ollama")
    classifier = RobustClassifier(llm)
    return ScanService(llm=llm, classifier=classifier)


@dashboard_bp.route("/")
def dashboard():
    db = Database()

    stats = {
        "total_emails": db.count_emails() if hasattr(db, "count_emails") else 0,
        "total_classifications": db.count_classifications() if hasattr(db, "count_classifications") else 0,
        "high_priority": db.count_high_priority() if hasattr(db, "count_high_priority") else 0,
        "needs_reply": db.count_needs_reply() if hasattr(db, "count_needs_reply") else 0,
    }

    recent = db.get_recent_classifications(limit=50) if hasattr(db, "get_recent_classifications") else []

    return render_template(
        "dashboard.html",
        stats=stats,
        recent=recent,
    )


@dashboard_bp.route("/scan/run", methods=["POST"])
def run_scan():
    def background_scan():
        scan_service = build_scan_service()
        scan_service.run()

    threading.Thread(target=background_scan, daemon=True).start()

    flash("Scan started in the background.")
    return redirect(url_for("dashboard.dashboard"))