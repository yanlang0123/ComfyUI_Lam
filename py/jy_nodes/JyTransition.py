# -*- coding: utf-8 -*-
"""剪映转场节点。"""


class JyTransition:
    """转场"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "transition": ("STRING", {"default": "", "tooltip": "转场名称"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "持续时间（秒）"}),
                "meida_out": ("MEIDA",),
            },
            "optional": {
                "meida_group": ("MEIDA_GROUP",),
            }
        }

    RETURN_TYPES = ("MEIDA", "MEIDA_GROUP",)
    RETURN_NAMES = ("图片/视频", "图片/视频组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_transition"
    CATEGORY = "lam"

    def jy_transition(self, transition, duration, meida_out, meida_group=[]):
        meida_group = [*meida_group]
        transition_data = {
            "transition": transition,
            "duration": int(duration * 1000000),
        }
        meida_out['transition_data'] = transition_data
        meida_group.append(meida_out)
        return (meida_out, meida_group,)


NODE_CLASS_MAPPINGS = {"JyTransition": JyTransition}
NODE_DISPLAY_NAME_MAPPINGS = {"JyTransition": "剪映转场"}


global_var=globals()
newInputs={}
transition=global_var.get("p0")
duration=global_var.get("p1")
meida_out=global_var.get("p2")
meida_group=global_var.get("p3",[])

jt=JyTransition()
rdata=jt.jy_transition(transition,duration,meida_out,meida_group)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]