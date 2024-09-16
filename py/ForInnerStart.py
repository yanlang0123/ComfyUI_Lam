from PIL import Image
import numpy as np
import torch
import os
import folder_paths
import random
import sys
from .src.utils.uitls import AlwaysEqualProxy
import comfy.utils
from comfy_execution.graph_utils import GraphBuilder
NUM_FLOW_SOCKETS=5
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
            },"hidden": {
                "obj": (AlwaysEqualProxy("*"), ),
                **{ f"initial_value{i}": ("*",{"rawLink": True}) for i in range(NUM_FLOW_SOCKETS)}
            }
        }
    RETURN_TYPES = ("DOWHILE","INT","INT",AlwaysEqualProxy("*"),"INT","INT")
    RETURN_NAMES = ("DOWHILE","循环次数","seed",'回传数据',"总数","步长")
    FUNCTION = "for_start_fun"

    CATEGORY = "lam"

    def for_start_fun(self,total,stop,i,obj=None,**kwargs):
        graph = GraphBuilder()
        objs=[]
        if 'initial_value0' in kwargs:
            total=kwargs["initial_value0"]
        if 'initial_value1' in kwargs:
            stop=kwargs["initial_value1"]
        if 'initial_value2' in kwargs:
            objs=kwargs["initial_value2"]
        # while_open = graph.node("DoWhileStart", i=i,obj=obj,initial_value0=total,initial_value1=stop,initial_value2=objs,
        #                         **{(f"initial_value{i}"): kwargs.get(f"initial_value{i}", None) for i in range(3, NUM_FLOW_SOCKETS)})
        random.seed(i)
        return {
            "result": tuple(["stub", i, random.randint(0,sys.maxsize),obj,total,stop,objs,]),
            "expand": graph.finalize(),
        }

NODE_CLASS_MAPPINGS = {
    "ForInnerStart": ForInnerStart
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ForInnerStart": "计次内循环首"
}
