from PIL import Image
import numpy as np
import requests
import json
from .src.utils.uitls import AlwaysEqualProxy

class ForEnd:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        
        return {
            "required": {
                "total": ("INT", {"forceInput": True}),
                "i": ("INT",{"forceInput": True}),
                "port": ("INT", {"default": 8188, "min": 1, "max": 99999}),
                "obj": (AlwaysEqualProxy("*"),),
            },
        }
    RETURN_TYPES = ()
    FUNCTION = "for_end_fun"
    OUTPUT_NODE = True

    CATEGORY = "lam"

    def for_end_fun(self,total,i,port,obj):
        
        r = requests.get("http://127.0.0.1:"+str(port)+"/queue")
        result = r.text
        #print(result)
        data = json.loads(result)
        #rdata=data[list(data.keys())[0]]
        rdata=data['queue_running'][0] if len(data['queue_running'])>0 else []
        index=0
        if len(rdata)>0:
            pdata=json.loads('{}')
            pdata['client_id']=rdata[3]['client_id']
            pdata['extra_data']={'extra_pnginfo':rdata[3]['extra_pnginfo']}
            pdata['prompt']=rdata[2]
            for key in list(pdata['prompt'].keys()):
                if pdata['prompt'][key]['class_type']=='ForStart':
                    index=i//pdata['prompt'][key]['inputs']['stop']
                    i=i+pdata['prompt'][key]['inputs']['stop']
                    pdata['prompt'][key]['inputs']['i']=i
                    break
            if i>=total:
                return { "ui": { "text":'循环结束' } }
            r = requests.post("http://127.0.0.1:"+str(port)+"/prompt",json=pdata)
            result = r.text

        return { "ui": { "text":"第"+str(index+1)+"次循环结果："+result} }

NODE_CLASS_MAPPINGS = {
    "ForEnd": ForEnd
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ForEnd": "计次循环尾"
}
