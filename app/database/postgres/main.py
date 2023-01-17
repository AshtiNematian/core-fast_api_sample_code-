import psycopg2
from app.core.config import settings, config


class PsqlClient:

    def __init__(self):
        self.conn = psycopg2.connect(settings.PSQL_URL)

    def get_cur(self):
        return self.conn.cursor()


psql_cru = PsqlClient().get_cur()
