from telethon import TelegramClient, events
from io import BytesIO
import asyncio
import random
import string

async def setup(client: TelegramClient) -> None:
    me = await client.get_me()
    owner = me.id

    def rnd():
        return "".join(random.choice(string.ascii_lowercase) for _ in range(10))

    @client.on(events.NewMessage(pattern=r'^\.grab$'))
    async def grab(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return

        if not event.is_reply:
            await event.delete()
            return

        msg = await event.get_reply_message()

        if not msg.media:
            await event.delete()
            return

        try:
            buffer = BytesIO()
            await client.download_media(msg, file=buffer)
            buffer.seek(0)

            name = rnd()

            if msg.photo:
                buffer.name = f"{name}.jpg"
            elif msg.video:
                buffer.name = f"{name}.mp4"
            elif msg.document:
                ext = msg.file.ext or ""
                buffer.name = f"{name}{ext}"
            else:
                buffer.name = name

            await client.send_file(
                "me",
                buffer
            )

            await event.delete()

        except:
            await event.delete()
            await asyncio.sleep(1)
            await event.delete()