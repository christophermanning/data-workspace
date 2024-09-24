from airflow.models.baseoperator import BaseOperator
from airflow.exceptions import AirflowSkipException

import urllib
import os

class ExtractOperator(BaseOperator):
    def __init__(self, uri: str, filename: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.uri = uri
        self.filename = filename

    def execute(self, context):
        filename = self.filename
        self.xcom_push(context, key="filename", value=filename)

        if os.path.isfile(filename):
            print(f"{filename} already exists")
            raise AirflowSkipException()
        else:
            print(f"Downloading {self.uri} to {filename}")
            urllib.request.urlretrieve(self.uri, filename)
