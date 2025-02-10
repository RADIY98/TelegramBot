from psycopg2 import connect


def init_tables():
    __create_client_table()
    __create_train_table()
    __create_exercise_table()


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


def sql_query(sql_request: str, *args):
    """
    Выполняем запрос к бд
    """
    connection = connect("dbname=telegram_bot_db user=postgres host=postgres password=postgres port=5432")
    # connection = connect("dbname=telegram_bot_db user=postgres password=postgres port=5432")
    result_list = []
    dict_value = {}

    print(sql_request)
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


def sql_query_record(sql_tmpl: str, params = None) -> dict:
    """
    SQL request to DB

    :param sql_tmpl: SQL template
    :param args: args
    :return:
    """
    connection = connect("dbname=telegram_bot_db user=postgres host=postgres password=postgres port=5432")
    # connection = connect("dbname=telegram_bot_db user=postgres password=postgres port=5432")

    result = {}

    cursor = connection.cursor()
    cursor.execute(sql_tmpl, params)
    if cursor.description:
        data = cursor.fetchone()
        fields = [column.name for column in cursor.description]
        for fields_name, value in zip(fields, data):
            result[fields_name] = value

    cursor.close()
    connection.commit()

    return result


def sql_query_scalar(sql_tmpl: str, args):
    """
    SQL request to DB

    :param sql_tmpl: SQL template
    :param args: args
    :return:
    """
    result = {}
    connection = connect("dbname=telegram_bot_db user=postgres host=postgres password=postgres port=5432")
    # connection = connect("dbname=telegram_bot_db user=postgres password=postgres port=5432")

    cursor = connection.cursor()
    cursor.execute(sql_tmpl, args)
    if cursor.description:
        data = cursor.fetchone()
        result = data[0] if data else None

    cursor.close()
    connection.commit()

    return result
