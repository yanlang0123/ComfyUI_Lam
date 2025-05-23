from .src.utils.uitls import AlwaysEqualProxy,AlwaysTupleZero
import comfy.samplers
import base64

class LamCommonHidden:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "hidden": {
                "hidden": ("STRING",{"multiline": True}),  #隐藏参数
                "unique_id": "UNIQUE_ID",           #节点编号
                "dynprompt": "DYNPROMPT",
                "prompt": "PROMPT",                 #流程节点信息
                "extra_pnginfo": "EXTRA_PNGINFO"    #前端流程图信息
            }
        }
    RETURN_TYPES = AlwaysTupleZero(AlwaysEqualProxy("*"),)

    FUNCTION = "commm_hidden"

    OUTPUT_NODE = True

    CATEGORY = "lam"

    def commm_hidden(self,hidden="",unique_id=None,extra_pnginfo=None,**kwargs):
        if hidden=="":
            hidden=[node['properties']['hidden'] for node in extra_pnginfo['workflow']['nodes'] if int(node['id'])==int(unique_id)][0]
        lookup = {}
        for arg in kwargs:
            lookup[arg] = kwargs[arg]
        
        msg='完成'
        r=""
        expand=None
        if hidden:
            hidden = base64.b64decode(hidden).decode("utf-8")
            exec(hidden, lookup)
            if 'result' in lookup:
                r = lookup['result']
            if "expand" in lookup:
                expand = lookup['expand']
        else:
            raise SyntaxError("隐藏节点语法错误")

        if not isinstance(r, tuple):
            r = (r,)
        
        return {"ui": {"value": [msg]}, "result": r,"expand":expand}
    
class LamSamplerName:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, {"tooltip": "The algorithm used when sampling, this can affect the quality, speed, and style of the generated output."})
            }
        }
    
    RETURN_TYPES = (AlwaysEqualProxy("*"),)
    RETURN_NAMES = ("sampler_name",)
    FUNCTION = "sampler_name"
    CATEGORY = "lam"

    def sampler_name(self, sampler_name):
        return (sampler_name,)
    
class LamScheduler:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, {"tooltip": "The scheduler controls how noise is gradually removed to form the image."})
            }
        }
    
    RETURN_TYPES = (AlwaysEqualProxy("*"),)
    RETURN_NAMES = ("scheduler",)
    FUNCTION = "scheduler"
    CATEGORY = "lam"

    def scheduler(self, scheduler):
        return (scheduler,)

    


NODE_CLASS_MAPPINGS = {
    "LamCommonHidden": LamCommonHidden,
    "LamSamplerName":LamSamplerName,
    "LamScheduler": LamScheduler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamCommonHidden": "通用隐藏节点",
    "LamSamplerName": "采样器名称",
    "LamScheduler": "调度器名称"
}


