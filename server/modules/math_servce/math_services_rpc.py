import sys
from util import custom_exception, mcs_common
from .import math_servicer

def add(a,b):
    return a+b

def mul(a,b):
    return a*b

def MathLib(a: int,b: int,operation: str) -> int:
    try:
        if operation == "add":
            return add(a,b)
        elif operation == "mul":
            return add(a,b)
        
        

    except custom_exception.UserException as e:
        raise e

    except Exception as e:
        error = mcs_common.get_error_traceback(sys, e)
        print (error)
        raise e    