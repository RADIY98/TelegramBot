from ...application.dto.pressed_buttons import PressedButton
from ...domain.entities.user_entity import UserEntity


def request_to_button(request: dict):
    return PressedButton(
        user_id=request.get("chat").get("id"),
        button_id=int(request.get("callback_query").get("data"))
    )

def request_to_user(request: dict):
    return UserEntity(
        user_id=request.get("chat").get("id"),
        update_id=request.get("update_id")
    )