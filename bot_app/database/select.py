from typing import List, Dict, Optional

from bot_app.database import sql_query, sql_query_scalar


def select_trains(client_id: int):
    sql_query(
        f"""
            SELECT
                *
            FROM
                "Train"
            WHERE
                "ClientID"={client_id}::int    
        """
    )

def get_clients_update_id(clients: List[int]) -> Dict[int, int]:
    """
    Получим данные клиентов из БД
    """
    clients_last_update: Optional[dict] = sql_query_scalar(
        """
                    SELECT
                        jsonb_build_object(
                            "id"::bigint, "UpdateId"::bigint
                        ) AS Result
                    FROM
                        "Client"
                    WHERE
                        "id" = ANY(%(clients)s::bigint[])
                """, {'clients': clients}
    )
    if clients_last_update:
        clients_last_update = {int(key): value for key, value in clients_last_update.items()}
    else:
        clients_last_update = {}

    return clients_last_update


def get_client_status(client: int) -> int:
    """
    Получим статус клиента
    """
    clients_last_update: int = sql_query_scalar(
        """
                    SELECT
                        "Status"
                    FROM
                        "Client"
                    WHERE
                        "id" = %(client)s::bigint
                """, {'client': client}
    )

    return clients_last_update

def get_client_selected_entity(client_id: int) -> int:
    """
    Получим ид сущности которой будем делать изменения
    """
    result = sql_query_scalar(
        f"""
        SELECT
            "SelectedEntity"
        FROM
            "Client"
        WHERE
            "id"=%(client)s::bigint
        """, {"client": client_id}
    )
    return result