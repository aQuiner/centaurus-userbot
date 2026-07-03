from __future__ import annotations
import importlib
from pathlib import Path
from telethon import TelegramClient
from .config import COGS_DIR


def _module_name(path: Path) -> str:
    relative = path.relative_to(COGS_DIR).with_suffix("")
    return "src.cogs." + ".".join(relative.parts)


async def load_cogs(client: TelegramClient) -> list[str]:
    paths = sorted(COGS_DIR.rglob("*.py"))
    loaded: list[str] = []
    for path in paths:
        if path.name.startswith("_") or path.name == "__init__.py":
            continue
        module = importlib.import_module(_module_name(path))
        await module.setup(client)
        loaded.append(path.stem)
    return loaded
