from PIL import Image
import numpy as np
import torch
import os
import folder_paths
import random
import sys

class ForStart:
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
    RETURN_TYPES = ("INT","INT","INT")
    RETURN_NAMES = ("总数","循环次数","seed")
    FUNCTION = "for_start_fun"

    CATEGORY = "lam"

    def for_start_fun(self,total,stop,i):
        random.seed(i)
        return (total,i,random.randint(0,sys.maxsize),)

NODE_CLASS_MAPPINGS = {
    "ForStart": ForStart
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ForStart": "计次循环首"
}
