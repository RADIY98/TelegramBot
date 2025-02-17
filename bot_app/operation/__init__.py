from abc import ABCMeta, abstractmethod

class Operation:
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self, msg: str):
        """
        Создание
        """

    @abstractmethod
    def delete(self, msg: str):
        """
        Удаление
        """

    @abstractmethod
    def change(self, msg: str):
        """
        Изменение
        """

    @abstractmethod
    def rename(self, msg: str):
        """
        Изменить название
        """