# -*- coding: utf-8 -*-
"""剪映特效轨道节点。"""


class JyEffectTrack:
    """特效轨道"""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "effect_group": ("EFFECT_GROUP",),
                "track_name": ("STRING", {"default": "audio", "tooltip": "轨道名称"}),
            }
        }

    RETURN_TYPES = ("TRACK",)
    RETURN_NAMES = ("轨道",)
    OUTPUT_NODE = False
    FUNCTION = "get_track"
    CATEGORY = "lam"

    def get_track(self, effect_group, track_name):
        track = {"track_type": "effect", "track_name": track_name, "group": effect_group}
        return (track,)


NODE_CLASS_MAPPINGS = {"JyEffectTrack": JyEffectTrack}
NODE_DISPLAY_NAME_MAPPINGS = {"JyEffectTrack": "剪映特效轨道"}


global_var=globals()
newInputs={}
effect_group=global_var.get("p0")
track_name=global_var.get("p1")

jet=JyEffectTrack()
rdata=jet.get_track(effect_group,track_name)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]