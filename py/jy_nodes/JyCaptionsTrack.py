# -*- coding: utf-8 -*-
"""剪映字幕轨道节点。"""


class JyCaptionsTrack:
    """字幕轨道"""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "captions_group": ("CAPTIONS_GROUP",),
                "track_name": ("STRING", {"default": "audio", "tooltip": "轨道名称"}),
            }
        }

    RETURN_TYPES = ("TRACK",)
    RETURN_NAMES = ("轨道",)
    OUTPUT_NODE = False
    FUNCTION = "get_track"
    CATEGORY = "lam"

    def get_track(self, captions_group, track_name):
        track = {"track_type": "text", "track_name": track_name, "group": captions_group}
        return (track,)


NODE_CLASS_MAPPINGS = {"JyCaptionsTrack": JyCaptionsTrack}
NODE_DISPLAY_NAME_MAPPINGS = {"JyCaptionsTrack": "剪映字幕轨道"}


global_var=globals()
newInputs={}
captions_group=global_var.get("p0")
track_name=global_var.get("p1")

jct=JyCaptionsTrack()
rdata=jct.get_track(captions_group,track_name)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]