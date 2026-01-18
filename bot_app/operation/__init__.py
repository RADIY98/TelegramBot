from abc import ABC, abstractmethod
from typing import Tuple


class Operation(ABC):

    @abstractmethod
    def handler(self, status: int, msg: str) -> Tuple[str, list]:
        ...

    @abstractmethod
    def create(self,  msg: str) -> Tuple[str, list]:
        ...

    @abstractmethod
    def delete(self, msg: str) -> Tuple[str, list]:
        ...

    @abstractmethod
    def change(self, msg: str) -> Tuple[str, list]:
        ...

    @abstractmethod
    def rename(self, msg: str) -> Tuple[str, list]:
        ...

    @abstractmethod
    def update(self, msg: str) -> Tuple[str, list]:
        ...