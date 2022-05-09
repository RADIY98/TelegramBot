from fastapi import FastAPI
from typing import Optional


class Application(FastAPI):
    def __init__(self, params: Optional[dict]):
        super().__init__()
        self.params = params

    def create_app(self):
        return FastAPI(**self.params)
