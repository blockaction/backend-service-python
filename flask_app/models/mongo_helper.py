from pymongo import MongoClient

def mongo_conn(): 
    try: 
        conn = MongoClient(host='127.0.0.1', port=27017) 
        return conn.beacon_chain
    except Exception as e: 
        print ("Mongo connection Error")

