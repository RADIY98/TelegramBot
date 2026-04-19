from bot_app.application.dto.pressed_buttons import PressedButton
from bot_app.domain.buttons.buttons_val_obj import Button


class HandleButton:
    def execute(self, button: PressedButton):
        if button.button_id == Button.TRAINS:
            pass
        elif button.button_id == Button.EXERCISE:
            pass
        else:
            pass
