
from flask import Flask
import requests 
from requests.utils import requote_uri
import json
import ast 
from flask import jsonify
import urllib3
http = urllib3.PoolManager()

app = Flask(__name__)


base_url = "https://api.prylabs.net"
headers = {
    'accept': 'application/json',
}
 


def send_error_msg():
    return jsonify({'error_msg':'no response from Prysm api'}), 505

def send_sucess_msg(response):
    return_data = ast.literal_eval(response)
    return_data['message'] = 'Sucess'
    return jsonify(return_data), 200


@app.route('/node/genesis')
def node_genesis():
    uri = '/eth/v1alpha1/node/genesis'
    url = base_url+uri
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()


#problem
@app.route('/node/syncing')
def node_syncing():
    url = 'https://api.prylabs.net/eth/v1alpha1/node/syncing'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()



@app.route('/node/version')
def node_version():
    # uri = 'eth/v1alpha1/node/version'
    url = 'https://api.prylabs.net/eth/v1alpha1/node/version'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()



@app.route('/validator/get_attestation')
def get_validator_attestation():
    current_slot =  81183
    url = 'https://api.prylabs.net/eth/v1alpha1/validator/attestation?slot=' + str(current_slot)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()


@app.route('/validator/blocks')
def validator_blocks():
    _epoch = 2163
    url = 'https://api.prylabs.net/eth/v1alpha1/beacon/blocks?epoch=' + str(_epoch)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()
  



@app.route('/validator/duties')
def validator_duties():
    epoch_number = 2304
    url = 'https://api.prylabs.net/eth/v1alpha1/validator/duties?epoch=' + str(epoch_number) + '&publicKeys='
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()



@app.route('/validator/status')
def validator_status():
    url = 'https://api.prylabs.net/eth/v1alpha1/validator/status'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()






#problem
@app.route('/validator/stream')
def validator_synced_stream():
    url = 'https://api.prylabs.net/eth/v1alpha1/validator/synced/stream'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()



if __name__ == "__main__":
    app.run(debug=True)