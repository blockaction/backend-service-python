import os, sys
import redis
from flask_app import common as common_util

def redis_connection():
    """
    Redis Connection
    """

    try:
        config = common_util.get_config()

        pool = redis.ConnectionPool(
            host=config.get('redis', 'host'),
            port=int(config.get('redis', 'port')),
            db=int(config.get('redis', 'db'))
        )

        redis_conn = redis.Redis(connection_pool=pool)

        # Check if the connection is up
        if redis_conn.ping():
            return redis_conn
        else:
            raise Exception('Redis Server is Down')

    except Exception as e:
        # error = common_util.get_error_traceback(sys, e)
        print (e)
        raise


def get_key(key):
    try:
        redis_conn = redis_connection()
        return redis_conn.get(key).decode('utf-8')
    except Exception as error:
        print (error)
        return False

def set_key(key, value):
    try:
        red_con = redis_connection()
        red_con.set(key, value)
        return True        
    except Exception as error :

        print (error)
        return False

def del_key(key):
    try:
        red_con = redis_connection()
        red_con.delete(key)
        return True        
    except Exception as e :
        print (error)
        return False

def hget(hash,key):
    try:
        red_con = redis_connection()
        value = red_con.hget(hash,key).decode('utf-8')
        return value
    except Exception as e :
        print (error)
        return False
