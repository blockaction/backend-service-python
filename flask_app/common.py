import os, sys
from flask import jsonify
import ast 
import base64
import re
import configparser
from datetime import datetime


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.curdir))
conf_file_path = BASE_DIR+'/configuration.ini'
config = configparser.ConfigParser()
config.read(conf_file_path)

def get_config():
    return config


def api():
    # base_url = "https://api.prylabs.net"
    base_url = 'http://3.94.76.3:4001'
    return base_url


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



def decode_public_key(pubkeyB64):
    '''
        decode base64 to hex format
    '''
    pubkeyBytes = base64.b64decode(pubkeyB64)
    pubkeyHex = pubkeyBytes.hex()   
    return '0x'+pubkeyHex


def encode_pubic_key(pubkeyHex):
    ''' 
        encode hex key to base64 pubkey
    '''
    pubkeybytes = bytes.fromhex(pubkeyHex)
    pubkeyB64  = base64.b64encode(pubkeybytes)
    return pubkeyB64

def get_current_epoch():
    try:    
        uri = '/eth/v1alpha1/beacon/chainhead'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            data = ast.literal_eval(data)
            return int(data.get('finalizedEpoch'))
    except Exception as e:
        print (e)
        return False

def get_current_date_time():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string 

