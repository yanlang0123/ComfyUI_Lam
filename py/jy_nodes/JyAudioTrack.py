# -*- coding: utf-8 -*-
"""剪映音频轨道节点。"""


class JyAudioTrack:
    """音频轨道"""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio_group": ("AUDIO_GROUP",),
                "track_name": ("STRING", {"default": "audio", "tooltip": "轨道名称"}),
            }
        }

    RETURN_TYPES = ("TRACK",)
    RETURN_NAMES = ("轨道",)
    OUTPUT_NODE = False
    FUNCTION = "get_track"
    CATEGORY = "lam"

    def get_track(self, audio_group, track_name):
        track = {"track_type": "audio", "track_name": track_name, "group": audio_group}
        return (track,)


NODE_CLASS_MAPPINGS = {"JyAudioTrack": JyAudioTrack}
NODE_DISPLAY_NAME_MAPPINGS = {"JyAudioTrack": "剪映音频轨道"}


global_var=globals()
newInputs={}
audio_group=global_var.get("p0")
track_name=global_var.get("p1")

jat=JyAudioTrack()
rdata=jat.get_track(audio_group,track_name)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]