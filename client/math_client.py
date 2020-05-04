

import random 
import sys, os
import time
import grpc

from mcs_protos import grpc_client_math_interface, grpc_server_math_interface

allowed_operation = "add , mul, sub"

def prepare_data():
    data =  grpc_client_math_interface.param(
        a = 2,
        b = 6,
        operation = 'add'
    )
    return data

def send_request(stub):
    responses = stub.MathLib(prepare_data())
    print(responses)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = grpc_server_math_interface.MathStub(channel)
        print("-------------- grpc maths client service --------------")
        send_request(stub)



if __name__ == '__main__':
    run()

			