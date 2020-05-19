from .import third_party
from .import node
from client import client_beacon_chain
from flask_app import common 
from flask_app.models import mongo_helper
import json 
import requests
import chardet
import urllib3
http = urllib3.PoolManager()
import sys,os 
import base64


base_url = common.api()

def get_current_chain_state():
    try:
        response = client_beacon_chain.GetChainHead()
        if response:
            return_data = {
                'finalizedEpoch' : response.finalized_epoch,
                'finalizedSlot' : response.finalized_slot,
                'currentEpoch' : response.head_epoch,
                'currentSlot' : response.head_slot
            }

            voted_ether_data = get_participation_rate()
            if voted_ether_data:
                participation = voted_ether_data.get('participation')
                return_data['voted_ether'] = int(participation.get('votedEther'))/1000000000
                return_data['eligible_ether'] =  int(participation.get('eligibleEther'))/1000000000

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
    pageToken = args.get("page", "")
    pageSize = request.args.get("perPage", "")
    uri = '/eth/v1alpha1/validators'
    url = base_url+uri
    # pageSize = 10
    validators = http.request(
        'GET',
        url,
        fields={
            'slot' : third_party.get_current_slot(),
            'pageToken' : pageToken,
            'pageSize' : pageSize
        } 
    )

    if validators.status == 200:
        validators =  json.loads(validators.data.decode('UTF-8'))
        additional_data = {
            'count' : len(validators.get('validatorList'))
        }

        validators_list = validators.get('validatorList')
        for data in validators_list:
            pk = dict(data.get('validator'))
            pkB64 = pk.get('publicKey')
            pkHex = common.decode_public_key(pkB64)
            pk['publicKey'] = pkHex
            data['validator'] = pk


        return common.send_sucess_msg(validators, **additional_data)
    


def get_validator_queue():

    try:
        uri = '/eth/v1alpha1/validators/queue'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            data = common.parse_dictionary(data)
            queue = data.get('activationPublicKeys')
            return_data = {
                'public_keys' : queue,
                'count' : len(queue)
            } 
            return common.send_sucess_msg(return_data)
        else:
            return common.send_error_msg()
    except Exception as e :
        print(e)
        return common.send_error_msg()



def get_attestations(args):
    try:
        pageToken = args.get("page", "")
        pageSize = request.args.get("perPage", "")
        url = base_url+"/eth/v1alpha1/beacon/attestations"
        current_epoch = str(third_party.get_current_epoch())
        # pageSize = 10
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
            response = json.loads(attestations.data.decode('UTF-8'))
            attestation_list = response.get('attestations')
            attestation_list.reverse()
            for data in attestation_list:
                blockchain_data = data.get('data')
                blockchain_data['beaconBlockRoot'] = common.decode_public_key(blockchain_data.get('beaconBlockRoot'))
                data['data'] = blockchain_data

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
    db =  mongo_helper.mongo_conn()
    data = db.graph_data.find({}).limit(10)
    return_data = []
    for d in data :
        return_dict = {}
        return_dict['epoch'] =  d.get('epoch')
        return_dict['ether'] = d.get('ether')
        return_data.append(return_dict)

    return common.send_sucess_msg({'data':return_data})




def get_validators_detail_by_public_key(pubkeyHex):
    '''
        Validator info  by Publick Key
    '''
    uri = '/eth/v1alpha1/validator/status'
    url = base_url+uri
    pubkeyB64 = str(common.encode_pubic_key(pubkeyHex[2::]).decode('utf-8'))
    validators = http.request(
        'GET',
        url,
        fields={
            'publicKey' : pubkeyB64            
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
                'publicKeys' : pubkeyB64
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


def searchable_data(data):
    try: 
        check_data = data[:2]
        if check_data == '0x':
            return get_validators_detail_by_public_key(data)

    except Exception as e:
        pass 


def get_epoch_data(epoch_number):
    uri = '/eth/v1alpha1/validators/participation'
    url = base_url+uri
    response = http.request(
        'GET',
        url,
        fields={
            'epoch_number' : str(epoch_number)           
        } 
    )

    if response.status == 200:
        data = json.loads(response.data.decode('UTF-8'))        
        epoch = (data.get('epoch'))
        finalized = str(data.get('finalized'))
        voted_ether = int(data.get('participation').get('votedEther'))/1000000000
        participation_rate = int(data.get('participation').get('globalParticipationRate'))
        eligible_ether = int(data.get('participation').get('eligibleEther'))/1000000000
        # validtor quee lenth
        return_data = {
            'epoch': epoch,
            'finalized' :finalized,
            'voted_ether': str(voted_ether),
            'participation_rate' : str(participation_rate),
            'eligible_ether' : str(eligible_ether)
        }

        #  Total Validator Count
        uri = '/eth/v1alpha1/validators'
        url = base_url+uri
        validators = http.request(
            'GET',
            url,
            fields={
                'epoch' : epoch_number                         
            } 
        )

        if validators.status == 200:
            validators =  json.loads(validators.data.decode('UTF-8'))
            total_data = {
                'total_validator_count' : str(validators.get('totalSize'))
            }

       #  Pending Count
        uri = '/eth/v1alpha1/validators/queue'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            data = common.parse_dictionary(data)
            pending_data = {

                'pending_count' : str(len(data.get('activationPublicKeys')))
            } 
            
        return common.send_sucess_msg(return_data, **pending_data, **total_data)
    else:
        return common.send_error_msg()




# data from slot Number

def get_slot_data(slot):
    uri = '/eth/v1alpha1/beacon/blocks'
    url = base_url+uri
    response = http.request(
        'GET',
        url,
        fields={
            'slot' : slot          
        } 
    )

    if response.status == 200:
        slot_data = response.data.decode('UTF-8')
        slot_data = common.parse_dictionary(slot_data)
        return_data = {
            'slotNumber' : slot,
            'ParentRootHas' : common.decode_public_key(slot_data['blockContainers'][0]['block']['block']['parentRoot']),
            'proposer' : slot_data['blockContainers'][0]['block']['block']['proposerIndex'],
            'stateRoot' : common.decode_public_key(slot_data['blockContainers'][0]['block']['block']['stateRoot']),
            'signature' : common.decode_public_key(slot_data['blockContainers'][0]['block']['signature']),
            'blockRoot' : common.decode_public_key(slot_data['blockContainers'][0]['blockRoot']),
            'graffiti' : common.decode_public_key(slot_data['blockContainers'][0]['block']['block']['body']['graffiti']),
            'randaoReveal' : common.decode_public_key(slot_data['blockContainers'][0]['block']['block']['body']['randaoReveal']),
            'Eth_1_Block_Hash' :  common.decode_public_key(slot_data['blockContainers'][0]['block']['block']['body']['eth1Data']['blockHash']),
            'Eth_1_Deposit_Count' : slot_data['blockContainers'][0]['block']['block']['body']['eth1Data']['depositCount'],
            'Eth_1_Deposit_Root' : common.decode_public_key(slot_data['blockContainers'][0]['block']['block']['body']['eth1Data']['depositRoot'])
        }
        
        return common.send_sucess_msg(return_data)
    else:
        return common.send_error_msg()




def get_participation_rate():
    ''' 
        gives the global participation rate
    '''
    try:
        uri = '/eth/v1alpha1/validators/participation'
        url = base_url+uri
        response = http.request(
            'GET',
            url
        )
        if response.status == 200:
            data =  json.loads(response.data.decode('utf-8'))
            return data

    except Exception as e :
        print (e)
        pass