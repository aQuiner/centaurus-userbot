from telethon import TelegramClient
from .config import API_HASH, API_ID, SESSION_DIR, SESSION_NAME
from .loader import load_cogs
from .log import error, gray, highlight, setup_logger

logger = setup_logger()


def create_client() -> TelegramClient:
    session_path = SESSION_DIR / SESSION_NAME
    return TelegramClient(session_path, API_ID, API_HASH)


async def run() -> None:
    client = create_client()
    try:
        await client.start(
            phone=lambda: input("Phone: "),
            code_callback=lambda: input("Code: "),
            password=lambda: input("Password: "),
        )
        cogs = await load_cogs(client)
        logger.info(gray(f"Loaded {len(cogs)} cogs"))
        logger.info(highlight(", ".join(cogs) if cogs else ""))
        await client.run_until_disconnected()
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        logger.error(error(str(exc)))
    finally:
        await client.disconnect()
