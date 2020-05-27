import os, sys
from os.path import dirname, join, abspath

import requests 

import json 
import datetime
import schedule
import time


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from flask_app import beacon, common
from  flask_app.models import redis_helper,mongo_helper

base_url = common.api()



def global_participation_script():
    try:
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
            db_status = db_con.global_participation.insert(insert_data)
            print (db_status)
        else:
            False

    except Exception as e:
        error =  common.get_error_traceback(sys,e)
        print (error)


schedule.every().hour.do(global_participation_script)

while True:
    print ("*"*30)
    print ('Running python shedular for graph data')
    schedule.run_pending()
    time.sleep(10)