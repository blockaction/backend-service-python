import os, sys
from os.path import dirname, join, abspath
import  requests
import ast 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from flask_app import common
from flask_app.models import redis_helper


base_url = common.api()
config = common.get_config()

def crawl_chain_head():
    try:
        uri = '/eth/v1alpha1/beacon/chainhead'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            data = ast.literal_eval(data)
            finalized_epoch = int(data.get('finalizedEpoch'))
            finalized_slot  = int(data.get('finalizedSlot'))
            
            crawled_epoch = int(redis_helper.hget(
                hash= 'chain_head',
                key = 'finalizedEpoch'
            ))
            
            if crawled_epoch < finalized_epoch:
                redis_set_epoch = redis_helper.hset(
                    key_hash = 'chain_head',
                    key = 'finalizedEpoch',
                    value = finalized_epoch
                )

            crawled_slot = int(redis_helper.hget(
                hash= 'chain_head',
                key = 'finalizedSlot'
            ))
            if crawled_slot < finalized_slot:
                redis_set_slot = redis_helper.hset(
                    key_hash = 'chain_head',
                    key = 'finalizedSlot',
                    value = finalized_slot
                )                
 
    except Exception as e:
        print (e)
        return False



crawl_chain_head()
