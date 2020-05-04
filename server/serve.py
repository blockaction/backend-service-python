import os, sys
from os.path import dirname, join, abspath
import time
import grpc
from concurrent import futures

sys.path.insert(0, abspath(join(dirname(__file__), '../')))


import util
import modules.math_servce
from modules.math_servce import math_servicer as math_servce_util
# from mcs_protos import grpc_server_math_interface
from mcs_protos import beacon_chain_pb2_grpc


def serve_math_service_mcs():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # math_servce_util.mcs_services.create_logger()
    logger = math_servce_util.mcs_services.logger
    try:
        print ("******** serve math grpc service ********")
        
        while True:
            math_servicer = math_servce_util.MathServicer()
        
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

            grpc_server_math_interface.add_MathServicer_to_server(
                math_servicer, server
            )

            server.add_insecure_port('[::]:50051')
            print ("grpc listning at port 50051...")
            logger.msg_logger("grpc listning at port 50051...")
            server.start()
            server.wait_for_termination()
            time.sleep(86400)

    except util.custom_exception.UserException as e:
        logger.error_logger('user exception at serve_transaction mcs %s : ' % e)
        return

    except Exception as e:
        server.stop(0)
        error = util.mcs_common.get_error_traceback(sys, e)
        print (error)
        logger.error_logger('server transaction mcs error : %s ' % error)
        return

def serve_beacon_chain():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    try:
        while True:
            beacon_chain = beacon_servce_util.BeaconServicer()
        
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

            grpc_server_beacon_interface.add_BeaconServicer_to_server(
                math_servicer, server
            )

            server.add_insecure_port('[::]:50051')
            print ("grpc listning at port 50051...")
            logger.msg_logger("grpc listning at port 50051...")
            server.start()
            server.wait_for_termination()
            time.sleep(86400)

    except util.custom_exception.UserException as e:
        logger.error_logger('user exception at serve_transaction mcs %s : ' % e)
        return

    except Exception as e:
        server.stop(0)
        error = util.mcs_common.get_error_traceback(sys, e)
        print (error)
        logger.error_logger('server transaction mcs error : %s ' % error)
        return

if __name__ == '__main__':
    serve_math_service_mcs()