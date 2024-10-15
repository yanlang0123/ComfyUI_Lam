import time
import numpy as np
import base64
import uuid
import torch
import json
from .src.wechat.redisSub import r
from .src.utils.chooser import ChooserMessage, ChooserCancelled
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
                dataObj=json.loads(data)
                prompt=dataObj['prompt']
                fileKey=str(uuid.uuid4())
                if images!=None:
                    arr=np.clip(255. * images.cpu().numpy(), 0, 255).astype(np.uint8)
                    arrStr=base64.b64encode(arr.tobytes()).decode("utf-8")
                    r.setex(fileKey, 15, arrStr)
                    prompt[unique_id]['inputs']['data']=json.dumps({"sectype":sectype,"fileKey":fileKey,'shape':arr.shape})
                    prompt[unique_id]['inputs']['sectype']=1
                    prompt[unique_id]['inputs'].pop('images', None)
                else:
                    prompt[unique_id]['inputs']['data']=json.dumps({"sectype":sectype,"fileKey":fileKey})
                    prompt[unique_id]['inputs']['sectype']=1
                    prompt[unique_id]['inputs'].pop('images', None)
                r.publish(server,json.dumps({'event':'addTask','data':dataObj}))
                ChooserMessage.addMessage(unique_id, '__start__')
                while True:
                    if ChooserMessage.cancelled:
                        raise ChooserCancelled()
                    shape=r.get(fileKey+"_shape")
                    if shape!=None:
                        break
                    time.sleep(0.1)
                return ({"sectype":sectype,"fileKey":fileKey},images, )
        else:
            if server=='default':
                raise Exception("参数类型异常")
            dataObj=json.loads(data)
            fileKey=dataObj['fileKey']
            if fileKey=='':
                raise Exception("文件不能为空")
            if 'shape' in dataObj:
                shape=dataObj['shape']
                imgStr=r.get(fileKey)
                decoded = np.frombuffer(base64.b64decode(imgStr), dtype=np.uint8)
                result=decoded.reshape(shape)
                images=torch.from_numpy(np.array(result).astype(np.float32) / 255.0)
                r.delete(fileKey)
            return ({"sectype":sectype,"fileKey":fileKey},images, )
            
            

NODE_CLASS_MAPPINGS = {
    "SectionStart": SectionStart
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "SectionStart": "分段负载开始"
}
