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
