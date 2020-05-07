import os
from flask import jsonify
import ast 
import base64
import re

def send_error_msg(): 
    return jsonify({'error_msg':'no response from Prysm api'}), 505

def parse_dictionary(data):
    return (ast.literal_eval(data))    


def send_sucess_msg(response,**kwargs):
    try:
        if not type(response) ==  dict:
            response = parse_dictionary(response)
        response['message'] = 'Sucess'
        for k,v in kwargs.items():
            response[k] =  v
        return jsonify(response), 200
    except Exception as e:
        print (e)



def get_error_traceback(sys, e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return "%s || %s || %s || %s" %(exc_type, fname, exc_tb.tb_lineno,e)




# def decode_public_key(pk):

    
#     pk =  pk.encode('ascii')
#     if type(pk) == 'bytes':
#         pk = base64.decodebytes(pk)
#         return pk
#     else:
#         pk = base64.decodestring(pk)
#         t = type(pk)
#         return pk



import binascii

def decode_public_key(data_, altchars=b'+/'):
    hex_data = binascii.hexlify(data_)
    data = binascii.a2b_base64(hex_data)

    print (data)

