# -*- coding: utf-8 -*-
"""剪映图片/视频轨道节点。"""


class JyMediaTrack:
    """视频/图片轨道"""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "meida_group": ("MEIDA_GROUP",),
                "track_name": ("STRING", {"default": "audio", "tooltip": "轨道名称"}),
            }
        }

    RETURN_TYPES = ("TRACK",)
    RETURN_NAMES = ("轨道",)
    OUTPUT_NODE = False
    FUNCTION = "get_track"
    CATEGORY = "lam"

    def get_track(self, meida_group, track_name):
        track = {"track_type": "video", "track_name": track_name, "group": meida_group}
        return (track,)


NODE_CLASS_MAPPINGS = {"JyMediaTrack": JyMediaTrack}
NODE_DISPLAY_NAME_MAPPINGS = {"JyMediaTrack": "剪映图片/视频轨道"}


global_var=globals()
newInputs={}
meida_group=global_var.get("p0")
track_name=global_var.get("p1")

jmt=JyMediaTrack()
rdata=jmt.get_track(meida_group,track_name)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]