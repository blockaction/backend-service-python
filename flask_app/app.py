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
from flask_app import beacon, third_party, common
from flask_app import validator
from flask import Flask,request


app = Flask(__name__)
CORS(app)


@app.route('/api/beacon/get_current_chain_state')
def get_current_beacon_state():
    return beacon.get_current_chain_state()


@app.route('/api/validators/validators_list')
def get_validators():
    return beacon.get_validators_api(request.args)



@app.route('/api/validators_queue')
def get_validator_queue():
    return beacon.get_validator_queue()


@app.route('/api/attestations')
def get_attestations():
    return beacon.get_attestations(request.args)


@app.route('/api/get_validator_participation')
def get_graph_data():
    return beacon.get_validator_participation()

@app.route('/api/validator/info/<publicKey>')
def get_validators_detail_by_public_kehiy(publicKey):
    return beacon.get_validators_detail_by_public_key(publicKey)


@app.route('/api/getinfo/<data>')
def get_info(data):
    return beacon.searchable_data(data)

@app.route('/api/get_eth_price')
def get_eth_price():
    return third_party.send_current_eth_price()

@app.route('/api/slot/<slot>')
def get_slot_data(slot):
    data =  beacon.get_slot_data(slot)
    if data:
        return common.send_sucess_msg({'data': data})
    else:
        return common.send_error_msg()

@app.route('/api/attestion')
def get_attestion_by_slot():
    return beacon.get_attestion_by_slot(request.args)

@app.route('/api/latest_block')
def get_latest_block():
    return beacon.get_latest_block()


@app.route('/api/epoch/<epoch_number>')
def get_epoch_data(epoch_number):
    return beacon.get_epoch_data(epoch_number)


@app.route('/api/get_participation_rate')
def get_participation_rate():
    return third_party.get_data_for_global_participation_rate()


@app.route('/api/get_latest_block')
def get_letest_block():
    return beacon.get_latest_block(request.args)


@app.route('/api/volume')
def get_volume():
    return third_party.get_vol_data(request.args)




if __name__ == "__main__":
    app.run(debug=False,host= '0.0.0.0')
