from telethon import TelegramClient, events

async def setup(client: TelegramClient) -> None:
    me = await client.get_me()
    owner = me.id

    @client.on(events.NewMessage(pattern=r'^\.save$'))
    async def save(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return

        if not event.is_reply:
            await event.delete()
            return

        msg = await event.get_reply_message()
        await client.forward_messages("me", msg)
        await event.delete()