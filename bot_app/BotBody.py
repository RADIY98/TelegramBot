import os

from datetime import datetime

import requests
from fastapi import APIRouter, Request

from bot_app.application.use_cases.main_class import MainClass
from . import base_names
from infrastructure.repositories.postgresql.user_repository import PostgresClientRepository
from .interface.telegram.response import TelegramResponseResolver

router = APIRouter()
STARTED_TIME = datetime.now()
path = os.path.realpath("bot_app")


@router.post(r"/bot")
async def get_updates(request: Request):
    """Метод получения обновлений"""
    record = await request.json()

    return MainClass(
        PostgresClientRepository(),
        TelegramResponseResolver()
    ).execute(record)


@router.put("/bot")
def send_message(**kwargs):
    """
    Метод отправки сообщений
    """
    method = '/sendMessage'
    response = requests.post(base_names.URL + base_names.TOKEN + method, data=kwargs)

    return response
