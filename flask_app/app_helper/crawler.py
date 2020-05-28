import os, sys
from os.path import dirname, join, abspath
import  requests
import ast 
import time 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from client  import client_beacon_chain

import schedule

from flask_app import common,beacon
from flask_app.models import redis_helper, mongo_helper



base_url = common.api()
config = common.get_config()

def crawl_chain_head():
    print ('Executing Crawler script....')
    try:
        for chain_head_data in  client_beacon_chain.getChainHeadStream():
            current_epoch = int(chain_head_data.get('headEpoch'))
            current_slot  = int(chain_head_data.get('headSlot'))
            
            crawled_slot = int(redis_helper.hget(
                hash= 'chain_head',
                key = 'current_slot_'
            ))
            print('crawled slot is {} current slot is {}'.format(crawled_slot,current_slot))

            if crawled_slot < current_slot:
                diffrence = current_slot - crawled_slot

                if diffrence > 1 :
                    #case of skipped block
                    print ('processing skipped block')
                    for i in range(diffrence -1):
                        crawled_slot = crawled_slot + 1

                        print ('processing skipped block: {} '.format(crawled_slot))

                        db_conn = mongo_helper.mongo_conn()
                        db_status = db_conn.latest_block.insert({
                            'epoch' : int(current_epoch),
                            'slot' : int(crawled_slot),
                            'proposer' : 'NA',
                            'attestian_count' : 0,
                            'status' : 'Skipped'
                        })
                        print (db_status)
     
                print ('processing redis operation.........')
                redis_set_slot = redis_helper.hset(
                    key_hash = 'chain_head',
                    key = 'current_slot_',
                    value = current_slot
                )

                crawled_epoch = int(redis_helper.hget(
                    hash= 'chain_head',
                    key = 'current_epoch_'
                ))
                
                if crawled_epoch < current_epoch:
                    redis_set_epoch = redis_helper.hset(
                        key_hash = 'chain_head',
                        key = 'current_epoch_',
                        value = current_epoch
                    )
                slot_data = beacon.get_slot_data(current_slot)[0]
                attestian_count = slot_data.get('attestations_count', '0')
                proposer = slot_data.get('proposer', 'NA')

                print ('processing_db operation')

                db_conn = mongo_helper.mongo_conn()
                db_status = db_conn.latest_block.insert({
                    'epoch' : str(current_epoch),
                    'slot' : str(current_slot),
                    'proposer' : proposer,
                    'attestian_count' : attestian_count,
                    'status' : 'proposed'
                })
                print (db_status)

            else:
                print ('skipping redis operation')
        else:
            print ('No Response from Blockchain')
    except Exception as e:
        error =  common.get_error_traceback(sys, e)
        print (error)




crawl_chain_head()
