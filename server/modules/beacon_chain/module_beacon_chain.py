import sys, os
import mcs_protos
from server import util
from util import custom_exception
from mcs_protos import beacon_chain_pb2, beacon_chain_pb2_grpc

mcs_services = util.McsServices(log='math_service_mcs')


class BeaconServicer(beacon_chain_pb2_grpc.BeaconChainServicer):
    def __init__(self):
        pass 
    