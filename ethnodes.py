
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


def get_current_epoch():
    return 1230

def send_error_msg(): 
    return jsonify({'error_msg':'no response from Prysm api'}), 505

def send_sucess_msg(response):
    return_data = ast.literal_eval(response)
    return_data['message'] = 'Sucess'
    return jsonify(return_data), 200

@app.route('/attestations')
def get_attestations():
    
    '''
    Retrieve attestations by block root, slot, or epoch.
    An attestation is a validator’s vote, weighted by the validator’s balance.  
    Attestations are broadcasted by validators in addition to blocks.
    '''

    url = base_url+"/eth/v1alpha1/beacon/attestations"
    current_epoch = str(get_current_epoch())
    pageSize = 10
    attestations = http.request(
        'GET',
        url,
        fields={
            'epoch' : current_epoch,
            'pageSize' : pageSize 
        } 
    )

    if attestations.status == 200:
        response = attestations.data.decode('UTF-8')
        return send_sucess_msg(response)
    else:
        return send_error_msg()

@app.route('/get_block_stream')
def get_block_stream():
    api = '/eth/v1alpha1/beacon/blocks/stream'
    url = base_url+api
    block_stream = requests.get(url,headers=headers)
    print (block_stream)

@app.route('/validators_queue')
def get_validator_queue():
    uri = '/eth/v1alpha1/validators/queue'
    url = base_url+uri
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()

@app.route('/beacon_configuration')
def get_beacon_configuration():
    uri = '​/eth​/v1alpha1​/beacon​/config'
    url = base_url+uri
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return send_sucess_msg(data)
    else:
        return send_error_msg()

@app.route('/get_current_beacon_state')
def get_current_beacon_state():
    try:
        uri = '/eth/v1alpha1/beacon/chainhead'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            return send_sucess_msg(data)
        else:
            return send_error_msg()
    except expression as identifier:
        pass



@app.route('/get_current_chain_state')
def get_current_chain_state():
    try:
        uri = '/eth/v1alpha1/beacon/chainhead'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            return send_sucess_msg(data)
        else:
            return send_error_msg()
    except expression as identifier:
        pass    


if __name__ == "__main__":
    print (dir())
    app.run(debug=True)


