import redis
from threading import Thread, current_thread
from comfy.cli_args import args
from .config import Config
from redis.exceptions import RedisError
import time
r=None
def connect_redis():
    global r
    if Config().cluster and 'redis'==Config().cluster["clusterType"] and len(Config().redis.keys())>0:
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

class RedisSubscriber:
    def __init__(self, channel='mychannel',messageFunc=None):
        #设置socket_keepalive参数，以确保TCP连接不会因为长时间空闲而被关闭
        self.channel = channel
        self.messageFunc=messageFunc
        self.restart()
        self.pubsub.subscribe(self.channel)
        
    def restart(self):
        self.redis_client = redis.StrictRedis(host=Config().redis['host'], port=Config().redis['port'], 
                password=Config().redis['password'], db=0,
                socket_keepalive=True,socket_connect_timeout=999999)
        self.pubsub = self.redis_client.pubsub()
    def listen(self):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                self.handle_message(message['data'])
 
    def handle_message(self, data):
        #print(f"Received message: {data}")
        if self.messageFunc!=None:
            self.messageFunc(self.redis_client,data)
 
    def reconnect(self):
        self.pubsub.unsubscribe()
        self.pubsub.subscribe(self.channel)
 
    def run(self):
        while True:
            try:
                self.listen()
            except redis.exceptions.ConnectionError:
                print("Connection to Redis lost. Attempting to reconnect...")
                time.sleep(2)  # Wait 5 seconds before retrying
                self.reconnect()
            except redis.exceptions.TimeoutError:
                print("Timeout error occurred. Attempting to reconnect...")
                time.sleep(2)  # Wait 5 seconds before retrying
                self.restart()
                self.reconnect()

            


