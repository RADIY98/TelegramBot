from abc import ABC, abstractmethod
from typing import List

from ..entities.train_entity import Train

class TrainRepository(ABC):

    @abstractmethod
    def add(self, client: int, train_name: str) -> None:
        pass

    @abstractmethod
    def delete(self, train_id: int) -> None:
        pass

    @abstractmethod
    def read(self, train_id: int) -> Train:
        pass

    @abstractmethod
    def rename(self, train_id: int, new_train_name: str) -> None:
        pass

    @abstractmethod
    def get_all_trains_name(self, client_id: int) -> List[str]:
        pass
