from rich.logging import RichHandler
import logging


def setup_logger(name: str = "email_agent"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    return logging.getLogger(name)