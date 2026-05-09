from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
import threading

from utils.logger import setup_logger


class ScanScheduler:
    def __init__(self, scan_service):
        self.scan_service = scan_service
        self.scheduler = BackgroundScheduler()
        self.lock = threading.Lock()

        self.log = setup_logger("scheduler")

    def _run_safe_scan(self):
        if self.lock.locked():
            self.log.warning("Scan already running — skipping duplicate trigger")
            return

        with self.lock:
            try:
                self.log.info("Starting scheduled email scan...")
                self.scan_service.run()
                self.log.info("Email scan completed successfully")

            except Exception as e:
                self.log.exception(f"Scheduled scan failed: {e}")

    # ----------------------------
    # SCHEDULE SETUP
    # ----------------------------
    def start(self):
        self.scheduler.add_job(
            self._run_safe_scan,
            CronTrigger(hour=8, minute=0),
            id="daily_email_scan",
            replace_existing=True
        )

        self.scheduler.start()
        atexit.register(lambda: self.scheduler.shutdown())

        self.log.info("Scheduler started — running daily at 8:00 AM")

    # ----------------------------
    # MANUAL TRIGGER
    # ----------------------------
    def run_now(self):
        self.log.info("Manual scan triggered")
        threading.Thread(target=self._run_safe_scan).start()