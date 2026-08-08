# -*- coding: utf-8 -*-
"""剪映带动画图片/视频节点。"""

import os


class JyMediaAnimation:
    """带动画图片/视频"""

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
                "animation_in": ("ANIMATION_IN",),
                "animation_group": ("ANIMATION_GROUP",),
                "animation_out": ("ANIMATION_OUT",),
            }
        }

    RETURN_TYPES = ("MEIDA", "MEIDA_GROUP",)
    RETURN_NAMES = ("带动画图片/视频", "图片/视频组",)
    OUTPUT_NODE = False
    FUNCTION = "animation_video"
    CATEGORY = "lam"

    def animation_video(self, file_path, start_in_media, start_at_track, duration, volume,
                        meida_group=[], animation_in=None, animation_group=None, animation_out=None):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        meida_group = [*meida_group]
        animation_datas = []
        if animation_in:
            animation_datas.append(animation_in)
        if animation_group:
            animation_datas.append(animation_group)
        if animation_out:
            animation_datas.append(animation_out)
        meida = {
            "media_file_full_name": file_path,
            "start_in_media": int(start_in_media * 1000000),
            "start_at_track": int(start_at_track * 1000000),
            "duration": int(duration * 1000000),
            "volume": volume,
            "animation_datas": animation_datas,
        }
        meida_group.append(meida)
        return (meida, meida_group,)


NODE_CLASS_MAPPINGS = {"JyMediaAnimation": JyMediaAnimation}
NODE_DISPLAY_NAME_MAPPINGS = {"JyMediaAnimation": "剪映带动画图片/视频"}


global_var=globals()
newInputs={}
file_path=global_var.get("p0")
start_in_media=global_var.get("p1")
start_at_track=global_var.get("p2")
duration=global_var.get("p3")
volume=global_var.get("p4")
meida_group=global_var.get("p5",[])
animation_in=global_var.get("p6")
animation_group=global_var.get("p7")
animation_out=global_var.get("p8")

jma=JyMediaAnimation()
rdata=jma.animation_video(file_path,start_in_media,start_at_track,duration,volume,meida_group,animation_in,animation_group,animation_out)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]