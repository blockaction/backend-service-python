import grpc
import google

from mcs_protos import validator_pb2, validator_pb2_grpc
from google.protobuf import empty_pb2

def decode_public_key(data):
    validator_instance = validator_pb2.Validator()
    # serialized = validator_instance.SerializeToString(data.public_key)
    data_ = validator_instance.ParseFromString(data)
    return data_


    