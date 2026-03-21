from fastapi import FastAPI
from .BotBody import get_updates, send_message, router
from .database import init_tables
from psycopg2 import connect

from .infrastructure.db.postgres import DatabaseStart

app = FastAPI()
app.include_router(router)
DatabaseStart(connect(
            f"dbname=telegram_bot_db user={DbUser.DB_ROLE} host=postgres password={DbUser.ADMIN_PASSWORD} port=5432"
        )).execute()
