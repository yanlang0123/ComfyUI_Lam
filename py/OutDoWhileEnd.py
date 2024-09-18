from PIL import Image
import numpy as np
import requests
import json
from .src.utils.uitls import AlwaysEqualProxy
from server import PromptServer
from .WeChatAuth import prompt as promptFun
from copy import deepcopy

class OutDoWhileEnd:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        
        return {
            "required": {
                "start": ("OUTDOWHILE", {"rawLink": True}),
                "ANY": (AlwaysEqualProxy("*"), ),
                "obj": (AlwaysEqualProxy("*"),),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",           #节点编号
                "prompt": "PROMPT",                 #流程节点信息
                "extra_pnginfo": "EXTRA_PNGINFO"    #前端流程图信息
            },
        }
    RETURN_TYPES = ()
    FUNCTION = "for_end_fun"
    OUTPUT_NODE = True

    CATEGORY = "lam"

    def for_end_fun(self,start,ANY,obj,unique_id,prompt,extra_pnginfo):
        pdata=json.loads('{}')
        pdata['client_id']=PromptServer.instance.client_id
        pdata['extra_data']={'extra_pnginfo':deepcopy(extra_pnginfo)}
        pdata['prompt']=deepcopy(prompt)
        start_id=start[0]
        StatusInfo=pdata['extra_data']['extra_pnginfo']['StatusInfo'] if 'StatusInfo' in pdata['extra_data']['extra_pnginfo'] else ''
        index=pdata['extra_data']['extra_pnginfo']['index'] if 'index' in pdata['extra_data']['extra_pnginfo'] else 0
        if index==0:
            StatusInfo=''

        i=pdata['prompt'][start_id]['inputs']['i'] if 'i' in pdata['prompt'][start_id]['inputs'] else 0
        pdata['prompt'][start_id]['inputs']['i']=i+1
        pdata['extra_data']['extra_pnginfo']['index']=index+1
        
        result = "第"+str(index+1)+"论结束........."

        if not ANY:
            result = result+ '\n整个循环结束'
        else:
            r = promptFun(PromptServer.instance,pdata)

        if StatusInfo.endswith('循环结束')==False and len(StatusInfo)>0:
            result=StatusInfo+'\n'+result

        pdata['extra_data']['extra_pnginfo']['StatusInfo']=result

        return { "ui": { "text":result} }

NODE_CLASS_MAPPINGS = {
    "OutDoWhileEnd": OutDoWhileEnd
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OutDoWhileEnd": "判断外循环尾"
}
