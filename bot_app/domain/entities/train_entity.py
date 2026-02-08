from ..database import sql_query, sql_query_record, sql_query_scalar


class TrainStatus:
    """
    Статусы тренировок
    """
    CHANGE = 1
    DELETE = 2
    CREATE = 3
    RENAME = 4
    status_array = [CREATE, DELETE, CHANGE, RENAME]
