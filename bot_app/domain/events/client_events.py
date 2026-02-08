from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ClientEventStatusChange:
    client_status: Optional[int]
    client_id: int


@dataclass(frozen=True)
class ClientEventSelectedEntityChange:
    selected_id: Optional[int]
    client_id: int