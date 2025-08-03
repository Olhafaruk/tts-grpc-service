#repository/tg_client.py
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID      = int(os.getenv("API_ID"))
API_HASH    = os.getenv("API_HASH")
SESSION_STR = os.getenv("SESSION_STRING")


client = TelegramClient(
    StringSession(SESSION_STR),
    API_ID,
    API_HASH
)
