from os.path import dirname, join, abspath
import mcs_common
import configparser
from mcs_common import get_error_traceback
from mcs_common.services import custom_exception

ROOT_DIR = abspath(dirname(__file__))

conf_file_path = ROOT_DIR+'/configuration.ini'
env = configparser.RawConfigParser()
env.read(conf_file_path)

def get_env():
    return env


class McsServices:
    def __init__(self, log):
        self.obj_common = mcs_common.CommonUtil(log=log, env=env)
        self.obj_common.create_logger()

        self.logger = self.obj_common.logger

        self.db = self.obj_common.db_init(
            database = 'mongo',  #accepted mongo/mysql/psql
            host=env.get('mongo', 'host'),
            user=env.get('mongo', 'user'),
            password=env.get('mongo', 'passwd'),
            db_name=env.get('mongo', 'db_name'),
            port=env.get('mongo', 'port')
        ) 

        self.redis = self.obj_common.redis_init(
            host = env.get('redis', 'host'),
            port = env.get('redis', 'port'),
            db = env.get('redis', 'db')
        )

    def create_logger(self):
        self.obj_common.create_logger()
        self.logger = self.obj_common.logger
    