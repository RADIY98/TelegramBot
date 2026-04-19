from dataclasses import dataclass
from typing import Optional


@dataclass
class UserEntity:
    """User object"""
    user_id: int
    update_id: int
    first_name: str
    user_name: str
