from dataclasses import dataclass

@dataclass
class Train:
    """
    Статусы тренировок
    """
    train_id: int
    name: str
    client_id: int
