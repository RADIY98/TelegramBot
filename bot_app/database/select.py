from bot_app.database import sql_query


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
