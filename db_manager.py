import psycopg2

from config import config


class DBManager:
    def __init__(self, database_name, params):
        self.conn = psycopg2.connect(dbname=database_name, **params)


par = config()
d = DBManager('postgres', par)
d.conn()
