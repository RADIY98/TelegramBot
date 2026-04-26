from abc import ABC

class IResponseResolver(ABC):
    """Interface of reponses"""

    @staticmethod
    def send_short_response():
        pass

    @staticmethod
    def send_full_response(params: dict):
        pass
