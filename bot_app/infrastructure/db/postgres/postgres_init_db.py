from psycopg2 import connect

from ....base_names import DbUser, DB_PASSWORD

class DatabaseStart:
    def __init__(self):
        self.dns = connect(
            f"dbname=telegram_bot_db user={DbUser.DB_ROLE} host=postgres password={DbUser.ADMIN_PASSWORD} port=5432"
        )

    def __create_custom_user(self):
        """Создаем нового пользователя в БД для безопасности"""

        # connection = connect(f"dbname=telegram_bot_db user='postgres' host=postgres password={DB_PASSWORD} port=5432")
        # connection = connect("dbname=telegram_bot_db user=postgres password=postgres port=5432")
        is_role_exist = False
        cursor = self.dns.cursor()
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

    def __create_client_table(self) -> None:
        """Создаем таблицу клиента"""

        cursor = self.dns.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS "User" (
            "id" INTEGER PRIMARY KEY,
            "FirstName" TEXT NOT NULL,
            "UserName" TEXT NOT NULL,
            "UpdateId" INTEGER NOT NULL,
            "Status" INTEGER,
            "SelectedEntity" INTEGER
            )
            """
        )
        cursor.close()

    def __create_train_table(self) -> None:
        """Создаем таблицу тренировок"""

        cursor = self.dns.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS "Train" (
            "id" SERIAL PRIMARY KEY,
            "Name" text NOT NULL,
            "ClientID" INTEGER NOT NULL REFERENCES "User"(id) ON DELETE CASCADE
            )
            """
        )
        cursor.close()


    def __create_exercise_table(self) -> None:
        """Создаем таблицу упражнений"""

        cursor = self.dns.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS "Exercise" (
            "id" SERIAL PRIMARY KEY,
            "Name" text NOT NULL,
            "TrainId" INTEGER NOT NULL REFERENCES "Train"(id) ON DELETE CASCADE,
            "Settings" jsonb
            )
            """
        )

    def execute(self):
        self.__create_custom_user()
        self.__create_client_table()
        self.__create_train_table()
        self.__create_exercise_table()

        self.dns.commit()
