
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

#Node 

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


@app.route('/node/peers')
def node_peers():
    uri = '/eth/v1alpha1/node/peers'
    url = base_url+uri
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()


@app.route('/node/services')
def node_services():
    url = 'https://api.prylabs.net/eth/v1alpha1/node/services'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()


@app.route('/node/version')
def node_version():
    uri = 'eth/v1alpha1/node/version'
    url = base_url+uri
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()

# BeaconNodeValidator :-

@app.route('/validator/chainstart_stream')
def validator_chainstartstream():
    url = 'https://api.prylabs.net/eth/v1alpha1/validator/chainstart/stream'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()




@app.route('/validator/domain')
def valiidator_domain():
    url = 'https://api.prylabs.net/eth/v1alpha1/validator/domain'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()





@app.route('/validator/duties')
def validator_duties():
    url = 'https://api.prylabs.net/eth/v1alpha1/validator/duties'
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
    print (dir())
    app.run(debug=True)