from PIL import Image
import numpy as np
import requests
import json
import comfy.utils
import torch
from .src.utils.uitls import AlwaysEqualProxy

class ForInnerEnd:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        
        return {
            "required": {
                "total": ("INT", {"forceInput": True}),
                "obj": (AlwaysEqualProxy("*"), ),
            }
        }
    RETURN_TYPES = (AlwaysEqualProxy("*"),)
    RETURN_NAMES = ('obj',)
    FUNCTION = "for_end_fun"

    CATEGORY = "lam"

    def for_end_fun(self,total,obj, **kwargs):
        objs=None
        if obj!=None and hasattr(obj, 'shape') and torch.is_tensor(obj) :
            objs=obj
        elif obj!=None:
            objs=[]
            objs.append(obj)
            
        for k,v in kwargs.items():
            if k.startswith('obj') and v!=None:
                if hasattr(obj, 'shape') and torch.is_tensor(obj) and torch.is_tensor(v):
                    if objs==None:
                        obj = v
                        continue
                    if  objs.shape[1:] != v.shape[1:]:
                        v = comfy.utils.common_upscale(v.movedim(-1,1), obj.shape[2], obj.shape[1], "bilinear", "center").movedim(1,-1)
                    objs = torch.cat((objs, v), dim=0)
                else:
                    objs.append(v)
                    
        return (objs,)

NODE_CLASS_MAPPINGS = {
    "ForInnerEnd": ForInnerEnd
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ForInnerEnd": "计次内循环尾"
}
