import torch
from .src.adv_encode import advanced_encode, advanced_encode_XL


class MultiTextEncodeAdvanced:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip": ("CLIP", ),
                "textList": ("LIST",),
                "token_normalization": (["none", "mean", "length", "length+mean"],),
                "weight_interpretation": (["comfy", "A1111", "compel", "comfy++", "down_weight"],),
            },
            "optional": {
                "pre_text": ("STRING", {"multiline": True, }),
                "app_text": ("STRING", {"multiline": True, }),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "multi_text_set_area"

    CATEGORY = "lam"

    def multi_text_set_area(self, clip, textList, token_normalization, weight_interpretation, pre_text='', app_text='', affect_pooled='disable'):
        if len(textList) == 0:
            raise Exception('至少要输入一个文本')

        pooled_out = []
        cond_out = []
        for i in range(len(textList)):
            cond, pooled = advanced_encode(
                clip, pre_text+' '+textList[i]+' '+app_text, token_normalization, weight_interpretation, w_max=1.0, apply_to_pooled=affect_pooled == 'enable')
            if cond!=None:
                cond_out.append(cond)

            if pooled!=None:
                pooled_out.append(pooled)

        final_pooled_output = torch.cat(pooled_out, dim=0) if len(pooled_out) > 0 else None
        final_conditioning = torch.cat(cond_out, dim=0) if len(cond_out) > 0 else None

        return ([[final_conditioning, {"pooled_output": final_pooled_output}]],)


NODE_CLASS_MAPPINGS = {
    "MultiTextEncodeAdvanced": MultiTextEncodeAdvanced
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiTextEncodeAdvanced": "多文本CLIP批量编码(BNK)"
}
