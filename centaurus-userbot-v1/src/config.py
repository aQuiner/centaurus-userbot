from __future__ import annotations
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
COGS_DIR = BASE_DIR / "cogs"
SESSION_DIR = BASE_DIR / "session"
SESSION_DIR.mkdir(exist_ok=True)
CONFIG_PATH = ROOT_DIR / "cfg.json"

with CONFIG_PATH.open("r", encoding="utf-8") as handle:
    data = json.load(handle)

API_ID = data["api_id"]
API_HASH = data["api_hash"]
SESSION_NAME = data["session_name"]
