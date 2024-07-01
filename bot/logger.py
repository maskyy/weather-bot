import logging

from .config import CONFIG


logger = logging.getLogger("bot")


def setup_logger():
    logger.setLevel(getattr(logging, CONFIG["LOG_LEVEL"]))
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
