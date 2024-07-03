import redis
from threading import Thread, current_thread
from comfy.cli_args import args
from .config import Config
from redis.exceptions import RedisError
r=None
def connect_redis():
    global r
    if len(Config().redis.keys())>0:
        print('连接redis')
        # 尝试连接Redis
        try:
            pool = redis.ConnectionPool(host=Config().redis['host'], port=Config().redis['port'],password=Config().redis['password'], db=0, decode_responses=True )#password="xxxxx"
            r = redis.Redis(connection_pool=pool)
        except RedisError as e:
            print(f"连接失败: {e}")
            r = None
    return r

connect_redis()
def run_with_reconnect(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except RedisError as e:
                print(f"重连: {e}")
                r=connect_redis()
                if r is None:
                    return
 
    return wrapper

class PubSub(object):
    def __init__(self):
        if r:
            self.pub = r.pubsub()

    def subscribe(self, *args):
        if r:
            self.pub.subscribe(*args)
            self.pub.parse_response()
            return self.pub
        else:
            return None

