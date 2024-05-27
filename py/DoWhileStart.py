from PIL import Image
import numpy as np
import torch
import os
import folder_paths
import random
import sys
from .src.utils.uitls import AlwaysEqualProxy

class DoWhileStart:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "obj": (AlwaysEqualProxy("*"), ),
            }
        }
    RETURN_TYPES = (AlwaysEqualProxy("*"),"DOWHILE","INT","INT",)
    RETURN_NAMES = ('obj','DOWHILE',"循环次数","seed",)
    FUNCTION = "do_while_start_fun"

    CATEGORY = "lam"

    def do_while_start_fun(self,obj, **kwargs):
        i=kwargs['i'] if 'i' in kwargs else 0
        random.seed(i)
        return (obj,'DOWHILE',i,random.randint(0,sys.maxsize),)

NODE_CLASS_MAPPINGS = {
    "DoWhileStart": DoWhileStart
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DoWhileStart": "判断循环首"
}
