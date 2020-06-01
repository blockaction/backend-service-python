import os, sys
from os.path import dirname, join, abspath
import  requests
import ast 
import time 
import requests 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from client  import client_beacon_chain
import json
import schedule
import arrow 
from flask_app import common,beacon
from flask_app.models import redis_helper, mongo_helper
# import datetime
from datetime import datetime,timezone


import urllib3
http = urllib3.PoolManager()

def get_slot_time(slot):
    genesis_epoch = int(common.genesis_time())
    blockchain_slot_time = genesis_epoch+(int(slot)*12)
    blockchain_slot_time_utc = datetime.utcfromtimestamp(blockchain_slot_time).strftime("%Y-%m-%dT%H:%M:%SZ")
    return blockchain_slot_time_utc


def get_epoch_time(epoch):
    genesis_epoch = int(common.genesis_time())
    blockchain_epoch_time = genesis_epoch+(int(epoch)*384)
    blockchain_epoch_time_utc = datetime.utcfromtimestamp(blockchain_epoch_time).strftime("%Y-%m-%dT%H:%M:%SZ")
    return blockchain_epoch_time_utc


def get_genesis_time():
    base_url = common.api()
    uri  = '/eth/v1alpha1/node/genesis'    
    url = base_url+ uri
    response =  http.request(
        'GET',
        url
    )
    if response.status == 200:
        response =  json.loads(response.data.decode('UTF-8'))
        genesis_time = response.get('genesisTime')
        genesis_datetime_ = datetime.strptime(genesis_time,"%Y-%m-%dT%H:%M:%SZ")
        genesis_epoch = arrow.get(genesis_datetime_).timestamp    

        return genesis_epoch

