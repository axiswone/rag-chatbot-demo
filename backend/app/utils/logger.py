import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

log_dir = REPO_ROOT / "logs"

log_dir.mkdir(parents=True, exist_ok=True)


def setup_logger(name: str = "chat_logger") -> logging.Logger:

    logger = logging.getLogger(name)

    if not logger.handlers:

        handler = RotatingFileHandler(
            log_dir / "chat.log",
            maxBytes=10_000_000,
            backupCount=3
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        logger.setLevel(logging.INFO)

    return logger