# This proxy will close the connection after querying to avoid concurrency locks with external processes: Airflow, dbt, other notebooks
import duckdb


class QueryResult:
    query = None
    params = None

    def __init__(self, query, params):
        self.query = query
        self.params = params

        self.conn = duckdb.connect("/duckdb/dev.duckdb")
        self.conn.query("LOAD spatial")

    def _ipython_display_(self):
        self.show()

    def show(self):
        q = self.conn.query(self.query, params=self.params).show()
        self.conn.close()
        return q

    def df(self):
        q = self.conn.query(self.query, params=self.params).df()
        self.conn.close()
        return q

    def fetchall(self):
        q = self.conn.query(self.query, params=self.params).fetchall()
        self.conn.close()
        return q


def query(query, params=None):
    return QueryResult(query, params)
