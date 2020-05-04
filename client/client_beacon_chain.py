import grpc
import google

from mcs_protos import beacon_chain_pb2, beacon_chain_pb2_grpc
from google.protobuf import empty_pb2

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
            return response.validator_list
    except Exception as e:
        return False
    