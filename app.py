from flask import Flask

from routes.dashboard import dashboard_bp
from routes.settings import settings_bp


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-change-me"

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(settings_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=8080, debug=True)


# from ai.robust_classifier import RobustClassifier
# from ai.llm.manager import LLMManager
# from services.scan_service import ScanService


# def main():
#     llm = LLMManager(provider_name="ollama")
#     classifier = RobustClassifier(llm)
#     scan_service = ScanService(llm=llm, classifier=classifier)
#     scan_service.run()


# if __name__ == "__main__":
#     main()