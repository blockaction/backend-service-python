import requests
from flask_app import common
import ast
from flask_app import common
from flask_app.models import mongo_helper
from datetime import datetime 


base_url = common.api()

def get_current_ethereum_price():
    api = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,JPY,EUR?1eef1b3afe86c87ccb9b43f6a7ed8c4483fc5076e99b0f8cecfcae04f054ec75'
    response = requests.get(api)
    if response.status_code == 200:
        data =  common.parse_dictionary(response.content.decode('UTF-8'))    
        price = data.get('USD')
        return price
    else:
        return ('error in parsing eth price')


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
        return common.send_error_msg()


def get_current_slot():
    try:    
        uri = '/eth/v1alpha1/beacon/chainhead'
        url = base_url+uri
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('UTF-8')    
            data = ast.literal_eval(data)
            return int(data.get('finalizedSlot'))
    except Exception as e:
        print (e)
        return common.send_error_msg()

def send_current_eth_price():
    price = get_current_ethereum_price()
    return common.send_sucess_msg({'price' :price})



def get_data_for_global_participation_rate():
    try:
        db_con = mongo_helper.mongo_conn()
        db_data = db_con.global_participation.find({}).sort([('_id',1)]).limit(24)

        timestamp_list = []
        voted_ether_list = []
        global_participation_list = []

        for data in db_data:
            ether = int(data.get('voted_ether'))/1000000000
            timestamp_list.append(data.get('timestamp'))
            voted_ether_list.append(ether)
            global_participation_list.append(round(data.get('global_participation')*100,2))

        return_dict = {
            'timestamp' : timestamp_list,
            'voted_ether' : voted_ether_list,
            'global_participation' : global_participation_list
        }
        return common.send_sucess_msg(return_dict)

    except Exception as e :
        print (e)
        pass


def get_vol_data():
    time = args.get("time", "")
    url = 'https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=' +time
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        data =  common.parse_dictionary(data)

        total_volumes = data['total_volumes']
        count = len(total_volumes)

        usdPrice = []
        marketcapValue =[]
        dateTime = []
        marketVolume = []

        for x in range(count):
            timestamp = total_volumes[x][0]
            usdvalue = data['prices'][x][1]
            capvalue = data['market_caps'][x][1]
            volume = data['total_volumes'][x][1]

            dt_object = datetime.fromtimestamp(timestamp/1000) 
            t = dt_object.strftime('%a,%b %d %Y,%H:%M')
            
            dateTime.append(t)
            usdPrice.append(usdvalue)
            marketcapValue.append(capvalue)
            marketVolume.append(volume)

        return_data = {
            'dateTime' : dateTime,
            'volumeUsd' : marketVolume,
            'marketCapValue' : marketcapValue,
            'prices' : usdPrice
        
        }
        return  common.send_sucess_msg(return_data)
    else:
        return  common.send_error_msg()
