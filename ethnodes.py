
from flask import Flask
import requests 
from requests.utils import requote_uri
import json
import ast 
from flask import jsonify
import urllib3
from flask_cors import CORS


http = urllib3.PoolManager()

app = Flask(__name__)
CORS(app)



base_url = "https://api.prylabs.net"
headers = {
    'accept': 'application/json',
}

def get_current_ethereum_price():
    api = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,JPY,EUR?1eef1b3afe86c87ccb9b43f6a7ed8c4483fc5076e99b0f8cecfcae04f054ec75'
    response = requests.get(api)
    if response.status_code == 200:
        data =  parse_dictionary(response.content.decode('UTF-8'))    
        price = data.get('USD')
        return price
    else:
        return ('error in parsing eth price')

def get_current_epoch():
    try:    
        uri = '/eth/v1alpha1/beacon/chainhead'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')    
            data = ast.literal_eval(data)
            return int(data.get('finalizedEpoch'))
    except Exception as e:
        print (e)
        return send_error_msg()


def send_error_msg(): 
    return jsonify({'error_msg':'no response from Prysm api'}), 505

def parse_dictionary(data):
    return (ast.literal_eval(data))    
    


def send_sucess_msg(response,**kwargs):
    if not type(response) ==  dict:
        response = parse_dictionary(response)
    response['message'] = 'Sucess'
    for k,v in kwargs.items():
        response[k] =  v

    return jsonify(response), 200

@app.route('/attestations')
def get_attestations():
    try:

        
        '''
        Retrieve attestations by block root, slot, or epoch.
        An attestation is a validator’s vote, weighted by the validator’s balance.  
        Attestations are broadcasted by validators in addition to blocks.
        '''

        url = base_url+"/eth/v1alpha1/beacon/attestations"
        current_epoch = str(get_current_epoch())
        pageSize = 2
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
            additional_data = {
                'defination' :'An attestation is a validator’s vote, weighted by the validator’s balance.  Attestations are broadcasted by validators in addition to blocks.'
            }
            return send_sucess_msg(response, **additional_data)
        else:
            return send_error_msg()
    except Exception as e :
        print(e)
        return send_error_msg()


@app.route('/get_block_stream')
def get_block_stream():
    try:
        api = '/eth/v1alpha1/beacon/blocks/stream'
        url = base_url+api
        block_stream = requests.get(url,headers=headers)
        print (block_stream)
    except Exception as e :
        print(e)
        return send_error_msg()

@app.route('/validators_queue')
def get_validator_queue():
    try:
        uri = '/eth/v1alpha1/validators/queue'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            data = parse_dictionary(data)
            return_data = {
                'public_keys' : data.get('activationPublicKeys'),
                'count' : len(data)
            } 
            return send_sucess_msg(return_data)
        else:
            return send_error_msg()
    except Exception as e :
        print(e)
        return send_error_msg()


#not working
@app.route('/beacon/beacon_configuration')
def get_beacon_configuration():
    try:

        uri = '​/eth​/v1alpha1​/beacon​/config'
        url = base_url+uri
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            return send_sucess_msg(data)
        else:
            return send_error_msg()

    except Exception as e :
        print(e)
        return send_error_msg()

@app.route('/beacon/get_current_beacon_state')
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

    except Exception as e :
        print(e)
        return send_error_msg()



@app.route('/beacon/get_current_chain_state')
def get_current_chain_state():
    try:
        uri = '/eth/v1alpha1/beacon/chainhead'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            data = parse_dictionary(data)
            return_data = {
                'finalizedEpoch' : data.get('finalizedEpoch'),
                'finalizedSlot' : data.get('finalizedSlot')
            }
            price = get_current_ethereum_price()
            peers_data = node_peers()


            additional_data = {
                'slot_defination' : 'A slot is a chance for a block to be added to the Beacon Chain and shards. A slot is like the block time, but slots can be empty as well',
                'epoch_defination' : 'Epoch is collection of slots , basically 32 slots i.e 6.4 minutes form one epoch',
                'price' : price,
                'peers_defination' : 'Peers are a fundamental element of the network who host ledgers and smart contracts',
                'peers_count' : len(peers_data.get('peers')),
                'peers' : peers_data.get('peers')
            }

            return send_sucess_msg(return_data, **additional_data)
        else:
            return send_error_msg()
    except Exception as e:
        print (e)




def node_peers():
    uri = '/eth/v1alpha1/node/peers'
    url = base_url+uri
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return parse_dictionary(data)


if __name__ == "__main__":
    app.run(debug=True,host= '0.0.0.0')


