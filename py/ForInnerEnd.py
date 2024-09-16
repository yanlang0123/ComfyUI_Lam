from PIL import Image
import numpy as np
import requests
import json
import comfy.utils
import torch
from .src.utils.uitls import AlwaysEqualProxy
from comfy_execution.graph_utils import GraphBuilder
NUM_FLOW_SOCKETS = 5
class ForInnerEnd:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        
        return {
            "required": {
                "start": ("DOWHILE", {"rawLink": True}),
                "obj": (AlwaysEqualProxy("*"),{"rawLink": True} ),
            },
            "hidden": {
                 f"initial_value{i}": ("*",{"rawLink": True}) for i in range(3, NUM_FLOW_SOCKETS)
            }
        }
    RETURN_TYPES = (AlwaysEqualProxy("*"),AlwaysEqualProxy("*"),)
    RETURN_NAMES = ('objs','endObj',)
    FUNCTION = "for_end_fun"

    CATEGORY = "lam"

    def for_end_fun(self,start,obj, **kwargs):
        graph = GraphBuilder()
        while_open = start[0]
        exprStr='''
import torch
import comfy.utils
if hasattr(p1, 'shape') and torch.is_tensor(p1) :
    if len(p0)==0:
        p0=p1
    else:
        if  p0.shape[1:] != p1.shape[1:]:
            p1= comfy.utils.common_upscale(p1.movedim(-1,1), p0.shape[2], p0.shape[1], "bilinear", "center").movedim(1,-1)
        p0 = torch.cat((p0, p1), dim=0)
elif p1 is not None:
    p0.append(p1)

result=p0
'''
        addObjs = graph.node("MultiParamFormula", advanced="enable",expression=exprStr, p0=[while_open,6], p1=obj)
        inode = graph.node("MultiParamFormula", advanced="disable",expression="p0+p1", p0=[while_open,1], p1=[while_open,5])
        anyNode = graph.node("MultiParamFormula", advanced="disable",expression="p0<p1", p0=inode.out(0), p1=[while_open,4])
        input_values = {f"initial_value{i}": kwargs.get(f"initial_value{i}", None) for i in range(3, NUM_FLOW_SOCKETS)}
        while_close = graph.node("DoWhileEnd",
                start=start,
                stop=[while_open,5],
                ANY=anyNode.out(0),
                obj=obj,
                initial_value0=[while_open,4],
                initial_value1=[while_open,5],
                initial_value2=addObjs.out(0),
                **input_values)
        return {
            "result": tuple([while_close.out(4),while_close.out(1),]),
            "expand": graph.finalize(),
        }

NODE_CLASS_MAPPINGS = {
    "ForInnerEnd": ForInnerEnd
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ForInnerEnd": "计次内循环尾"
}
