
class MultiTextSetGligen:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
             "required": {
                "gligen_textbox_model": ("GLIGEN", ),
                "conditioning_to": ("CONDITIONING", ),
                "clip": ("CLIP", ),
                "body_boxs": ("BOXS",),
            },
            "optional": {
                "textList": ("LIST",),
                "text0": ("STRING", {"forceInput": True}),
                "text1": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "multi_text_set_gligen"

    CATEGORY = "lam"

    def multi_text_set_gligen(self, gligen_textbox_model,conditioning_to,clip,body_boxs, textList=[],**kwargs):
        for arg in kwargs:
            if type(kwargs[arg]) != str: 
                continue
            if arg.startswith('text'):
                textList.append(kwargs[arg])

        if len(textList)==0:
            raise Exception('至少要输入一个文本')

        minSize=min([len(body_boxs),len(textList)])
        conditioning= conditioning_to
        for i in range(minSize):
            w,h,x,y=body_boxs[i]
            conditioning=self.appendGligen(conditioning, clip, gligen_textbox_model,textList[i], w,h,x,y)

        return (conditioning,)

    def encode(self, clip, text):
        tokens = clip.tokenize(text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return [[cond, {"pooled_output": pooled}]]
    
    def appendGligen(self, conditioning_to, clip, gligen_textbox_model, text, width, height, x, y):
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
    "MultiTextSetGligen": MultiTextSetGligen
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiTextSetGligen": "多文本GLIGEN设置"
}