from PIL import Image
import numpy as np
import requests
import json
import comfy.utils
import torch

class ForInnerEnd:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        
        return {
            "required": {
                "total": ("INT", {"forceInput": True}),
                "images": ("IMAGE", ),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ('图片',)
    FUNCTION = "for_end_fun"

    CATEGORY = "lam"

    def for_end_fun(self,total,images, **kwargs):
        for k,v in kwargs.items():
            if k.startswith('images') and v!=None:
                if images== None:
                    images = v
                    continue
                if images.shape[1:] != v.shape[1:]:
                    v = comfy.utils.common_upscale(v.movedim(-1,1), images.shape[2], images.shape[1], "bilinear", "center").movedim(1,-1)
                images = torch.cat((images, v), dim=0)

        return (images,)

NODE_CLASS_MAPPINGS = {
    "ForInnerEnd": ForInnerEnd
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ForInnerEnd": "计次内循环尾"
}
