# -*- coding: utf-8 -*-
"""剪映字幕节点。"""


def _add_newlines(text, max_length):
    """在指定长度处添加换行符，max_length 按中文字符数量计算（1 个中文 = 2 个英文宽度）。"""

    def get_char_width(char):
        if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303f':
            return 2
        return 1

    max_width = max_length * 2
    result = []
    current_line = ""
    current_width = 0

    for char in text:
        char_width = get_char_width(char)
        if current_width + char_width > max_width:
            result.append(current_line)
            current_line = char
            current_width = char_width
        else:
            current_line += char
            current_width += char_width

    if current_line:
        result.append(current_line)

    return '\n'.join(result)


class JyCaptionsNative:
    """字幕"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"default": "", "multiline": True, "tooltip": "字幕内容"}),
                "font": ("STRING", {"default": "宋体", "tooltip": "字体"}),
                "color": ("STRING", {"default": "#FFFFFF", "tooltip": "字幕颜色"}),
                "size": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 300, "step": 1.0, "tooltip": "字幕大小"}),
                "transform_x": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.1, "tooltip": "水平位移, 单位为半个画布宽"}),
                "transform_y": ("FLOAT", {"default": -0.8, "min": -1.0, "max": 1.0, "step": 0.1, "tooltip": "垂直位移, 单位为半个画布高"}),
                "start_at_track": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "草稿添加时间（秒）"}),
                "duration": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "持续时间（秒）"}),
                "row_max_size": ("INT", {"default": 16, "min": 1, "max": 1000, "step": 1, "tooltip": "行最大字符数, 单句超过将自动换行"}),
            },
            "optional": {
                "captions_group": ("CAPTIONS_GROUP",),
            }
        }

    RETURN_TYPES = ("JY_CAPTIONS", "CAPTIONS_GROUP",)
    RETURN_NAMES = ("字幕", "字幕组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_captions"
    CATEGORY = "lam"

    def jy_captions(self, text, font, color, size, transform_x, transform_y,
                    start_at_track, duration, row_max_size, captions_group=[]):
        captions_group = [*captions_group]
        captions = {
            "subtitle": _add_newlines(text, row_max_size),
            "font": font,
            "color": color,
            "size": size,
            "start_at_track": int(start_at_track * 1000000),
            "duration": int(duration * 1000000),
        }
        captions['clip_settings'] = {"transform_y": transform_y, "transform_x": transform_x}
        captions_group.append(captions)
        return (captions, captions_group,)


NODE_CLASS_MAPPINGS = {"JyCaptionsNative": JyCaptionsNative}
NODE_DISPLAY_NAME_MAPPINGS = {"JyCaptionsNative": "剪映字幕"}


global_var=globals()
newInputs={}
text=global_var.get("p0")
font=global_var.get("p1")
color=global_var.get("p2")
size=global_var.get("p3")
transform_x=global_var.get("p4")
transform_y=global_var.get("p5")
start_at_track=global_var.get("p6")
duration=global_var.get("p7")
row_max_size=global_var.get("p8")
captions_group=global_var.get("p9",[])

jcn=JyCaptionsNative()
rdata=jcn.jy_captions(text,font,color,size,transform_x,transform_y,start_at_track,duration,row_max_size,captions_group)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]