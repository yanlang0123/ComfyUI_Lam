# -*- coding: utf-8 -*-
"""剪映特效节点。"""


class JyEffectNative:
    """特效"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "effect": ("STRING", {"default": "", "tooltip": "特效名称"}),
                "start_at_track": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "草稿添加时间（秒）"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "持续时间（秒）"}),
            },
            "optional": {
                "effect_group": ("EFFECT_GROUP",),
            }
        }

    RETURN_TYPES = ("JY_EFFECT", "EFFECT_GROUP",)
    RETURN_NAMES = ("特效", "特效组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_effect"
    CATEGORY = "lam"

    def jy_effect(self, effect, start_at_track, duration, effect_group=[]):
        effect_group = [*effect_group]
        effect_data = {
            "effect_name_or_resource_id": effect,
            "start": int(start_at_track * 1000000),
            "duration": int(duration * 1000000),
        }
        effect_group.append(effect_data)
        return (effect_data, effect_group,)


NODE_CLASS_MAPPINGS = {"JyEffectNative": JyEffectNative}
NODE_DISPLAY_NAME_MAPPINGS = {"JyEffectNative": "剪映特效"}


global_var=globals()
newInputs={}
effect=global_var.get("p0")
start_at_track=global_var.get("p1")
duration=global_var.get("p2")
effect_group=global_var.get("p3",[])

jen=JyEffectNative()
rdata=jen.jy_effect(effect,start_at_track,duration,effect_group)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]