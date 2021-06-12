import ast
import json


def fetch_one_result_by_json(cursor):
    for row in cursor.fetchall():
        return json.loads(row[0])


def cursor_fetch_all(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def fetch_result(cursor):
    columns = [col[0] for col in cursor.description]
    res = []
    for row in cursor.fetchall():
        r = {}
        for i, c in enumerate(row):
            try:
                r[columns[i]] = ast.literal_eval(c)
            except Exception:
                r[columns[i]] = c
        res.append(r)
    return res
