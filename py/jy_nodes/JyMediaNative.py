# -*- coding: utf-8 -*-
"""剪映图片/视频节点（不带动画）。"""

import os


class JyMediaNative:
    """不带动画图片/视频"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {"default": "", "tooltip": "图片/视频地址"}),
                "start_in_media": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "视频开始时间（秒）"}),
                "start_at_track": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "草稿添加时间（秒）"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "持续时间（秒）"}),
                "volume": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 20.0, "step": 0.01, "tooltip": "音量"}),
            },
            "optional": {
                "meida_group": ("MEIDA_GROUP",),
            }
        }

    RETURN_TYPES = ("MEIDA", "MEIDA_GROUP",)
    RETURN_NAMES = ("图片/视频", "图片/视频组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_media"
    CATEGORY = "lam"

    def jy_media(self, file_path, start_in_media, start_at_track, duration, volume, meida_group=[]):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        meida_group = [*meida_group]
        meida = {
            "media_file_full_name": file_path,
            "start_in_media": int(start_in_media * 1000000),
            "start_at_track": int(start_at_track * 1000000),
            "duration": int(duration * 1000000),
            "volume": volume,
        }
        meida_group.append(meida)
        return (meida, meida_group,)


NODE_CLASS_MAPPINGS = {"JyMediaNative": JyMediaNative}
NODE_DISPLAY_NAME_MAPPINGS = {"JyMediaNative": "剪映图片/视频"}


global_var=globals()
newInputs={}
file_path=global_var.get("p0")
start_in_media=global_var.get("p1")
start_at_track=global_var.get("p2")
duration=global_var.get("p3")
volume=global_var.get("p4")
meida_group=global_var.get("p5",[])

jmn=JyMediaNative()
rdata=jmn.jy_media(file_path,start_in_media,start_at_track,duration,volume,meida_group)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]