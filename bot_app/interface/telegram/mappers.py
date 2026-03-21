from typing import Optional

from ...application.dto.pressed_buttons import PressedButton
from ...domain.entities.user_entity import UserEntity


def request_to_button(request: dict):
    data: Optional[str]= request.get("callback_query").get("data")
    return PressedButton(
        user_id=request.get("chat").get("id"),
        button_id=int(data) if data else None,
        text=request.get("message").get("text")
    )

def request_to_user(request: dict):
    return UserEntity(
        user_id=request.get("chat").get("id"),
        update_id=request.get("update_id")
    )