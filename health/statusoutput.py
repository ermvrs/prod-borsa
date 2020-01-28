from flask import Flask
from health.healthcontroller import InformationDatabase
import json
app = Flask("__main__")

@app.route('/')
def hello():
    return "Hello"

@app.route('/errors')
def errorlist():
    json_string = json.dumps([ob.__dict__ for ob in InformationDatabase.getInstance().getObject("Errors")])
    return json_string