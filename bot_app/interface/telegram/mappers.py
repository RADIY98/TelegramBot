from typing import Optional, List

from ...application.dto.pressed_buttons import PressedButton
from ...domain.entities.user_entity import UserEntity


def request_to_button(request: dict):
    data: Optional[str]= request.get("callback_query").get("data")
    split_data: List[Optional[str], Optional[str]] = data.split(sep=",") if data else ["None", "None"]
    button_id, entity_id = split_data

    if button_id:
        button_id = int(button_id)

    if entity_id:
        entity_id = int(entity_id)

    return PressedButton(
        user_id=request.get("chat").get("id"),
        button_id=button_id,
        entity_id=entity_id,
        text=request.get("message").get("text")
    )

def request_to_user(request: dict):
    return UserEntity(
        user_id=request.get("chat").get("id"),
        update_id=request.get("update_id")
    )