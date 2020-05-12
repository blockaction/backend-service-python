from .import third_party
from .import node
from client import client_beacon_chain
from flask_app import common, models
import json 
import requests
import chardet
import urllib3
http = urllib3.PoolManager()
import sys,os 
import base64
import request 


base_url = common.api()

def get_current_chain_state():
    try:

        response = client_beacon_chain.GetChainHead()
        
        if response:
            return_data = {
                'finalizedEpoch' : response.finalized_epoch,
                'finalizedSlot' : response.finalized_slot
            }
            price = third_party.get_current_ethereum_price()
            peers_data =  node.node_peers() #TODO get node from rpc 


            additional_data = {
                'slot_defination' : 'A slot is a chance for a block to be added to the Beacon Chain and shards. A slot is like the block time, but slots can be empty as well',
                'epoch_defination' : 'Epoch is collection of slots , basically 32 slots i.e 6.4 minutes form one epoch',
                'price' : price,
                'peers_defination' : 'Peers are a fundamental element of the network who host ledgers and smart contracts',
                'peers_count' : len(peers_data.get('peers')),
                'peers' : peers_data.get('peers')
            }

            return common.send_sucess_msg(return_data, **additional_data)

    except Exception as e:
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()


def list_validators_grpc():
    try:
        response = client_beacon_chain.list_validators()
        if not response:
            raise ('Error')

        validator_list = []

        for data in response:
            single_data =  data.validator
            data_dist = dict()

            pk = single_data.public_key

            data_dist['public_key'] = common.decode_public_key(pk)
            data_dist['effective_balance'] = single_data.effective_balance
            validator_list.append(data_dist)
        
        return common.send_sucess_msg({'data':validator_list})
            
    except Exception as e :
        print (e)





def get_validators_api(args):
    pageToken = args.get("page", "1")
    uri = '/eth/v1alpha1/validators'
    url = base_url+uri
    pageSize = 10
    validators = http.request(
        'GET',
        url,
        fields={
            'epoch' : third_party.get_current_epoch(),
            'pageToken' : pageToken,
            'pageSize' : pageSize
        } 
    )

    if validators.status == 200:
        validators =  json.loads(validators.data.decode('UTF-8'))
        additional_data = {
            'count' : len(validators.get('validatorList'))
        }
        # pk = validators.get('validatorList')[0]
        # pk = dict(pk.get('validator'))
        # print (pk)
        # pk = pk.get('publicKey')
        # pk = common.decode_public_key(pk)
        # print (pk)
        return common.send_sucess_msg(validators, **additional_data)
    


def get_validator_queue():

    try:
        uri = '/eth/v1alpha1/validators/queue'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            data = common.parse_dictionary(data)
            return_data = {
                'public_keys' : data.get('activationPublicKeys'),
                'count' : len(data)
            } 
            return common.send_sucess_msg(return_data)
        else:
            return common.send_error_msg()
    except Exception as e :
        print(e)
        return common.send_error_msg()



def get_attestations(args):
    try:
        pageToken = args.get("page", "1")
        url = base_url+"/eth/v1alpha1/beacon/attestations"
        current_epoch = str(third_party.get_current_epoch())
        pageSize = 10
        attestations = http.request(
            'GET',
            url,
            fields={
                'epoch' : current_epoch,
                'pageSize' : pageSize,
                'pageToken' : pageToken 
            } 
        )

        if attestations.status == 200:
            response = attestations.data.decode('UTF-8')
            additional_data = {
                'defination' :'An attestation is a validator’s vote, weighted by the validator’s balance.  Attestations are broadcasted by validators in addition to blocks.'
            }
            return common.send_sucess_msg(response, **additional_data)
        else:
            return common.send_error_msg()
    except Exception as e :
        print(e)
        return common.send_error_msg()


def get_validator_participation():
    db =  models.mongo_conn()
    data = db.graph_data.find({}).limit(10)
    return_data = []
    for d in data :
        return_dict = {}
        return_dict['epoch'] =  d.get('epoch')
        return_dict['ether'] = d.get('ether')
        return_data.append(return_dict)

    return common.send_sucess_msg({'data':return_data})


# Validator info  by Publick Key


def get_validators_detail(publicKey):
    uri = '/eth/v1alpha1/validator/status'
    url = base_url+uri
    validators = http.request(
        'GET',
        url,
        fields={
            'publicKey' : publicKey            
        } 
    )

    if validators.status == 200:
        status_data = validators.data.decode('UTF-8')
        status_data = common.parse_dictionary(status_data)
        return_data = {
            'status' : status_data.get('status'),
            'activationEpoch' : status_data.get('activationEpoch')
        }
        
        uri = '/eth/v1alpha1/validators/balances'
        url = base_url+uri

        response = http.request(
            'GET',
            url,
            fields={
                'publicKeys' : publicKey
            } 
        )

        if response.status == 200:
            balance_data = response.data.decode('UTF-8')
            balance_data = common.parse_dictionary(balance_data).get('balances')
            balance_data = balance_data[0]

            balance =  int(balance_data.get('balance'))/9000000000
            balance = str(round(balance, 2)) +" ETH"

            index = balance_data.get('index')

        
            return_data['balance'] = balance
            return_data['index'] = index

            return common.send_sucess_msg(return_data)
    else:
        return common.send_error_msg()
