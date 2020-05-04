import sys, os

import mcs_protos
from server import util
from mcs_protos import grpc_server_math_interface, grpc_client_math_interface
from modules.math_servce import math_services_rpc

from util import custom_exception

mcs_services = util.McsServices(log='math_service_mcs')

class MathServicer(grpc_server_math_interface.MathServicer):
    def __init__(self):
        self.logger =  mcs_services.logger

    def send_mathLib_response(self,ret_val):
        self.logger.msg_logger('sending response {}'.format(ret_val))
        return grpc_client_math_interface.resp(
            result = ret_val
        )
    #calling calling rpc
    def MathLib(self, request, context):
        try:                
            a =  int(request.a)
            b =  int(request.b)
            operatoin = str(request.operation)

            self.logger.msg_logger('got request a = {} b = {} for {}'.format(a,b,operatoin))

            # #method 1
            # if operatoin == "add":
            #     ret_val = math_services_rpc.add(a,b)

            #method2
            ret_val = math_services_rpc.MathLib(a,b,operatoin)

            return self.send_mathLib_response(ret_val)
        except custom_exception.UserException as e:
            raise
        except Exception as e:
            error = util.get_error_traceback(sys, e)
            print (error)
            self.logger.error_logger(error)
            raise

