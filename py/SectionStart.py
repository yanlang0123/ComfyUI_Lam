import time
import numpy as np
import base64
import uuid
import torch
import json
import comfy.model_management
import redis
from redis.exceptions import RedisError
from .src.wechat.config import Config
from .src.wechat.redisSub import r
from .src.utils.chooser import ChooserMessage
class SectionStart:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        sectionServers=['default']
        if r:
            keys=r.keys('sectionheartbeat:*')
            for key in keys:
                channel=key.replace('sectionheartbeat:','')
                sectionServers.append(channel)
        return {
            "required": {
                "server": (sectionServers, ),
            },
            "optional": {
                "images": ("IMAGE", ),
            },
            "hidden": {
                "sectype": ("INT", {}),
                "data": ("STRING", {}),
                "unique_id": "UNIQUE_ID",           #节点编号
            }
        }
    RETURN_TYPES = ("SECTION","IMAGE",)
    FUNCTION = "blank_image"

    CATEGORY = "lam"

    def blank_image(self,server,images=None, sectype=0,data='',unique_id=""):
        if sectype==0:
            if server=='default':
                return (None,images, )
            else:
                if Config().cluster==None or len(Config().redis.keys())<=0:
                    raise Exception("redis未配置")
                pool = redis.ConnectionPool(host=Config().redis['host'], port=Config().redis['port'],password=Config().redis['password'], db=0, decode_responses=True )#password="xxxxx"
                rc = redis.Redis(connection_pool=pool)
                dataObj=json.loads(data)
                prompt=dataObj['prompt']
                fileKey=str(uuid.uuid4())
                if images!=None:
                    arr=np.clip(255. * images.cpu().numpy(), 0, 255).astype(np.uint8)
                    arrStr=base64.b64encode(arr.tobytes()).decode("utf-8")
                    rc.setex(fileKey, 15, arrStr)
                    prompt[unique_id]['inputs']['data']=json.dumps({"sectype":sectype,"fileKey":fileKey,'shape':arr.shape})
                    prompt[unique_id]['inputs']['sectype']=1
                    prompt[unique_id]['inputs'].pop('images', None)
                else:
                    prompt[unique_id]['inputs']['data']=json.dumps({"sectype":sectype,"fileKey":fileKey})
                    prompt[unique_id]['inputs']['sectype']=1
                    prompt[unique_id]['inputs'].pop('images', None)
                rc.publish(server,json.dumps({'event':'addTask','data':dataObj}))
                while not (unique_id in ChooserMessage.messages) and not ("-1" in ChooserMessage.messages):
                    if ChooserMessage.cancelled:
                        rc.publish(server,json.dumps({'event':'sectionDone','data':{'id':unique_id,'message':'__cancel__'}}))
                        raise comfy.model_management.InterruptProcessingException()
                    time.sleep(0.5)
                rc.close()
                pool.close()
                return ({"sectype":sectype,"fileKey":fileKey,"server":server},images, )
        else:
            if server=='default':
                raise Exception("参数类型异常")
            dataObj=json.loads(data)
            fileKey=dataObj['fileKey']
            if fileKey=='':
                raise Exception("文件不能为空")
            if Config().cluster==None or len(Config().redis.keys())<=0:
                raise Exception("redis未配置")
            pool = redis.ConnectionPool(host=Config().redis['host'], port=Config().redis['port'],password=Config().redis['password'], db=0, decode_responses=True )#password="xxxxx"
            rc = redis.Redis(connection_pool=pool)
            if 'shape' in dataObj:
                shape=dataObj['shape']
                imgStr=rc.get(fileKey)
                decoded = np.frombuffer(base64.b64decode(imgStr), dtype=np.uint8)
                result=decoded.reshape(shape)
                images=torch.from_numpy(np.array(result).astype(np.float32) / 255.0)
                rc.delete(fileKey)
            mainPath=rc.get('mainPath')
            if mainPath==None:
                raise Exception("主服务不存在")
            rc.publish(mainPath,json.dumps({'event':'sectionDone','data':{'id':unique_id,'message':1}}))
            rc.close()
            pool.close()
            return ({"sectype":sectype,"fileKey":fileKey},images, )
            
            

NODE_CLASS_MAPPINGS = {
    "SectionStart": SectionStart
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "SectionStart": "分段负载开始"
}
