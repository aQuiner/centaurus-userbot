from telethon import TelegramClient, events
from deep_translator import GoogleTranslator

async def setup(client: TelegramClient) -> None:
    me = await client.get_me()
    owner = me.id

    @client.on(events.NewMessage(pattern=r'^\.translate$'))
    async def translate(event: events.NewMessage.Event) -> None:
        if event.sender_id != owner:
            return

        if not event.is_reply:
            await event.delete()
            return

        msg = await event.get_reply_message()

        if not msg.text:
            await event.delete()
            return

        text = msg.text

        letters = [c.lower() for c in text if c.isalpha()]

        if not letters:
            await event.delete()
            return

        ru = sum("а" <= c <= "я" or c == "ё" for c in letters)
        en = sum("a" <= c <= "z" for c in letters)

        if ru >= len(letters) * 0.7:
            target = "en"
        elif en >= len(letters) * 0.7:
            target = "ru"
        else:
            await event.delete()
            return

        result = GoogleTranslator(source="auto", target=target).translate(text)

        await event.reply(f"> {result}")
        await event.delete()