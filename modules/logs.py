from telethon import TelegramClient, events
import json
import os
import asyncio

FILE = "status.json"

def load():
    if not os.path.exists(FILE):
        return {"logs": False}
    with open(FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

async def setup(client: TelegramClient) -> None:
    me = await client.get_me()
    owner = me.id

    state = load()

    async def check_channel():
        try:
            await client.get_entity("znode-logs")
            return True
        except:
            return False

    @client.on(events.NewMessage(pattern=r'^\.logs$'))
    async def logs(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return

        if not event.is_private:
            await event.delete()
            return

        exists = await check_channel()

        if not exists:
            msg = await event.edit("no such channel it must be created")
            await asyncio.sleep(3)
            await msg.delete()
            return

        state["logs"] = True
        save(state)

        await event.delete()

    @client.on(events.NewMessage(pattern=r'^\.nologs$'))
    async def nologs(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return

        if not event.is_private:
            await event.delete()
            return

        state["logs"] = False
        save(state)

        msg = await event.edit("logs disabled")
        await asyncio.sleep(1)
        await msg.delete()

    @client.on(events.NewMessage)
    async def logger(event: events.NewMessage.Event) -> None:
        if not state.get("logs"):
            return

        if event.sender_id == owner:
            return

        if not event.is_private:
            return

        try:
            user = await client.get_entity(event.sender_id)

            name = user.first_name or "none"
            uid = event.sender_id
            text = event.raw_text or "[media]"

            msg = f'<a href="tg://user?id={uid}">{name}</a>\n<b>{text}</b>'

            await client.send_message(
                "znode-logs",
                msg,
                parse_mode="html"
            )

        except:
            pass