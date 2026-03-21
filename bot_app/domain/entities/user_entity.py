from dataclasses import dataclass

@dataclass
class UserEntity:
    """
    Класс клиента
    """
    user_id: int
    update_id: int
    first_name: str
    user_name: str