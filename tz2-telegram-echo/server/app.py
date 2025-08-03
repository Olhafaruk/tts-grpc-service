#server/app.py

import asyncio
import random

from telethon import events
from telethon.tl.functions.messages import SendMessageRequest

from repository.tg_client import client

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    text = event.raw_text
    print("Получили:", text, flush=True)


    peer = await event.get_input_chat()


    random_id = random.getrandbits(64)


    await client(
        SendMessageRequest(
            peer,
            text,
            random_id
        )
    )
    print("Отправили:", text, flush=True)

async def main():
    await client.start()
    print("Bot-клиент запущен", flush=True)
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
