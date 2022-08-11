"""
Module for validating data
"""
__author__ = "Nelidov N.N."


from pydantic import BaseModel, Field
from datetime import datetime


class MessageFrom(BaseModel):
    """
    Class of the sender
    """
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str


class MessageChat(BaseModel):
    """
    Class of the chat
    """
    id: int
    first_name: str
    username: str
    type: str


class Message(BaseModel):
    """
    Class of the message
    """
    message_id: int
    from_: MessageFrom = Field(alias="from")
    chat: MessageChat
    date: datetime
    text: str


class Response(BaseModel):
    """
    Class of the response from telegram
    """
    update_id: int
    message: Message
