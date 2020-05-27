import os, sys
from os.path import dirname, join, abspath
import  requests
import ast 
import time 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import schedule

from flask_app import common,beacon
from flask_app.models import redis_helper, mongo_helper



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
            current_epoch = int(data.get('headEpoch'))
            current_slot  = int(data.get('headSlot'))
            
            crawled_slot = int(redis_helper.hget(
                hash= 'chain_head',
                key = 'current_slot'
            ))
            print('crawled slot is {} current slot is {}'.format(crawled_slot,current_slot))
            if crawled_slot < current_slot:
                print ('processing redis operation.........')
                redis_set_slot = redis_helper.hset(
                    key_hash = 'chain_head',
                    key = 'current_slot',
                    value = current_slot
                )

                crawled_epoch = int(redis_helper.hget(
                    hash= 'chain_head',
                    key = 'current_epoch'
                ))
                
                if crawled_epoch < current_epoch:
                    redis_set_epoch = redis_helper.hset(
                        key_hash = 'chain_head',
                        key = 'current_epoch',
                        value = current_epoch
                    )
                slot_data = beacon.get_slot_data(current_slot)[0]
                attestian_count = slot_data.get('attestations_count', '0')
                proposer = slot_data.get('proposer', 'NA')

                status = 'proposed'

                if slot_data.get('status') == 'skipped':
                    status = 'skipped'

                print ('processing_db operation')

                db_conn = mongo_helper.mongo_conn()
                db_status = db_conn.latest_block.insert({
                    'epoch' : str(current_epoch),
                    'slot' : str(current_slot),
                    'proposer' : proposer,
                    'attestian_count' : attestian_count,
                    'status' : status
                })
                print (db_status)

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


crawl_chain_head()