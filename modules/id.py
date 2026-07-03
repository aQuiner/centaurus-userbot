from telethon import TelegramClient, events

async def setup(client: TelegramClient) -> None:
    me = await client.get_me()
    owner = me.id

    @client.on(events.NewMessage(pattern=r'^\.id$'))
    async def id(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return

        if event.is_reply:
            msg = await event.get_reply_message()
            await event.edit(str(msg.sender_id))
        else:
            await event.edit(str(event.sender_id))