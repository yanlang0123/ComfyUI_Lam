
class MultiTextSetMask:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
             "required": {
                "clip": ("CLIP", ),
                "body_masks": ("MASKS",),
                "background_text": ("STRING", {"forceInput": True}),
                "text0": ("STRING", {"forceInput": True}),
            },
            "optional": {
                "text1": ("STRING", {"forceInput": True}),
            },
            "hidden": {"extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "multi_text_set_masks"

    CATEGORY = "lam"

    def multi_text_set_masks(self, clip,body_masks,background_text, extra_pnginfo, unique_id,**kwargs):
        values=[]
        for node in extra_pnginfo["workflow"]["nodes"]:
            if node["id"] == int(unique_id):
                values = node["properties"]["values"]
                break
        textList=[]
        for arg in kwargs:
            if type(kwargs[arg]) != str: 
                continue
            if arg.startswith('text'):
                textList.append(kwargs[arg])

        minSize=min([len(body_masks),len(textList)])
        conditioning=self.encode(clip,background_text)
        for i in range(minSize):
            conditioning_1=self.encode(clip,textList[i])
            conditioning_2=self.condAppend(conditioning_1,body_masks[i],values[i][0],values[i][1])
            conditioning=conditioning+conditioning_2

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