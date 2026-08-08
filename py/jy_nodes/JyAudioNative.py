# -*- coding: utf-8 -*-
"""剪映音频节点。"""

import os


class JyAudioNative:
    """音频"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {"default": "", "tooltip": "音频地址"}),
                "start_in_media": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "音频开始时间（秒）"}),
                "start_at_track": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "草稿添加时间（秒）"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "持续时间（秒）"}),
                "volume": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 20.0, "step": 0.01, "tooltip": "音量"}),
            },
            "optional": {
                "audio_group": ("AUDIO_GROUP",),
            }
        }

    RETURN_TYPES = ("JY_AUDIO", "AUDIO_GROUP",)
    RETURN_NAMES = ("音频", "音频组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_audio"
    CATEGORY = "lam"

    def jy_audio(self, file_path, start_in_media, start_at_track, duration, volume, audio_group=[]):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        audio_group = [*audio_group]
        audio = {
            "media_file_full_name": file_path,
            "start_in_media": int(start_in_media * 1000000),
            "start_at_track": int(start_at_track * 1000000),
            "duration": int(duration * 1000000),
            "volume": volume,
        }
        audio_group.append(audio)
        return (audio, audio_group,)


NODE_CLASS_MAPPINGS = {"JyAudioNative": JyAudioNative}
NODE_DISPLAY_NAME_MAPPINGS = {"JyAudioNative": "剪映音频"}


global_var=globals()
newInputs={}
file_path=global_var.get("p0")
start_in_media=global_var.get("p1")
start_at_track=global_var.get("p2")
duration=global_var.get("p3")
volume=global_var.get("p4")
audio_group=global_var.get("p5",[])

jan=JyAudioNative()
rdata=jan.jy_audio(file_path,start_in_media,start_at_track,duration,volume,audio_group)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]