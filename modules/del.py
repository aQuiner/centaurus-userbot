from telethon import TelegramClient, events
import asyncio

async def setup(client: TelegramClient) -> None:
    me = await client.get_me()
    owner = me.id

    @client.on(events.NewMessage(pattern=r'^\.del$'))
    async def delete(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return

        target = await event.get_reply_message()

        try:
            if target:
                await client.delete_messages(event.chat_id, target.id)
            else:
                await client.delete_messages(event.chat_id, event.id)

            await client.delete_messages(event.chat_id, event.id)

        except:
            await event.edit("не вышло удалить сообщение")
            await asyncio.sleep(2)
            await event.delete()