import requests
from flask_app import common
import ast 

base_url = "https://api.prylabs.net"
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