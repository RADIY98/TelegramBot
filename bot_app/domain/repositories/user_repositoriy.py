from abc import ABC

from bot_app.domain.entities.user_entity import UserEntity


class IUserRepository(ABC):

    @staticmethod
    def get_user_info(user_id: int) -> UserEntity:
        pass

    @staticmethod
    def create_user(user_id: int, first_name: str, username: str, update_id: int) -> None:
        pass

    @staticmethod
    def change_update_id(user_id: int, update_id: int) -> None:
        pass

    @staticmethod
    def update_user_status(user_id: int, new_status: int) -> None:
        pass

    @staticmethod
    def update_user_selected_entity(user_id: int, new_entity: int) -> None:
        pass
