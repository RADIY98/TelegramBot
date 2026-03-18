from dataclasses import dataclass

@dataclass
class UserEntity:
    """
    Класс клиента
    """
    user_id: int
    update_id: int
    first_visit: bool = True