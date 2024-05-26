from fastapi import FastAPI
from .BotBody import get_updates, send_message, router


app = FastAPI()
app.include_router(router)
