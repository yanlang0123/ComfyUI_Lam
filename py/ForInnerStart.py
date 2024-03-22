from PIL import Image
import numpy as np
import torch
import os
import folder_paths
import random
import sys

class ForInnerStart:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "total": ("INT", {"default": 0, "min": 0, "max": 99999}),
                "stop": ("INT", {"default": 1, "min": 1, "max": 999}),
                "i": ("INT", {"default": 0, "min": 0, "max": 99999}),
            }
        }
    RETURN_TYPES = ("INT","INT","INT","IMAGE",)
    RETURN_NAMES = ("总数","循环次数","seed",'图片',)
    FUNCTION = "for_start_fun"

    CATEGORY = "lam"

    def for_start_fun(self,total,stop,i, **kwargs):
        images=kwargs['images'] if 'images' in kwargs else None
        random.seed(i)
        return (total,i,random.randint(0,sys.maxsize),images,)

NODE_CLASS_MAPPINGS = {
    "ForInnerStart": ForInnerStart
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ForInnerStart": "计次内循环首"
}
