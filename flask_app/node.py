import requests
from flask_app import common
base_url = "https://api.prylabs.net"
headers = {
    'accept': 'application/json',
}


# from client import 
def node_peers():
    uri = '/eth/v1alpha1/node/peers'
    url = base_url+uri
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('UTF-8')
        return common.parse_dictionary(data)