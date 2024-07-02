import logging

from .config import CONFIG


log = logging.getLogger("bot")


def setup_logger():
    log.setLevel(getattr(logging, CONFIG["LOG_LEVEL"]))
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
