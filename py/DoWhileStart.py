from PIL import Image
import numpy as np
import torch
import os
import folder_paths
import random
import sys
from .src.utils.uitls import AlwaysEqualProxy
NUM_FLOW_SOCKETS = 5
class DoWhileStart:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "obj": (AlwaysEqualProxy("*"), ),
            },"hidden": {
                "i": ("INT", {"default": 0, "min": 0, "max": 99999}),
                **{f"initial_value{i}": ("*",{"rawLink": True}) for i in range(NUM_FLOW_SOCKETS)}
            }
        }
    RETURN_TYPES = ("DOWHILE","INT","INT",AlwaysEqualProxy("*"))
    RETURN_NAMES = ("DOWHILE","循环次数","seed",'回传数据')
    FUNCTION = "do_while_start_fun"

    CATEGORY = "lam"

    def do_while_start_fun(self,obj=None,i=0, **kwargs):
        random.seed(i)
        values = ["stub",i,random.randint(0,sys.maxsize),obj]
        for i in range(NUM_FLOW_SOCKETS):
            values.append(kwargs.get(f"initial_value{i}", None))
        return tuple(values)

NODE_CLASS_MAPPINGS = {
    "DoWhileStart": DoWhileStart
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DoWhileStart": "判断循环首"
}
