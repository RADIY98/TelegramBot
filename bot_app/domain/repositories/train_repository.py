from abc import ABC, abstractmethod
from typing import List

from ..entities.train_entity import Train

class ITrainRepository(ABC):

    @abstractmethod
    def read(self, train_id: int) -> Train:
        pass