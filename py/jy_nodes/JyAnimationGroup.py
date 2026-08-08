# -*- coding: utf-8 -*-
"""组动画（中间动画）节点。"""


class JyAnimationGroup:
    """中间动画"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "animation": ("STRING", {"default": "", "tooltip": "动画名称"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("ANIMATION_GROUP",)
    RETURN_NAMES = ("中间动画",)
    OUTPUT_NODE = False
    FUNCTION = "jy_animation_group"
    CATEGORY = "lam"

    def jy_animation_group(self, animation, duration):
        return ({
            "animation": animation,
            "duration": int(duration * 1000000),
            "animation_type": "group",
        },)


NODE_CLASS_MAPPINGS = {"JyAnimationGroup": JyAnimationGroup}
NODE_DISPLAY_NAME_MAPPINGS = {"JyAnimationGroup": "组动画"}


global_var=globals()
newInputs={}
animation=global_var.get("p0")
duration=global_var.get("p1")

jag=JyAnimationGroup()
rdata=jag.jy_animation_group(animation,duration)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]