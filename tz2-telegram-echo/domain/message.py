# domain/message.py


class Message:
    def __init__(self, text: str, chat_id: int):
        self.text = text
        self.chat_id = chat_id
