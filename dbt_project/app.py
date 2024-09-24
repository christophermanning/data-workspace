# basic server to run dbt from airflow

from flask import Flask, request
from dbt.cli.main import dbtRunner, dbtRunnerResult

PORT = 8000

# https://docs.getdbt.com/reference/programmatic-invocations
dbt = dbtRunner()

app = Flask(__name__)

@app.route("/run", methods=['POST'])
def run():
    cli_args = ["run"]

    select = ''.join(c for c in request.form.get("select", "") if c.isalpha() or c == "_" or c == "*")
    if select != "":
        cli_args.extend(["--select", select])

    res: dbtRunnerResult = dbt.invoke(cli_args)

    if not res.success:
        return str(res.exception), 500

    if len(res.result) == 0:
        return f"Nothing built for {select}; adjust `select` parameter", 400

    lines = []

    for r in res.result:
        if r.status == "error":
            return r.message, 500
        lines.append(f"{r.node.name}: {r.status}")

    return "\n".join(lines)
