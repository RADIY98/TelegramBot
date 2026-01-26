from ..database import sql_query_scalar, sql_query_record


def get_client_selected_entity(client_id: int) -> int:
    """
    Получим ид сущности которой будем делать изменения
    """
    result = sql_query_scalar(
        """
        SELECT
            "SelectedEntity"
        FROM
            "Client"
        WHERE
            "id"=%(client)s::bigint
        """, {"client": client_id}
    )
    return result


def get_all_trains_for_keyboard(client_id) -> list:
    """
    Получить тренировку
    """
    result = sql_query_scalar(
        """
            SELECT
                array_agg("Name")
            FROM
                "Train"
            WHERE
                "ClientID"=%s::bigint
            GROUP BY
                "ClientID"
        """, [client_id]
    )

    return result if result else []


def get_all_exercises_for_keyboard(train_id: int) -> str:
    """
    Получить тренировку
    """
    result = sql_query_scalar(
        """
            SELECT
                "Settings"
            FROM
                "Exercise"
            WHERE
                "TrainId"=%s::bigint
        """, [train_id]
    )
    msg = ""
    for ex_name, ex_value in result.items():
        if len(list(filter(None, ex_value))) > 1:
            msg += (f"{ex_name}: \n Веса - {','.join(i for i in ex_value[0])} \n "
                    f"Количество подходов - {','.join(i for i in ex_value[1])}\n\n")
        else:
            msg += f"{ex_name}: \nКоличество подходов - {','.join(i for i in ex_value[0])}\n\n"

    return msg


def read_train(client_id: int, train_id: int) -> dict:
    """
    Прочитать тренировку
    """
    result = sql_query_record(
        """        
        SELECT
            *
        FROM 
            "Train"
        WHERE
            "id" = %s::bigint AND
            "ClientID"=%s::bigint
            """, [train_id, client_id]
    )
    return result


def get_client_data(client_id: int) -> dict:
    """
    Получить разом информацию по клиенту
    """
    result = sql_query_record(
        """
        WITH trains AS (
            SELECT
                array_agg("Name")
            FROM
                "Train"
            WHERE 
                "ClientID"=%s::bigint
            GROUP BY
                "ClientID"
        )
        SELECT
            "id"::bigint,
            "UpdateId"::bigint,
            "Status"::int,
            "SelectedEntity"::bigint,
            (SELECT * FROM trains) "Trains"
        FROM
            "Client"
        WHERE
            "id" = %s::bigint
        """, [client_id, client_id]
    )
    return result
