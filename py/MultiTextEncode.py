import torch

class MultiTextEncode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
             "required": {
                "clip": ("CLIP", ),
                "textList": ("LIST",),
            },
            "optional": {
                "pre_text": ("STRING", {"multiline": True, }), 
                "app_text": ("STRING", {"multiline": True, }),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "multi_text_set_area"

    CATEGORY = "lam"

    def multi_text_set_area(self,clip,textList,pre_text='',app_text=''):
        if len(textList)==0:
            raise Exception('至少要输入一个文本')

        pooled_out = []
        cond_out = []
        for i in range(len(textList)):
            cond, pooled=self.encode(clip,pre_text+' '+textList[i]+' '+app_text)
            cond_out.append(cond)
            pooled_out.append(pooled)

        final_pooled_output = torch.cat(pooled_out, dim=0)
        final_conditioning = torch.cat(cond_out, dim=0)

        return ([[final_conditioning, {"pooled_output": final_pooled_output}]],)

    def encode(self, clip, text):
        tokens = clip.tokenize(text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return cond, pooled
    
NODE_CLASS_MAPPINGS = {
    "MultiTextEncode": MultiTextEncode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiTextEncode": "多文本CLIP批量编码"
}