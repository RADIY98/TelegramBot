from psycopg_pool import ConnectionPool

from bot_app.infrastructure.db.postgres.postgres_database import Database


def create_pool():
    connection_pool = ConnectionPool()
    db = Database(connection_pool)

    return db
