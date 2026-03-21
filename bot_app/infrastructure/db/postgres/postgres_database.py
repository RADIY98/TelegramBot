from typing import Any, Dict, List


class Database:
    def __init__(self, dns):
        self.dns=dns

    def sql_query(self, sql_request: str, *args) -> List[Dict[str, Any]]:
        """
        Выполняем запрос к бд
        """
        # connection = connect(
        #     f"dbname=telegram_bot_db user={DbUser.DB_ROLE} host=postgres password={DbUser.ADMIN_PASSWORD} port=5432"
        # )
        result_list = []
        dict_value = {}

        print(sql_request)
        print(args)
        cursor = self.dns.cursor()
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
        self.dns.commit()

        return result_list

    def sql_query_record(self, sql_tmpl: str, params=None) -> Dict[str, Any]:
        """
        SQL request to DB
        """
        # connection = connect(
        #     f"dbname=telegram_bot_db user={DbUser.DB_ROLE} host=postgres password={DbUser.ADMIN_PASSWORD} port=5432"
        # )

        print(sql_tmpl)
        print(params)
        result = {}

        cursor = self.dns.cursor()
        cursor.execute(sql_tmpl, params)
        if cursor.description:
            fields = [column.name for column in cursor.description]
            data = cursor.fetchone()
            if not data:
                data = [None for _ in fields]
            for fields_name, value in zip(fields, data):
                result[fields_name] = value

        cursor.close()
        self.dns.commit()

        return result

    def sql_query_scalar(self, sql_tmpl: str, args) -> Dict:
        """
        SQL request to DB

        :param sql_tmpl: SQL template
        :param args: args
        :return:
        """
        result = {}
        # connection = connect(
        #     f"dbname=telegram_bot_db user={DbUser.DB_ROLE} host=postgres password={DbUser.ADMIN_PASSWORD} port=5432"
        # )
        print(sql_tmpl)
        print(args)
        cursor = self.dns.cursor()
        cursor.execute(sql_tmpl, args)
        if cursor.description:
            data = cursor.fetchone()
            result = data[0] if data else None

        cursor.close()
        self.dns.commit()

        return result
