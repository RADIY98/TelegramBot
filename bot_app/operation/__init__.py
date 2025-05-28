from abc import ABCMeta, abstractmethod

class Operation:
    """
    Абстрактный класс операций
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self):
        """
        Создание
        """

    @abstractmethod
    def delete(self):
        """
        Удаление
        """

    @abstractmethod
    def change(self):
        """
        Изменение
        """

    @abstractmethod
    def rename(self):
        """
        Изменить название
        """