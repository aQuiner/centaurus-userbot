from telethon import TelegramClient, events
import time

async def setup(client: TelegramClient) -> None:
    me = await client.get_me()
    owner = me.id

    @client.on(events.NewMessage(pattern=r'^\.ping$'))
    async def ping(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return

        start = time.time()
        msg = await event.edit("ping...")
        end = time.time()

        ms = round((end - start) * 1000, 2)
        await msg.edit(f"`ping {ms}ms`")