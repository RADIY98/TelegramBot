import asyncio
import json
import os

from datetime import datetime
from typing import Optional, List, Dict

import requests
from fastapi import APIRouter
from bot_app.KeyBoard import KeyBoard
from bot_app.trains.utils import parse_file
from . import base_names
from bot_app.database import sql_query, sql_query_scalar
from .schemas.Response import Msg
from .trains import get_all_trains_for_keyboard, get_all_exercises_for_keyboard

router = APIRouter()
STARTED_TIME = datetime.now()
path = os.path.realpath("bot_app")


# TODO ПРИ ПОДКЛЮЧЕНИЕ К БОТУ СДЕЛАТЬ ПРОКИДЫВАНИЕ КНОПОК

@router.get('/')
async def loong_pool_request():
    while True:
        await asyncio.sleep(3)
        get_updates()


@router.get(r"/bot")
def get_updates():
    """
    Метод получения обновлений
    """
    response_list = _get_http_request()
    import pydevd_pycharm
    pydevd_pycharm.settrace('localhost', port=2010, stdoutToServer=True, stderrToServer=True)
    if response_list:
        client_data = _get_clients_update_id(
            [
                record.get("message").get("chat").get("id") for record in response_list
            ]
        )

        for record in response_list:
            msg: Msg = Msg(record.get("message"))
            client_id = msg.chat.id
            update_id = record.get("update_id")
            print(update_id)

            if not client_data.get(client_id):
                _insert_client(msg, update_id)

            elif update_id <= client_data.get(client_id):
                continue

            trains = get_all_trains_for_keyboard(client_id)

            if msg.text == "/start":
                send_message(
                    chat_id=client_id,
                    text=msg.text,
                    reply_markup=json.dumps(
                        {'keyboard': KeyBoard(base_names.StartButtons.buttons_array).get_keyboard()})
                )
                _insert_client(msg, update_id)
            elif msg.text == base_names.StartButtons.trains:
                print()
                send_message(
                    chat_id=client_id,
                    text=msg.text,
                    reply_markup=json.dumps(
                        {
                            'keyboard': KeyBoard(get_all_trains_for_keyboard(client_id)).get_keyboard()
                        }
                    )
                )
            elif msg.text in trains[:-1]:
                send_message(
                    chat_id=client_id,
                    text=get_all_exercises_for_keyboard(client_id, msg.text),
                    reply_markup=json.dumps(
                        {
                            'keyboard': KeyBoard(get_all_trains_for_keyboard(client_id)).get_keyboard()
                        }
                    )
                )
            elif msg.text == base_names.StartButtons.statistic:
                pass
            elif msg.text == base_names.MAIN_MENU:
                send_message(
                    chat_id=client_id,
                    text=msg.text,
                    reply_markup=json.dumps(
                        {'keyboard': KeyBoard(base_names.StartButtons.buttons_array).get_keyboard()})
                )
            elif msg.document is not None:
                file = __download_file(msg.document)
                train_obj = parse_file(file)
                sql_query("""
                    DELETE FROM
                        "Train"
                    WHERE
                        "ClientID"=%s::bigint
                    """, [client_id]
                )
                for train_name, train in train_obj.items():
                    sql_query(
                        """
                        INSERT INTO
                            "Train"
                            (
                            "Name",
                            "ClientID",
                            "Settings"
                            )
                        VALUES 
                        (
                            %s::text,
                            %s::bigint,
                            %s::json
                        )
                        """, (train_name, client_id, json.dumps(train))
                    )

            res = sql_query(
                """
                UPDATE
                    "Client"
                SET
                    "UpdateId"=%s::bigint
                WHERE
                    "id"=%s::bigint
                RETURNING
                    "id",
                    "UpdateId"
                
                """, (update_id, client_id)
            )
            print(res)
            send_message(chat_id=client_id, text=f"{client_id}, {update_id}")

    return response_list


def _get_http_request() -> dict:
    """
    Получим данные от ТГ
    """
    method = '/getUpdates'
    params = {'limit': 100, "offset": base_names.global_id + 10}
    resp = requests.get(
        base_names.URL + base_names.TOKEN + method,
        params
    )
    result_list = resp.json()['result']

    return result_list


def _call_tg_method(method: str, params: dict) -> dict:
    """
    Получим данные от ТГ
    """
    resp = requests.get(
        f"{base_names.URL}{base_names.TOKEN}{method}",
        params
    )
    print(resp.json())
    result_list = resp.json()

    return result_list


def _get_clients_update_id(clients: List[int]) -> Dict[int, int]:
    """
    Получим данные клиентов из БД
    """
    clients_last_update: Optional[dict] = sql_query_scalar(
        """
                        SELECT
                            jsonb_build_object(
                                "id"::bigint, "UpdateId"::bigint
                            ) AS Result
                        FROM
                            "Client"
                        WHERE
                            "id" = ANY(%(clients)s::bigint[])
                """, {'clients': clients}
    )
    if clients_last_update:
        clients_last_update = {int(key): value for key, value in clients_last_update.items()}
    else:
        clients_last_update = {}

    return clients_last_update


def _insert_client(msg: Msg, update_id: int):
    """
    Добавляем клиента в БД
    """
    sql_query(
        f"""
                    INSERT INTO
                        "Client"
                    VALUES 
                        (
                            %s::bigint,
                            %s::text,
                            %s::text,
                            %s::bigint
                        )
                    """,
        (msg.chat.id, msg.chat.first_name, msg.chat.username, update_id)
    )


def __download_file(document) -> requests.Response:
    """
    Скачивает файл
    """
    file_info = _call_tg_method("/getFile", {"file_id": document.file_id})
    resp: requests.Response = requests.get(
        f"https://api.telegram.org/file/bot{base_names.TOKEN}/{file_info.get('result').get('file_path')}"
    )
    resp.encoding = "utf-8"
    return resp


@router.put("/bot")
def send_message(**kwargs):
    """
    Метод отправки сообщений
    """
    method = '/sendMessage'
    response = requests.post(base_names.URL + base_names.TOKEN + method, data=kwargs)

    return response
