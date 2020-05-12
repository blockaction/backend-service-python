import os, sys
from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '../')))

from flask import Flask
import requests 
from requests.utils import requote_uri
import json
import ast 
from flask import jsonify

from flask_cors import CORS
from flask_app import beacon
from flask_app import validator
from flask import request



app = Flask(__name__)
CORS(app)


@app.route('/beacon/get_current_chain_state')
def get_current_beacon_state():
    return beacon.get_current_chain_state()


@app.route('/validators/validators_list')
def get_validators():
    return beacon.get_validators_api(request.args)



@app.route('/validators_queue')
def get_validator_queue():
    return beacon.get_validator_queue()


@app.route('/attestations')
def get_attestations():
    return beacon.get_attestations(request.args)


@app.route('/get_validator_participation')
def get_graph_data():
    return beacon.get_validator_participation()

@app.route('/validator/info/<publicKey>')
def get_validators_detail_by_public_key(publicKey):
    return beacon.get_validators_detail_by_public_key(publicKey)


@app.route('/getinfo/<data>')
def get_info(data):
    return beacon.searchable_data(data)

if __name__ == "__main__":
    app.run(debug=True,host= '0.0.0.0')
