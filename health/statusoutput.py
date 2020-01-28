from flask import Flask,request
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

@app.route('/pair')
def pairoutputs():
    pair = request.args.get('name',default="TESTBTC",type=str)
    json_string = json.dumps([ob.__dict__ for ob in InformationDatabase.getInstance().getObject(pair)])
    return json_string

@app.route('/signals')
def signalsout():
    json_string = json.dumps([ob.__dict__ for ob in InformationDatabase.getInstance().getObject('Signals')])
    return json_string

@app.route('/pairstatus')
def pairstateout():
    json_string = json.dumps(InformationDatabase.getInstance().getObject('PairStatus'))
    return json_string