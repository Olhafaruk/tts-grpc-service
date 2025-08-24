import asyncio
import os

from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")
TWO_FA = os.getenv("TWO_FA_PASSWORD")  # если есть 2FA, иначе пустая строка


async def main():
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.start(phone=PHONE, password=TWO_FA)
    print("=== YOUR SESSION STRING ===")
    print(client.session.save())
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
