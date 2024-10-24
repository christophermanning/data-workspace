from flask import Flask, request, render_template
import os
import json

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    services = json.loads(os.getenv("SERVICES"))

    return render_template('index.html', services=services)
