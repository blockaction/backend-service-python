from .import third_party
from .import node
from client import client_beacon_chain
from flask_app import common 
from flask_app.models import mongo_helper
from flask_app.app_helper import time_calculator
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
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()





def get_validators_api(args):
    try:
        pageToken = args.get("page", "1")
        pageSize = args.get("perPage", "10")
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
                pk['effectiveBalance'] = float(pk.get('effectiveBalance')) / 1000000000
                data['validator'] = pk


            return common.send_sucess_msg(validators, **additional_data)
        
    except Exception as e:
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()
        

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
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()


def get_attestations(args):
    try:
        pageToken = args.get("page", "1")
        pageSize = args.get("perPage", "10")
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
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()


def get_validator_participation():
    try:

        db =  mongo_helper.mongo_conn()
        data = db.graph_data.find({}).limit(10)
        return_data = []
        for d in data :
            return_dict = {}
            return_dict['epoch'] =  d.get('epoch')
            return_dict['ether'] = d.get('ether')
            return_data.append(return_dict)

        return common.send_sucess_msg({'data':return_data})
    except Exception as e:
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()


# validator by Index
def get_validators_detail_by_index(index):
    '''
        Validator info  by index
    '''
    try:
        uri = '/eth/v1alpha1/validator'
        url = base_url+uri
        validators = http.request(
            'GET',
            url,
            fields={
                'index' : index           
            } 
        )
        
        if validators.status == 200:
            validators =  json.loads(validators.data.decode('UTF-8'))
            additional_data = {
                'publicKey' : common.decode_public_key(validators.get('publicKey')),
                'effectiveBalance' : str(int(validators.get('effectiveBalance'))/1000000000) + " ETH",
                'slashed' : validators.get('slashed'),
                'eligibilityEpoch' : validators.get('activationEligibilityEpoch'),
                'withdrawalCredentials' : validators.get('withdrawalCredentials'),
                'withdrawableEpoch' : validators.get('withdrawableEpoch'),
                'index' : index
                
            }

        pubkeyB64 = validators.get('publicKey')
        uri = '/eth/v1alpha1/validator/status'
        url = base_url+uri
        # pubkeyB64 = str(common.encode_pubic_key(pubkeyHex[2::]).decode('utf-8'))
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
                    'publicKey' : pubkeyB64
                } 
            )

            if response.status == 200:
                balance_data = response.data.decode('UTF-8')
                epoch = common.parse_dictionary(balance_data).get('epoch')
                balance_data = common.parse_dictionary(balance_data).get('balances')
                balance_data = balance_data[0]
                
                balance =  int(balance_data.get('balance'))/1000000000
                deposits_Received = int(balance_data.get('balance'))/1000000000
                deposits_Received = str(round(deposits_Received, 0)) +" ETH"
                index = balance_data.get('index')

                return_data['currentBalance'] = balance
                return_data['depositsReceived'] = deposits_Received
                return_data['index'] = index
                return_data['epoh'] = epoch
                return_data['totalIncome'] = round(balance%32,5)

            return common.send_sucess_msg(return_data, ** additional_data)
        else:
            return common.send_error_msg()

    except Exception as e:
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()



#Validator by Publickey
def get_validators_detail_by_public_key(pubkeyHex):
    '''
        Validator info  by Publick Key
    '''
    try:
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
                # 'eth1_DepositBlockNumber' : status_data.get('eth1DepositBlockNumber')
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
                epoch = common.parse_dictionary(balance_data).get('epoch')
                balance_data = common.parse_dictionary(balance_data).get('balances')
                balance_data = balance_data[0]
                
                balance =  int(balance_data.get('balance'))/1000000000
                deposits_Received = int(balance_data.get('balance'))/1000000000
                deposits_Received = str(round(deposits_Received, 0)) +" ETH"
                index = balance_data.get('index')

            uri = '/eth/v1alpha1/validator'
            url = base_url+uri
            validators = http.request(
                'GET',
                url,
                fields={
                    'index' : index           
                } 
            )
           
            if validators.status == 200:
                validators =  json.loads(validators.data.decode('UTF-8'))
                additional_data = {
                    'publicKey' : common.decode_public_key(validators.get('publicKey')),
                    'effectiveBalance' : str(int(validators.get('effectiveBalance'))/1000000000) + " ETH",
                    'slashed' : validators.get('slashed'),
                    'eligibilityEpoch' : validators.get('activationEligibilityEpoch'),
                    'withdrawalCredentials' : validators.get('withdrawalCredentials'),
                    'withdrawableEpoch' : validators.get('withdrawableEpoch')
                    
                }

                return_data['currentBalance'] = balance
                return_data['depositsReceived'] = deposits_Received
                return_data['index'] = index
                return_data['epoh'] = epoch
                return_data['totalIncome'] = round(balance%32,5)

            return common.send_sucess_msg(return_data, ** additional_data)
        else:
            return common.send_error_msg()

    except Exception as e:
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()

        
def searchable_data(data):
    try: 
        check_data = data[:2]
        if check_data == '0x':
            return get_validators_detail_by_public_key(data)

    except Exception as e:
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()


def get_epoch_data(epoch_number):
    try:
        epoch_state = client_beacon_chain.GetChainHead()
        if not epoch_state:
            raise
        finalized_epoch = int(epoch_state.finalized_epoch)

        if int(epoch_number) <= finalized_epoch:
            finnalized =  True
        else:
            finnalized = False


        uri = '/eth/v1alpha1/beacon/blocks'
        url = base_url+uri

        response = http.request(
            'GET',
            url,
            fields={
                'epoch' : str(epoch_number)           
            } 
        )        

        
        if response.status == 200:
            block_data_ = json.loads(response.data.decode('UTF-8')) 
            block_container = block_data_.get('blockContainers')

            epoch_time = time_calculator.get_epoch_time(int(epoch_number))
            return_list = []

            return_data = {
                'epoch' : epoch_number,
                'time' : epoch_time,
                'blocks' : {
                    'proposed' : len(block_container),
                    'skipped' : 32 - len(block_container)
                }
            } 
            deposit_count = 0
            voluntry_exit_count = 0
            attester_slashing_count = 0
            proposer_slashing_count = 0
            attestations_count = 0

            for single_block_data in block_container:
               
                block_data = single_block_data.get('block')
                block_detail = block_data.get('block')
                block_body = block_detail.get('body')

                deposit_count = deposit_count + len(block_body.get('deposits'))
                voluntry_exit_count = voluntry_exit_count + len(block_body.get('voluntaryExits'))
                attester_slashing_count =  attester_slashing_count + len(block_body.get('attesterSlashings'))
                proposer_slashing_count = proposer_slashing_count + len(block_body.get('proposerSlashings'))
                attestations_count = attestations_count + len(block_body.get('attestations'))


            return_data.update({
                'deposits' : deposit_count,
                'voluntay_exists' : voluntry_exit_count,
                'slashing' : {
                    'proposer_slashing' : proposer_slashing_count,
                    'attester_slashing' : attester_slashing_count
                },
                'attestations' : attestations_count
            })

        uri = '/eth/v1alpha1/validators/participation'
        url = base_url+uri
        if not finnalized:
            response = http.request(
                'GET',
                url
            )
        else:
            response = http.request(
                        'GET',
                        url,
                        fields={
                            'epoch' : epoch_number
                        }                         
                    )            


        if response.status == 200:
            data = json.loads(response.data.decode('UTF-8'))        
            return_data['finalized'] = data.get('finalized')            
            voted_ether = float(data.get('participation').get('votedEther')) / 1000000000
            participation_rate = float(data.get('participation').get('globalParticipationRate')) * 100
            eligible_ether = float(data.get('participation').get('eligibleEther'))/1000000000

        return_data.update({
            'voted_ether' : voted_ether,
            'participation_rate' : participation_rate,
            'eligible_ether' : eligible_ether
        })

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

            count = {
                'validator_count' : str(validators.get('totalSize'))
            }
            return_data.update(count)
        return common.send_sucess_msg(return_data)

        # else:
        #     return common.send_error_msg()

    except Exception as e:
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()




# data from slot Number

def get_slot_data(slot):
    try:
        '''
           retrives block by slot 
           A slot is a chance for a block to be added to the Beacon Chain and shards.
        '''
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
            block_container = slot_data.get('blockContainers')

            slot_time = time_calculator.get_slot_time(slot)
           
            
            if len(block_container) == 0 :
                epoch = get_epoch_by_slot(slot)

                return_data = [{
                    'status' : 'skipped',
                    'slot' : slot,
                    'epoch' : epoch,
                    'time' : slot_time
                }]

                return return_data

            return_list = []
            for single_block_data in block_container:
                return_data = {
                    'status' : 'proposed',
                    'time' : slot_time
                }
                return_data['block_root'] =  common.decode_public_key(single_block_data.get('blockRoot'))
                block_data = single_block_data.get('block')
               
                return_data['signature'] = common.decode_public_key(block_data.get('signature'))
                block_detail = block_data.get('block')

                return_data['parent_root'] = common.decode_public_key(block_detail.get('parentRoot'))
                return_data['proposer'] = block_detail.get('proposerIndex')
                return_data['slot'] = block_detail.get('slot')
                return_data['state_root'] = common.decode_public_key(block_detail.get('stateRoot'))
                block_body = block_detail.get('body')
                

                return_data['graffiti'] = {
                    'utf_8' : common.decode_bytes_utf8(block_body.get('graffiti')),
                    'hex' : common.decode_public_key(block_body.get('graffiti'))
                }
                return_data['randao_reveal'] = common.decode_public_key(block_body.get('randaoReveal'))
                return_data['deposits'] = len(block_body.get('deposits'))
                return_data['voluntaryExits'] = len(block_body.get('voluntaryExits'))

                return_data['slashing'] = {
                    'attester' : len(block_body.get('attesterSlashings')),
                    'proposer' : len(block_body.get('proposerSlashings'))
                }

                eth1_encoded_data = block_body.get('eth1Data')
                return_data['eth1_data'] = {
                    'block_hash' : common.decode_public_key(eth1_encoded_data.get('blockHash')),
                    'deposit_count' : eth1_encoded_data.get('depositCount'),
                    'deposit_root' : common.decode_public_key(eth1_encoded_data.get('depositRoot'))
                }

                return_data['attestations_count'] = len(block_body.get('attestations'))
                
                epoch = get_epoch_by_slot(slot)
                return_data['epoch'] = epoch

                return_list.append(return_data)

            return return_list
        else:
            return False

    except Exception as e:
        error = common.get_error_traceback(sys,e)
        print (error)
        return False



def get_attestion_by_slot(args):
    try:
        '''

        '''
        uri = '/eth/v1alpha1/beacon/blocks'
        url = base_url+uri
        response = http.request(
            'GET',
            url,
            fields={
                'slot' : args.get('slot')
            } 
        )

        if response.status == 200:
            slot_data = response.data.decode('UTF-8')
            slot_data = common.parse_dictionary(slot_data)

            block_container = slot_data.get('blockContainers')
            return_list = []
            for single_block_data in block_container:
                return_data = {

                }
                block_data = single_block_data.get('block')
                block_detail = block_data.get('block')
                return_data['slot'] = block_detail.get('slot')
                block_body = block_detail.get('body')
                
                attestians_data = block_body.get('attestations')
                return_data['attestations_count'] = len(attestians_data)

                attestian_list = []
                for single_attestation in attestians_data:
                    single_attestians_return_data = {

                    }
                    single_attestians_return_data['aggregationBits'] = single_attestation.get('aggregationBits')
                    single_attestians_return_data['signature'] = common.decode_public_key(single_attestation.get('signature'))

                    single_attestians_data = single_attestation.get('data')

                    single_attestians_return_data['beaconBlockRoot'] = common.decode_public_key(single_attestians_data.get('beaconBlockRoot'))
                    single_attestians_return_data['committeeIndex'] = single_attestians_data.get('committeeIndex')
                    single_attestians_return_data['source_epoch'] = single_attestians_data.get('source').get('epoch')
                    single_attestians_return_data['source_epoch_root'] = common.decode_public_key(single_attestians_data.get('source').get('root'))
                    single_attestians_return_data['target_epoch'] = single_attestians_data.get('target').get('epoch')
                    single_attestians_return_data['target_epoch_root'] = common.decode_public_key(single_attestians_data.get('target').get('root'))

                    attestian_list.append(single_attestians_return_data)
                
                return_data['attestian_detail'] = attestian_list


            return common.send_sucess_msg({'data': return_data})
        else:
            return common.send_error_msg()

    except Exception as e:
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()


def get_latest_block(args):
    '''gives data of latest block from db'''
    try :
        page = int(args.get('page', 1))
        perPage = int(args.get('perPage', 10))
        db_con = mongo_helper.mongo_conn()
        db_data = db_con.latest_block.find({}).sort([('_id',-1)]).limit(perPage)
        if not db_data:
            raise

        return_list = []
        for data in db_data:
            return_dict = {
                
            }
            return_dict['epoch'] = data.get('epoch','NA')
            return_dict['slot'] = data.get('slot','NA')
            if not (data.get('slot') == 'NA'):
                return_dict['time'] = time_calculator.get_slot_time(data.get('slot'))

            return_dict['proposer'] = data.get('proposer','N/A')
            return_dict['attestian_count'] = data.get('attestian_count','NA')
            return_dict['status'] = data.get('status','NA')
            return_list.append(return_dict)
        
        return common.send_sucess_msg({'data': return_list})
    except Exception as e:
        error = common.get_error_traceback(sys,e)
        print (error)
        return False


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
        error = common.get_error_traceback(sys,e)
        print (error)
        return common.send_error_msg()



def get_epoch_by_slot(slot):
    db = mongo_helper.mongo_conn()
    epoch_data = db.latest_block.find_one({'slot': int(slot)})
    if epoch_data:
        return epoch_data.get('epoch')
    else:
        epoch_data = db.latest_block.find_one({'slot': str(slot)})
        if epoch_data:
            return epoch_data.get('epoch')
        else:
            return 'NA'
            
