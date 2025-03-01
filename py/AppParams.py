from PIL import Image
import numpy as np
import torch
import folder_paths
import os
class AppParams:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
               "appName": ("STRING", {"default":""}),
               "appType": (["default","paint-board"],),
               "appDesc": ("STRING", {"multiline": True,"default":""}),
            }
        }
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "add_app_params"

    CATEGORY = "lam"

    def add_app_params(self,**kwargs):
        return 

NODE_CLASS_MAPPINGS = {
    "AppParams": AppParams
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "AppParams": "应用参数管理"
}
