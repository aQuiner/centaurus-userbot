from telethon import TelegramClient, events
import random

async def setup(client: TelegramClient) -> None:
    me = await client.get_me()
    owner = me.id

    def clown(text: str) -> str:
        out = []
        for c in text:
            if c.isalpha():
                out.append(c.upper() if random.random() > 0.5 else c.lower())
            else:
                out.append(c)
        return "".join(out) + " 🤡"

    @client.on(events.NewMessage(pattern=r'^\.clown$'))
    async def clown_cmd(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return

        if not event.is_reply:
            await event.delete()
            return

        msg = await event.get_reply_message()

        if not msg.text:
            await event.delete()
            return

        result = clown(msg.text)

        try:
            await event.edit(result)
        except:
            await event.delete()