# server/app.py

import asyncio

from repository.tg_client import client
from telethon import events


@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    text = event.raw_text
    print("Получили:", text, flush=True)

    await event.reply(text)
    print(f"Отправили (reply to {event.message.id}):", text, flush=True)


async def main():
    await client.start()
    print("Bot-клиент запущен", flush=True)
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
