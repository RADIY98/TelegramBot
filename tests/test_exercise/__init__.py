import sys
from unittest.mock import MagicMock

# Создаём КОРРЕКТНЫЙ мок, который поддерживает []
mock_psycopg2 = MagicMock()  # ← MagicMock, а не Mock!
mock_conn = MagicMock()
mock_cursor = MagicMock()

# Ключевой момент: настраиваем возвращаемые значения
mock_cursor.fetchone.return_value = [True]  # СЛОВАРЬ!
mock_cursor.fetchall.return_value = [{"id": 1}, {"id": 2}]     # СПИСОК словарей!
mock_cursor.__getitem__.return_value = "значение"  # Поддержка cursor[индекс]

mock_conn.cursor.return_value = mock_cursor
mock_psycopg2.connect.return_value = mock_conn

# Подменяем в sys.modules
sys.modules['psycopg2'] = mock_psycopg2

from bot_app.operation import exercise