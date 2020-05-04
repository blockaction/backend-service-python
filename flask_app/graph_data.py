import requests 
import models
import common
import json 

base_url = "https://api.prylabs.net"
uri = '/eth/v1alpha1/validators/participation'

url = base_url+uri
response  = requests.get(url)
if response.status_code == 200:
    data = json.loads(response.content.decode('UTF-8'))
    
    epoch = str(data.get('epoch'))
    voted_ether = int(data.get('participation').get('votedEther'))/1000000000
    store_data = {
        'epoch': epoch+' Epoch',
        'ether': voted_ether
    }
    db_con = models.mongo_conn()
    db_con.graph_data.insert(store_data)
