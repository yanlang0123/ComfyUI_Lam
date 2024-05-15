
class MultiTextSetMask:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
             "required": {
                "conditioning_to": ("CONDITIONING", ),
                "clip": ("CLIP", ),
                "body_masks": ("MASKS",),
            },
            "optional": {
                "textList": ("LIST",),
                "text0": ("STRING", {"forceInput": True}),
                "text1": ("STRING", {"forceInput": True}),
            },
            "hidden": {"extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "multi_text_set_masks"

    CATEGORY = "lam"

    def multi_text_set_masks(self,conditioning_to,clip,body_masks, extra_pnginfo, unique_id,textList=[],**kwargs):
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
        
        minSize=min([len(body_masks),len(textList)])
        conditioning=conditioning_to
        for i in range(minSize):
            if len(values)>i:
                value= values[i]
            else:
                value= values[0]

            conditioning_1=self.encode(clip,textList[i])
            conditioning_3=self.condAppend(conditioning_1,body_masks[i],value[0],value[1])
            conditioning=conditioning+conditioning_3

        return (conditioning,)

    def encode(self, clip, text):
        tokens = clip.tokenize(text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return [[cond, {"pooled_output": pooled}]]
    
    def condAppend(self, conditioning, mask, strength, set_cond_area):
        c = []
        set_area_to_bounds = False
        if set_cond_area != "default":
            set_area_to_bounds = True
        if len(mask.shape) < 3:
            mask = mask.unsqueeze(0)
        for t in conditioning:
            n = [t[0], t[1].copy()]
            _, h, w = mask.shape
            n[1]['mask'] = mask
            n[1]['set_area_to_bounds'] = set_area_to_bounds
            n[1]['mask_strength'] = strength
            c.append(n)
        return c
    
NODE_CLASS_MAPPINGS = {
    "MultiTextSetMask": MultiTextSetMask
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiTextSetMask": "多文本遮罩条件设置"
}