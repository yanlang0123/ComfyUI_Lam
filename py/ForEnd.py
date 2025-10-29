from PIL import Image
import numpy as np
import requests
import json
from .src.utils.uitls import AlwaysEqualProxy
from server import PromptServer
from .src.LamCustomPrompt import prompt as promptFun
from copy import deepcopy

class ForEnd:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        
        return {
            "required": {
                "total": ("INT", {"forceInput": True}),
                "i": ("INT",{"forceInput": True}),
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

    def for_end_fun(self,total,i,obj,unique_id,prompt,extra_pnginfo):
        pdata=json.loads('{}')
        pdata['client_id']=PromptServer.instance.client_id
        pdata['prompt']=deepcopy(prompt)
        start_id=prompt[unique_id]['inputs']['total'][0]
        result=''
        if extra_pnginfo :
            pdata['extra_data']={'extra_pnginfo':deepcopy(extra_pnginfo)}
            StatusInfo=pdata['extra_data']['extra_pnginfo']['StatusInfo'] if 'StatusInfo' in pdata['extra_data']['extra_pnginfo'] else ''
            index=pdata['extra_data']['extra_pnginfo']['index'] if 'index' in pdata['extra_data']['extra_pnginfo'] else 0
            if index==0:
                StatusInfo=''
                
            pdata['extra_data']['extra_pnginfo']['index']=index+1
            result = "第"+str(index+1)+"论结束........."
            if StatusInfo.endswith('循环结束')==False and len(StatusInfo)>0:
                result=StatusInfo+'\n'+result

            pdata['extra_data']['extra_pnginfo']['StatusInfo']=result

        i=i+pdata['prompt'][start_id]['inputs']['stop']
        pdata['prompt'][start_id]['inputs']['i']=i
        
        isDone=False
        if i>=total:
            result = result+ '\n整个循环结束'
            isDone = True
        else:
            queue_data=PromptServer.instance.prompt_queue.get_current_queue()
            pdata['prompt_id']=queue_data[0][0][1]
            r = promptFun(PromptServer.instance,pdata)

        return { "ui": { "text":[result],"isDone":[isDone]} }

NODE_CLASS_MAPPINGS = {
    "ForEnd": ForEnd
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ForEnd": "计次循环尾"
}
