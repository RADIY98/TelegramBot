from fastapi import FastAPI
from .BotBody import get_updates, send_message, router
from .database import init_tables

from .infrastructure.db.postgres.postgres_init_db import DatabaseStart

app = FastAPI()
app.include_router(router)

DatabaseStart().execute()
