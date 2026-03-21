
import datetime


class Chat:
    def __init__(self, chat: dict):
        self.id: int = chat.get("id")
        self.first_name: str = chat.get("first_name")
        self.username: str = chat.get("username")
        self.type: str = chat.get("type")


class Sender:
    def __init__(self, sender: dict):
        self.id: int = sender.get("id")
        self.is_bot: bool = sender.get("is_bot")
        self.first_name: str = sender.get("first_name")
        self.username: str = sender.get("username")
        self.language_code: str = sender.get("language_code")
        self.is_premium: bool = sender.get("is_premium")


class Document:
    def __init__(self, document: dict):
        self.file_id: int = document.get("file_id")
        self.file_path: int = document.get("file_path")


class Msg:
    def __init__(self, msg: dict):
        self.message_id: int = msg.get("message_id")
        self.date: datetime = msg.get("date")
        self.text: str = msg.get("text")
        self.from_: Sender = Sender(msg.get("from"))
        self.chat: Chat = Chat(msg.get("chat"))
        self.document: Document | None = Document(msg.get("document")) if msg.get("document") else None
