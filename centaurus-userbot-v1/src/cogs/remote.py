from __future__ import annotations
import ast
import importlib
import types
import importlib.util
import io
import json
import sys
import subprocess
import urllib.request
import tokenize
from pathlib import Path
from typing import Set, List
from telethon import TelegramClient, events

from ..config import COGS_DIR

INDEX_PATH = COGS_DIR / ".remote_index.json"
INDEX_PATH.parent.mkdir(exist_ok=True)


def _ensure_index() -> dict:
    if not INDEX_PATH.exists():
        INDEX_PATH.write_text(json.dumps({}))
    return json.loads(INDEX_PATH.read_text())


def _save_index(data: dict) -> None:
    INDEX_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def _to_raw(url: str) -> str:
    if "raw.githubusercontent.com" in url:
        return url
    if "github.com" in url:
        url = url.replace("github.com/", "raw.githubusercontent.com/")
        url = url.replace("/blob/", "/")
        return url
    return url


def _download(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "python-urllib/3"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8")


def _parse_imports(source: str) -> Set[str]:
    try:
        tree = ast.parse(source)
    except Exception:
        return set()
    names: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                names.add(n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.add(node.module.split(".")[0])
    return names


def _extract_requirements(source: str) -> List[str]:
    for line in source.splitlines():
        line = line.strip()
        if line.lower().startswith("# require:"):
            reqs = line.split(":", 1)[1]
            return [r.strip() for r in reqs.split(",") if r.strip()]
    return []


def _strip_comments(source: str) -> str:
    try:
        # try to unparse AST (removes comments)
        tree = ast.parse(source)
        try:
            return ast.unparse(tree)
        except Exception:
            pass
    except Exception:
        pass
    # fallback: use tokenize to remove comments
    out = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for toknum, tokval, _, _, _ in tokens:
            if toknum == tokenize.COMMENT:
                continue
            out.append(tokval)
        return "".join(out)
    except Exception:
        return source


def _pip_install(pkgs: List[str]) -> None:
    if not pkgs:
        return
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *pkgs])
    except Exception:
        pass


async def setup(client: TelegramClient) -> None:
    me = await client.get_me()
    owner = me.id

    @client.on(events.NewMessage(pattern=r'^\.load\s+(.+)$'))
    async def load(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return
        url = event.pattern_match.group(1).strip()
        msg = await event.edit("downloading...")
        try:
            raw = _to_raw(url)
            source = _download(raw)
        except Exception as exc:
            await msg.edit(f"{exc}")
            return

        reqs = _extract_requirements(source)
        if reqs:
            _pip_install(reqs)

        imports = _parse_imports(source)
        base_dir_url = "/".join(raw.split("/")[:-1])
        saved_files = []

        filename = Path(raw).name
        # remove comments before saving
        clean_source = _strip_comments(source)
        target = COGS_DIR / filename
        target.write_text(clean_source, encoding="utf-8")
        saved_files.append(filename)

        for name in imports:
            if name in ("telethon",):
                continue
            try:
                importlib.import_module(name)
            except Exception:
                candidate_url = f"{base_dir_url}/{name}.py"
                try:
                    cand_src = _download(candidate_url)
                    cand_clean = _strip_comments(cand_src)
                    cand_target = COGS_DIR / f"{name}.py"
                    cand_target.write_text(cand_clean, encoding="utf-8")
                    saved_files.append(cand_target.name)
                except Exception:
                    pass

        index = _ensure_index()
        stem = Path(filename).stem
        index[stem] = {"filename": filename, "source": raw}
        _save_index(index)

        module_name = f"src.cogs.{stem}"
        saved_list = ', '.join(saved_files)
        try:
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)
            if hasattr(module, "setup"):
                await module.setup(client)
            await msg.edit(f"loaded {saved_list}")
        except Exception as exc:
            # attempt to execute the source as fallback and call setup
            try:
                module = types.ModuleType(module_name)
                exec(clean_source, module.__dict__)
                sys.modules[module_name] = module
                if hasattr(module, "setup"):
                    await module.setup(client)
                await msg.edit(f"loaded (fallback) {saved_list}")
            except Exception as exc2:
                await msg.edit(f"module error {exc}; fallback error {exc2}")

    @client.on(events.NewMessage(pattern=r'^\.list$'))
    async def lst(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return
        index = _ensure_index()
        if not index:
            await event.edit("no loaded modules")
            return
        lines = []
        for key, val in index.items():
            lines.append(f"{key} -> {val.get('source','')}")
        await event.edit("\n".join(lines))

    @client.on(events.NewMessage(pattern=r'^\.unload\s+(.+)$'))
    async def unload(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return
        name = event.pattern_match.group(1).strip()
        msg = await event.edit("removing...")
        index = _ensure_index()
        removed = False
        if name in index:
            filename = index[name]["filename"]
            path = COGS_DIR / filename
            try:
                if path.exists():
                    path.unlink()
                mod = f"src.cogs.{name}"
                if mod in sys.modules:
                    del sys.modules[mod]
                del index[name]
                _save_index(index)
                removed = True
            except Exception as exc:
                await msg.edit(f"remove error {exc}")
                return
        else:
            path = COGS_DIR / f"{name}.py"
            if path.exists():
                try:
                    path.unlink()
                    mod = f"src.cogs.{Path(path).stem}"
                    if mod in sys.modules:
                        del sys.modules[mod]
                    for k, v in list(index.items()):
                        if v.get("filename") == path.name:
                            del index[k]
                    _save_index(index)
                    removed = True
                except Exception as exc:
                    await msg.edit(f"remove error {exc}")
                    return

        if removed:
            await msg.edit("module removed")
        else:
            await msg.edit("module not found")
