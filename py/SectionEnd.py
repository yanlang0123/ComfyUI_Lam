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
import pickle
from .src.utils.chooser import ChooserMessage
class SectionEnd:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "section": ("SECTION", ),
                "images": ("IMAGE", ),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",           #节点编号
            }
        }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "blank_image"
    OUTPUT_NODE = True
    CATEGORY = "lam"

    def blank_image(self,section,images,unique_id=''):
        if section is None:
            return (images, )
        if section['sectype']==1:
            if Config().cluster==None or len(Config().redis.keys())<=0:
                raise Exception("redis未配置")
            pool = redis.ConnectionPool(host=Config().redis['host'], port=Config().redis['port'],password=Config().redis['password'], db=0, decode_responses=True )#password="xxxxx"
            rc = redis.Redis(connection_pool=pool)
            arr=np.clip(255. * images.cpu().numpy(), 0, 255).astype(np.uint8)
            arrStr=base64.b64encode(arr.tobytes()).decode("utf-8")
            fileKey=section['fileKey']
            rc.setex(fileKey, 15, arrStr)
            serialized_tuple = ','.join([str(x) for x in arr.shape])
            rc.setex(fileKey+"_shape",15,serialized_tuple)
            mainPath=rc.get('mainPath')
            if mainPath==None:
                raise Exception("主服务不存在")
            rc.publish(mainPath,json.dumps({'event':'sectionDone','data':{'id':unique_id,'message':1}}))
            rc.close()
            pool.close()
            return (images, )
        else:
            fileKey=section['fileKey']
            server=section['server']
            if Config().cluster==None or len(Config().redis.keys())<=0:
                raise Exception("redis未配置")
            pool = redis.ConnectionPool(host=Config().redis['host'], port=Config().redis['port'],password=Config().redis['password'], db=0, decode_responses=True )#password="xxxxx"
            rc = redis.Redis(connection_pool=pool)    
            while not (unique_id in ChooserMessage.messages) and not ("-1" in ChooserMessage.messages):
                if ChooserMessage.cancelled:
                    rc.publish(server,json.dumps({'event':'sectionDone','data':{'id':unique_id,'message':'__cancel__'}}))
                    raise comfy.model_management.InterruptProcessingException()
                time.sleep(0.5)

            imgStr=rc.get(fileKey)
            shape=rc.get(fileKey+"_shape")
            if shape==None or imgStr==None:
                raise Exception("回传数据不存在")
            my_tuple = tuple([int(x) for x in shape.split(',')])
            decoded = np.frombuffer(base64.b64decode(imgStr), dtype=np.uint8)
            result=decoded.reshape(my_tuple)
            images=torch.from_numpy(np.array(result).astype(np.float32) / 255.0)
            rc.delete(fileKey)
            rc.delete(fileKey+"_shape")
            rc.close()
            pool.close()
        return (images, )

NODE_CLASS_MAPPINGS = {
    "SectionEnd": SectionEnd
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "SectionEnd": "分段负载结束"
}
