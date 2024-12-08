from fastapi import FastAPI
from .BotBody import get_updates, send_message, router
from .database import init_tables

app = FastAPI()
app.include_router(router)
init_tables()
