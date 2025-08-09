# services/echo_service.py

from domain.message import Message


class EchoService:
    async def reply(self, msg: Message) -> str:
        return msg.text
