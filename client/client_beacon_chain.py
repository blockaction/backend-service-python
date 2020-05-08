import grpc
import google

from mcs_protos import beacon_chain_pb2, beacon_chain_pb2_grpc
from google.protobuf import empty_pb2
from client import client_validators

def get_empty_data():
    return empty_pb2.Empty(

    )

def GetChainHead():
    try:    
        with grpc.insecure_channel('54.243.16.45:4000') as channel:
            stub = beacon_chain_pb2_grpc.BeaconChainStub(channel)
            response = stub.GetChainHead(get_empty_data())
            return response
    except Exception as e:
        raise e
        return False


def list_validators():
    try:    
        with grpc.insecure_channel('54.243.16.45:4000') as channel:
            stub = beacon_chain_pb2_grpc.BeaconChainStub(channel)
            response = stub.ListValidators(
                beacon_chain_pb2.ListValidatorsRequest(
                    epoch = 3003,
                    page_size = 100
                )
            )
            # return response.validator_list
            isntance = beacon_chain_pb2.Validators()
            response_ = isntance.SerializeToString(response)

            isntance.ParseFromString(response)
            print (isntance)
            # vl= response.validator_list[0].validator

            # print (type(vl))
            # a = client_validators.decode_public_key(vl)
            # print (a)
            # return a
            # vl= response.validator_list

    except Exception as e:
        return False
    

