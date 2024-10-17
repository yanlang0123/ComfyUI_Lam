import time
import numpy as np
import base64
import uuid
import torch
import json
from .src.wechat.redisSub import r
import pickle
from .src.utils.chooser import ChooserMessage, ChooserCancelled
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
            arr=np.clip(255. * images.cpu().numpy(), 0, 255).astype(np.uint8)
            arrStr=base64.b64encode(arr.tobytes()).decode("utf-8")
            fileKey=section['fileKey']
            r.setex(fileKey, 15, arrStr)
            serialized_tuple = ','.join([str(x) for x in arr.shape])
            r.setex(fileKey+"_shape",15,serialized_tuple)
            return (images, )
        else:
            fileKey=section['fileKey']
            ChooserMessage.addMessage(unique_id, '__start__')
            while True:
                if ChooserMessage.cancelled:
                    raise ChooserCancelled()
                imgStr=r.get(fileKey)
                shape=r.get(fileKey+"_shape")
                if shape!=None:
                    my_tuple = tuple([int(x) for x in shape.split(',')])
                if imgStr!=None:
                    break
                time.sleep(0.5)
            decoded = np.frombuffer(base64.b64decode(imgStr), dtype=np.uint8)
            result=decoded.reshape(my_tuple)
            images=torch.from_numpy(np.array(result).astype(np.float32) / 255.0)
            r.delete(fileKey)
            r.delete(fileKey+"_shape")
        return (images, )

NODE_CLASS_MAPPINGS = {
    "SectionEnd": SectionEnd
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "SectionEnd": "分段负载结束"
}
