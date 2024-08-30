from .src.utils.uitls import AlwaysEqualProxy
class LamCommonNames:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        names=["ckpt_name","lora_name","clip_name","control_net_name","style_model_name",
          "clip_vision_name","gligen_name","unet_name","vae_name","sampler_name","scheduler"]
        return {
            "required": {
                "name_type": (sorted(names), ),
            },"optional": {
                "i": ("INT",{"forceInput": True}),
            },"hidden": {
                "names": ("STRING", {"default": ""}),
            }
        }
    RETURN_TYPES = ("LIST","INT",AlwaysEqualProxy('*'),)
    RETURN_NAMES = ("名称列表","选择数量","下标名称",)
    FUNCTION = "get_comm_names"

    CATEGORY = "lam"

    def get_comm_names(self,name_type,i=None,names=''):
        names=names.split(',')
        name=names[i] if i is not None and len(names)>i else ''
        return (names,len(names),name, )

NODE_CLASS_MAPPINGS = {
    "LamCommonNames": LamCommonNames
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamCommonNames": "通用名称选择器"
}
