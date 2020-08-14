import requests
import base_names
from time import sleep


class BotHandler:
    """

    """
    def __init__(self):
        """

        """
        self.token = base_names.TOKEN
        self.url = base_names.URL


    def get_updates(self, offset=None, timeout=30):
        """

        :return:
        """
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.url + method, params)
        result_json = resp.json()['result']
        return result_json


    def last_update(self, data):
        """
        Получение данных о последнем обновление
        :return:
        """
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


    def send_message(chat, text):
        """
        Метод отправки сообщений
        :return:
        """
        params = {"chat_id": chat, "text": text}
        method = 'sendMessage'
        resp = requests.post(base_names.URL + method, data=params)
        return resp