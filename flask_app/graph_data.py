import os, sys
from os.path import dirname, join, abspath

import requests 
import models
import common
import json 
import datetime


sys.path.insert(0, abspath(join(dirname(__file__), '../')))

from flask_app import beacon
from flask_app.models import redis_helper,mongo_helper

base_url = common.api()

# uri = '/eth/v1alpha1/validators/participation'

# url = base_url+uri
# response  = requests.get(url)
# if response.status_code == 200:
#     data = json.loads(response.content.decode('UTF-8'))
    
#     epoch = str(data.get('epoch'))
#     voted_ether = int(data.get('participation').get('votedEther'))/1000000000
#     store_data = {
#         'epoch': epoch+' Epoch',
#         'ether': voted_ether
#     }
#     db_con = models.mongo_conn()
#     db_con.graph_data.insert(store_data)


def global_participation_script():
    data = beacon.get_participation_rate()
    if data:
        participation = data.get('participation')
        insert_data = {
            'voted_ether' : participation.get('votedEther'),
            'global_participation' : participation.get('globalParticipationRate'),
            'eligible_ether' : participation.get('eligibleEther'),
            'timestamp' : common.get_current_date_time()
        }    
        db_con = mongo_helper.mongo_conn()
        db_status = db_con.global_participation.insert(insert_data)
        print (db_status)
    else:
        False


global_participation_script()