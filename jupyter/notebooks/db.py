# This proxy will close the connection after querying to avoid concurrency locks with external processes: Airflow, dbt, other notebooks
import duckdb
from duckdb import ConnectionException


class QueryResult:
    def __init__(self, query_string, params):
        self.query_string = query_string
        self.params = params
        self.connect()

    def connect(self):
        self.conn = duckdb.connect("/duckdb/dev.duckdb")
        self.conn.query("LOAD spatial")

    def _ipython_display_(self):
        self.show()

    def query(self):
        e = None

        # retry with reconnect if connection is closed
        for _ in range(2):
            try:
                result = self.conn.query(self.query_string, params=self.params)
                return result
            except ConnectionException as ce:
                self.connect()
                e = ce
            except Exception as e:
                self.conn.close()
                raise e

        raise e

    def show(self):
        try:
            result = self.query().show()
        finally:
            self.conn.close()
        return result

    def df(self):
        try:
            result = self.query().df()
        finally:
            self.conn.close()
        return result

    def fetchall(self):
        try:
            result = self.query().fetchall()
        finally:
            self.conn.close()
        return result


def query(query_string, params=None):
    return QueryResult(query_string, params)
