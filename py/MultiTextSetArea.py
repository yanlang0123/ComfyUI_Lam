
class MultiTextSetArea:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
             "required": {
                "conditioning_to": ("CONDITIONING", ),
                "clip": ("CLIP", ),
                "body_boxs": ("BOXS",),
            },
            "optional": {
                "textList": ("LIST",),
                "text0": ("STRING", {"forceInput": True}),
                "text1": ("STRING", {"forceInput": True}),
            },
            "hidden": {"extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "multi_text_set_area"

    CATEGORY = "lam"

    def multi_text_set_area(self,conditioning_to,clip,body_boxs,extra_pnginfo, unique_id,textList=[],**kwargs):
        values=[]
        for node in extra_pnginfo["workflow"]["nodes"]:
            if node["id"] == int(unique_id):
                values = node["properties"]["values"]
                break
        for arg in kwargs:
            if type(kwargs[arg]) != str: 
                continue
            if arg.startswith('text'):
                textList.append(kwargs[arg])

        if len(textList)==0:
            raise Exception('至少要输入一个文本')

        minSize=min([len(body_boxs),len(textList)])
        conditioning=conditioning_to
        for i in range(minSize):
            w,h,x,y=body_boxs[i]
            conditioning_1=self.encode(clip,textList[i])
            conditioning_2=self.appendArea(conditioning_1,w,h,x,y,values[i])
            conditioning=conditioning+conditioning_2

        return (conditioning,)

    def encode(self, clip, text):
        tokens = clip.tokenize(text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return [[cond, {"pooled_output": pooled}]]
    
    def appendArea(self, conditioning, width, height, x, y, strength):
        c = []
        for t in conditioning:
            n = [t[0], t[1].copy()]
            n[1]['area'] = (height // 8, width // 8, y // 8, x // 8)
            n[1]['strength'] = strength
            n[1]['set_area_to_bounds'] = False
            c.append(n)
        return c
    
NODE_CLASS_MAPPINGS = {
    "MultiTextSetArea": MultiTextSetArea
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiTextSetArea": "多文本区域条件设置"
}