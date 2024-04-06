import torch
from nodes import MAX_RESOLUTION

class MultiGLIGENTextBoxApply:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conditioning_to": ("CONDITIONING", ),
                "clip": ("CLIP", ),
                "gligen_textbox_model": ("GLIGEN", ),
                "text0": ("STRING", {"forceInput": True}),
                "text1": ("STRING", {"forceInput": True}),
            },
            "hidden": {"extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }
    


    RETURN_TYPES = ("CONDITIONING", "INT", "INT")
    RETURN_NAMES = (None, "resolutionX", "resolutionY")
    FUNCTION = "doStuff"
    CATEGORY = "lam"

    def doStuff(self,conditioning_to, clip, gligen_textbox_model, extra_pnginfo, unique_id, **kwargs):

        c = []
        values = []
        resolutionX = 512
        resolutionY = 512

        for node in extra_pnginfo["workflow"]["nodes"]:
            if node["id"] == int(unique_id):
                values = node["properties"]["values"]
                resolutionX = node["properties"]["width"]
                resolutionY = node["properties"]["height"]
                break
        conditioning=conditioning_to
        k=0
        for arg in kwargs:
            if k > len(values): 
                break
            if type(kwargs[arg]) != str: 
                continue
            x, y = values[k][0], values[k][1]
            w, h = values[k][2], values[k][3]
            conditioning=self.append(conditioning, clip, gligen_textbox_model, kwargs[arg], w,h,x,y)
            k+=1
            
        return (conditioning, resolutionX, resolutionY)
  
    def append(self, conditioning_to, clip, gligen_textbox_model, text, width, height, x, y):
        c = []
        cond, cond_pooled = clip.encode_from_tokens(clip.tokenize(text), return_pooled=True)
        for t in conditioning_to:
            n = [t[0], t[1].copy()]
            position_params = [(cond_pooled, height // 8, width // 8, y // 8, x // 8)]
            prev = []
            if "gligen" in n[1]:
                prev = n[1]['gligen'][2]

            n[1]['gligen'] = ("position", gligen_textbox_model, prev + position_params)
            c.append(n)
        return c

NODE_CLASS_MAPPINGS = {
    "MultiGLIGENTextBoxApply": MultiGLIGENTextBoxApply
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiGLIGENTextBoxApply": "多GLIGEN文本框应用"
}
