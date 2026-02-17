from typing import Optional, List, Dict

from . import sql_query


class ClientRepository:

    @staticmethod
    def update_status(client_id: int, client_status: Optional[int]) -> List[Dict]:
        """
        Обновляем клиентский статус
        """
        return sql_query(
            """
            UPDATE
                "Client"
            SET 
                "Status"=%s::bigint
            WHERE
                "id"=%s::bigint
            RETURNING
                "id",
                "UpdateId"
            """, (client_status, client_id)
        )

    @staticmethod
    def update_selected_entity(client_id: int, msg: Optional[str]) -> None:
        """
        Обновлем ид выбранной сущности
        """
        sql_query(
            """
            WITH determine_selected_entity AS (
                SELECT
                    "id"
                FROM 
                    "Train"
                WHERE
                    "Name"=%s::text
                UNION
                SELECT
                    "id"
                FROM
                    "Exercise"
                WHERE
                    "Name"=%s::text
            )
            UPDATE
                "Client"
            SET
                "SelectedEntity"=(SELECT * FROM "determine_selected_entity" LIMIT 1)
            WHERE
                "id"=%s::bigint
            """, (msg, msg, client_id)
        )