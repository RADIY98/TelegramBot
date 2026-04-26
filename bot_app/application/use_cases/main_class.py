from bot_app import base_names
from bot_app.KeyBoard import KeyBoard
from bot_app.application.dto.pressed_buttons import PressedButton
from bot_app.application.use_cases.handle_button import HandleButton
from bot_app.domain.entities.user_entity import UserEntity
from bot_app.domain.repositories.user_repositoriy import IUserRepository
from bot_app.domain.response_resolver import IResponseResolver
from bot_app.interface.telegram.mappers import request_to_button
from bot_app.interface.telegram.request_model import Msg


class MainClass:
    def __init__(self, client_rep: IUserRepository, response_res: IResponseResolver):
        self.client_rep = client_rep
        self.response_res = response_res

    def execute(self, record):
        """Main scinarior"""
        if not record:
            return self.response_res.send_short_response()

        message = record.get("message")
        user_id = message.get("chat").get("id")

        msg: Msg = Msg(message)

        new_update_id: int = record.get("update_id")

        pushed_button: PressedButton = request_to_button(record)

        if pushed_button.text == "/start":
            self.client_rep.create_user(
                user_id,
                msg.chat.first_name,
                msg.chat.username,
                new_update_id
            )

            return self.response_res.send_full_response(
                {
                    "user_id": user_id,
                    "text_msg": base_names.WELCOME_MESSAGE,
                    "key_board": KeyBoard(base_names.StartButtons.buttons_array).get_keyboard()
                }
            )

        user_info: UserEntity = self.client_rep.get_user_info(user_id)

        if new_update_id <= user_info.update_id:
            return self.response_res.send_short_response()

        button_strategy = HandleButton().execute(pushed_button)

        text_msg, key_board = button_strategy.get()

        self.client_rep.change_update_id(user_id, new_update_id)

        return self.response_res.send_full_response(
            {
                "user_id": user_id,
                "msg": text_msg,
                "key_board": KeyBoard(key_board).get_keyboard()
            }
        )
