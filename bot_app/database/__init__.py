from typing import Any, Dict, List

from psycopg2 import connect
from ..base_names import DbUser, DB_PASSWORD


def init_tables():
    __create_custom_user()
    __create_client_table()
    __create_train_table()
    __create_exercise_table()


def __create_custom_user():
    """
    СОздаем нового пользователя в БД для безопасности
    """
    connection = connect(f"dbname=telegram_bot_db user='postgres' host=postgres password={DB_PASSWORD} port=5432")
    # connection = connect("dbname=telegram_bot_db user=postgres password=postgres port=5432")
    is_role_exist = False
    cursor = connection.cursor()
    cursor.execute(
        f"""
           SELECT 1 FROM pg_roles WHERE rolname = '{DbUser.DB_ROLE}'
        """
    )
    if cursor.description:
        data = cursor.fetchone()
        is_role_exist = data[0] if data else False
    if not is_role_exist:
        cursor.execute(f"""
            -- 2. Создаём отдельного пользователя для работы с БД  
            CREATE USER {DbUser.DB_ROLE} WITH LOGIN PASSWORD '{DbUser.ADMIN_PASSWORD}';  
            
            -- 3. Даём права только на нужные БД  
            GRANT CONNECT, CREATE ON DATABASE telegram_bot_db TO {DbUser.DB_ROLE};  
            
            -- 4. Даём права на схемы и таблицы (но не на всё подряд)  
            GRANT USAGE, CREATE ON SCHEMA public TO {DbUser.DB_ROLE};  
            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {DbUser.DB_ROLE};  
            
            -- 5. Отзываем опасные права у суперпользователя (если нужно)  
            ALTER USER postgres WITH NOSUPERUSER;  -- оставляем только для админских задач  
            """)

    cursor.close()
    connection.commit()


def __create_client_table() -> None:
    """
    Создаем таблицу клиента
    """
    sql_query(
        """
        CREATE TABLE IF NOT EXISTS "Client" (
        "id" INTEGER PRIMARY KEY,
        "FirstName" TEXT NOT NULL,
        "UserName" TEXT NOT NULL,
        "UpdateId" INTEGER NOT NULL,
        "Status" INTEGER,
        "SelectedEntity" INTEGER
        )
        """
    )


def __create_train_table() -> None:
    """
    Создаем таблицу тренировок
    """
    sql_query(
        """
        CREATE TABLE IF NOT EXISTS "Train" (
        "id" SERIAL PRIMARY KEY,
        "Name" text NOT NULL,
        "ClientID" INTEGER NOT NULL REFERENCES "Client"(id) ON DELETE CASCADE
        )
        """
    )


def __create_exercise_table() -> None:
    """
    Создаем таблицу упражнений
    """
    sql_query(
        """
        CREATE TABLE IF NOT EXISTS "Exercise" (
        "id" SERIAL PRIMARY KEY,
        "Name" text NOT NULL,
        "TrainId" INTEGER NOT NULL REFERENCES "Train"(id) ON DELETE CASCADE,
        "Settings" jsonb
        )
        """
    )


def sql_query(sql_request: str, *args) -> List[Dict[str, Any]]:
    """
    Выполняем запрос к бд
    """
    connection = connect(
        f"dbname=telegram_bot_db user={DbUser.DB_ROLE} host=postgres password={DbUser.ADMIN_PASSWORD} port=5432"
    )
    result_list = []
    dict_value = {}

    print(sql_request)
    print(args)
    cursor = connection.cursor()
    cursor.execute(sql_request, *args)
    if cursor.description:
        data = cursor.fetchall()
        fields_name = cursor.description
        fields_name = [column.name for column in fields_name]
        for one_list in data:
            for fields, value in zip(fields_name, one_list):
                dict_value[fields] = value
            result_list.append(dict_value)
            dict_value = {}
    cursor.close()
    connection.commit()

    return result_list


def sql_query_record(sql_tmpl: str, params = None) -> Dict[str, Any]:
    """
    SQL request to DB
    """
    connection = connect(
        f"dbname=telegram_bot_db user={DbUser.DB_ROLE} host=postgres password={DbUser.ADMIN_PASSWORD} port=5432"
    )

    print(sql_tmpl)
    print(params)
    result = {}

    cursor = connection.cursor()
    cursor.execute(sql_tmpl, params)
    if cursor.description:
        fields = [column.name for column in cursor.description]
        data = cursor.fetchone()
        if not data:
            data = [None for _ in fields]
        for fields_name, value in zip(fields, data):
            result[fields_name] = value

    cursor.close()
    connection.commit()

    return result


def sql_query_scalar(sql_tmpl: str, args) -> Dict:
    """
    SQL request to DB

    :param sql_tmpl: SQL template
    :param args: args
    :return:
    """
    result = {}
    connection = connect(
        f"dbname=telegram_bot_db user={DbUser.DB_ROLE} host=postgres password={DbUser.ADMIN_PASSWORD} port=5432"
    )
    print(sql_tmpl)
    print(args)
    cursor = connection.cursor()
    cursor.execute(sql_tmpl, args)
    if cursor.description:
        data = cursor.fetchone()
        result = data[0] if data else None

    cursor.close()
    connection.commit()

    return result
