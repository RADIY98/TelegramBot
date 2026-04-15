from abc import ABC, abstractmethod

from bot_app.domain.entities.user_entity import UserEntity


class IUserRepository(ABC):

    @abstractmethod
    def get_user_info(self, user_id: int) -> UserEntity:
        pass

    @abstractmethod
    def create_user(self, user_id: int) -> None:
        pass
