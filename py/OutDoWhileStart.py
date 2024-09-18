from PIL import Image
import numpy as np
import torch
import os
import folder_paths
import random
import sys
from .src.utils.uitls import AlwaysEqualProxy

class OutDoWhileStart:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "hidden": {
                "i": ("INT", {"default": 0, "min": 0, "max": 99999}),
            }
        }
    RETURN_TYPES = ("OUTDOWHILE","INT","INT")
    RETURN_NAMES = ("OUTDOWHILE","循环次数","seed")
    FUNCTION = "for_start_fun"

    CATEGORY = "lam"

    def for_start_fun(self,i=0):
        random.seed(i)
        return ("stub",i,random.randint(0,sys.maxsize),)

NODE_CLASS_MAPPINGS = {
    "OutDoWhileStart": OutDoWhileStart
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "OutDoWhileStart": "判断外循环首"
}
