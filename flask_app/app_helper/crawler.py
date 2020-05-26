import os, sys
from os.path import dirname, join, abspath
import  requests
import ast 
import time 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import schedule

from flask_app import common
from flask_app.models import redis_helper



base_url = common.api()
config = common.get_config()

def crawl_chain_head():
    print ('Executing Crawler script....')
    try:
        uri = '/eth/v1alpha1/beacon/chainhead'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')
            data = ast.literal_eval(data)
            finalized_epoch = int(data.get('finalizedEpoch'))
            finalized_slot  = int(data.get('finalizedSlot'))
            
            crawled_slot = int(redis_helper.hget(
                hash= 'chain_head',
                key = 'finalizedSlot'
            ))
            print('crawled slot is {} finalized slot is {}'.format(crawled_slot,finalized_slot))
            if crawled_slot < finalized_slot:
                print ('processing redis operation.........')
                redis_set_slot = redis_helper.hset(
                    key_hash = 'chain_head',
                    key = 'finalizedSlot',
                    value = finalized_slot
                )

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
            else:
                print ('skipping redis operation')
        else:
            print ('No Response from Blockchain')
    except Exception as e:
        error =  common.get_error_traceback(sys, e)
        print (error)


schedule.every(8).seconds.do(crawl_chain_head)


while True:
    print ("*"*30)
    print ('Running python shedular for blockchain crawler')
    schedule.run_pending()
    time.sleep(2)