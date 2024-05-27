from PIL import Image
import numpy as np
import requests
import json
import comfy.utils
import torch
from .src.utils.uitls import AlwaysEqualProxy

class DoWhileEnd:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "start": ("DOWHILE", {"forceInput": True}),
                "ANY": (AlwaysEqualProxy("*"), ),
                "obj": (AlwaysEqualProxy("*"), ),
            }
        }
    RETURN_TYPES = (AlwaysEqualProxy("*"),)
    RETURN_NAMES = ('endObj',)
    FUNCTION = "for_end_fun"

    CATEGORY = "lam"

    def for_end_fun(self,start,ANY,obj,**kwargs):
        print(kwargs)
        return (obj,)

NODE_CLASS_MAPPINGS = {
    "DoWhileEnd": DoWhileEnd
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DoWhileEnd": "判断循环尾"
}
