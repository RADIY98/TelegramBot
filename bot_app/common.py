import os
import json


def load_schema(schema_name):
    """
    Method for loading JSON-schema

    :param: Schema name
    :return:
    """
    full_path = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.join(full_path, 'schemas', schema_name + '.jsonschema')
    with open(file_name, 'r', encoding='utf-8') as file:
        schema_str = file.read()
    schema = json.loads(schema_str)

    return schema
