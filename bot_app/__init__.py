from fastapi import FastAPI
from typing import Optional


class Application(FastAPI):
    def __init__(self, params: Optional[dict]):
        self.params = params

    def create_app(self):
        return FastAPI(**self.params)
