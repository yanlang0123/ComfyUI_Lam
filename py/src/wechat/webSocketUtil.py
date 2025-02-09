import websocket
import uuid
import threading
import time
import json
import requests
import urllib
import folder_paths
import os
from .config import Config

class WebSocketClient(threading.Thread):
    def __init__(self, server_address, messageFunc=None):
        super().__init__()
        self.server_address = server_address
        self.client_id=str(uuid.uuid4())
        self.ws = websocket.WebSocket()
        self.messageFunc = messageFunc
        self.queue_remaining=0
        self.cliDict={}
        self.is_connected=False
        
    def handle_message(self, data):
        if self.messageFunc != None:
            self.messageFunc(self.server_address, data)
            
    def setMainServer(self):
        p = {"mainPath": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req =  requests.post("http://{}/wechatauth/setMainServer".format(self.server_address), data=data)
        print("返回状态码：",req.status_code)
        if req.status_code==200:
            self.is_connected=True
        
    def setSubscribe(self,json_data):
        if json_data['event']=='addTask':
            self.cliDict[json_data['data']['prompt_id']]=json_data['data']['client_id']
            json_data['data']['client_id']=self.client_id
        data = json.dumps(json_data).encode('utf-8')
        req =  requests.post("http://{}/wechatauth/setSubscribe".format(self.server_address), data=data)
        print("返回状态码：",req.status_code)
        return req.status_code==200
    
    def output(self,node_output):
        if 'images' in node_output:
            for image in node_output['images']:
                image['filename']=self.dowFile(image)
        elif 'gifs' in node_output:
            for image in node_output['gifs']:
                image['filename']=self.dowFile(image)
    def dowFile(self,data):
        if data['type']=="temp":
            output_dir = folder_paths.get_temp_directory()
        else:
            output_dir = folder_paths.get_output_directory()
        if 'subfolder' in data and data['subfolder']:
            file_path=os.path.join(output_dir,data['subfolder'],self.client_id+data['filename'])
        else:
            file_path=os.path.join(output_dir,self.client_id+data['filename'])
        url_values = urllib.parse.urlencode(data)
        with requests.get("http://{}/view?{}".format(self.server_address, url_values)) as response:
            open(file_path,'wb').write(response.content)

        return self.client_id+data['filename']

    def restart(self):
        url="ws://{}/ws?clientId={}".format(self.server_address, self.client_id)
        self.ws.connect(url)
        self.setMainServer()
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if 'type' in message:
                    message['event']=message['type']
                if 'event' in message:
                    if message['event'] in ['crystools.monitor']:
                        continue
                    if message['event'] == 'status':
                        self.queue_remaining=message['data']['status']['exec_info']['queue_remaining']
                    elif message['event']=='executed':
                        self.output(message['data']['output'])
                if 'data' in message and 'promptId' in message['data']:
                    message['sid']=self.cliDict[message['data']['promptId']]
                else:
                    message['sid']=None
                message['port']=self.server_address
                self.handle_message(message)
    def run(self):
        while True:
            try:
                self.restart()
            except Exception as e:
                self.is_connected=False
                time.sleep(2)
                print(f'websocket异常:{e},稍后重连')

