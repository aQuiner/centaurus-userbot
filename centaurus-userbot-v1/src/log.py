from __future__ import annotations
import logging
from colorama import init as colorama_init


class _Ansi:
    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"
    GRAY = "\x1b[90m"
    WHITE = "\x1b[97m"
    RED = "\x1b[91m"
    PURPLE = "\x1b[95m"
    ITALIC = "\x1b[3m"


def _format(text: str, color: str) -> str:
    return f"{_Ansi.BOLD}{color}{text}{_Ansi.RESET}"


def italic(text: str) -> str:
    return f"{_Ansi.ITALIC}{text}{_Ansi.RESET}"


def setup_logger() -> logging.Logger:
    colorama_init()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger = logging.getLogger("znode")
    logger.handlers = []
    logger.propagate = False
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def gray(text: str) -> str:
    return _format(text, _Ansi.GRAY)


def white(text: str) -> str:
    return _format(text, _Ansi.WHITE)


def error(text: str) -> str:
    return _format(text, _Ansi.RED)


def highlight(text: str) -> str:
    return _format(text, _Ansi.PURPLE)
