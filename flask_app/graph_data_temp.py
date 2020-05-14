import os, sys
from os.path import dirname, join, abspath

import requests 
import models
import common
import json 
import datetime
import schedule
import time


sys.path.insert(0, abspath(join(dirname(__file__), '../')))

from flask_app import beacon
from flask_app.models import redis_helper,mongo_helper

base_url = common.api()





def global_participation_temp():
    print ("#"*30)
    print("Executing global_participation_script")
    data = beacon.get_participation_rate()
    if data:
        participation = data.get('participation')
        insert_data = {
            'epoch' : data.get('epoch'),
            'voted_ether' : participation.get('votedEther'),
            'global_participation' : participation.get('globalParticipationRate'),
            'eligible_ether' : participation.get('eligibleEther'),
            'timestamp' : common.get_current_date_time()
        }
        db_con = mongo_helper.mongo_conn()
        db_status = db_con.global_participation_temp.insert(insert_data)
        print (db_status)
    else:
        False

schedule.every(1).minutes.do(global_participation_temp)

while True:
    print ("*"*30)
    print ('Running python shedular for graph data')
    schedule.run_pending()
    time.sleep(10)