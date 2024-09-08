import numpy as np
import os
import folder_paths
from PIL import Image
import json

class LamGetPngInfo:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "imgPath": ("STRING",{"default": ""}),                                                         #单行文本输入框
            },
        }

    RETURN_TYPES = ("DICT", ) #返回参数类型
    RETURN_NAMES = ("params",)  #返回参数名称

    FUNCTION = "get_info_str" #执行函数名称

    OUTPUT_NODE = True     #是否为输出节点

    CATEGORY = "lam"    #节点分类  lam/test

    DESCRIPTION = "获取png图片info信息"  #节点描述


    def get_info_str(self,imgPath):
        img = Image.open(imgPath)
        info=img.info
        return (info,)
    


NODE_CLASS_MAPPINGS = { #节点名称与类名对应关系
    "LamGetPngInfo": LamGetPngInfo,
}

NODE_DISPLAY_NAME_MAPPINGS = { #节点名称与显示名称对应关系
    "LamGetPngInfo": "获取图片信息",
}
