# -*- coding: utf-8 -*-
"""音频转字幕组节点。"""

import os
import difflib


def _correct_string(a, b):
    """根据 a 中的内容修正 b。"""
    matcher = difflib.SequenceMatcher(None, a, b)
    matches = matcher.get_matching_blocks()

    corrected = ""
    prev_start = 0
    prev_end = 0
    for match in matches:
        if prev_end <= 0:
            prev_start = match.a - match.b
            prev_end = match.a - match.b
        if match.a > prev_start + len(b):
            continue
        if match.a > prev_end:
            corrected += a[prev_end:match.a]
        corrected += a[match.a:match.a + match.size]
        prev_end = match.a + match.size
    return corrected


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


class JyAudio2CaptionsGroup:
    """音频转字幕组"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (["tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3"], {"default": "medium"}),
                "file_path": ("STRING", {"default": "", "tooltip": "音频地址"}),
                "start_at_track": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01, "tooltip": "草稿添加时间（秒）"}),
                "font": ("STRING", {"default": "宋体", "tooltip": "字体"}),
                "color": ("STRING", {"default": "#FFFFFF", "tooltip": "字幕颜色"}),
                "size": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 300, "step": 1.0, "tooltip": "字幕大小"}),
                "transform_x": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.1, "tooltip": "水平位移, 单位为半个画布宽"}),
                "transform_y": ("FLOAT", {"default": -0.8, "min": -1.0, "max": 1.0, "step": 0.1, "tooltip": "垂直位移, 单位为半个画布高"}),
                "row_max_size": ("INT", {"default": 16, "min": 1, "max": 1000, "step": 1, "tooltip": "行最大字符数, 单句超过将自动换行"}),
            },
            "optional": {
                "captions_group": ("CAPTIONS_GROUP",),
                "all_subtitles": ("STRING", {"forceInput": False}),
            }
        }

    RETURN_TYPES = ("CAPTIONS_GROUP", "STRING", "FLOAT",)
    RETURN_NAMES = ("字幕组", "文字内容", "结束时间",)
    OUTPUT_NODE = False
    FUNCTION = "jy_audio2captions_group"
    CATEGORY = "lam"

    def jy_audio2captions_group(self, model, file_path, start_at_track, font, color, size,
                                transform_x, transform_y, row_max_size=16,
                                captions_group=[], all_subtitles=""):
        import whisper
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        model = whisper.load_model(model)
        result = model.transcribe(file_path)
        segments = result["segments"]
        resultText = result["text"]
        captions_group = [*captions_group]
        end_time = 0
        for i in range(len(segments)):
            text = segments[i]["text"]
            text = _correct_string(all_subtitles, text) if len(all_subtitles) > 0 else text
            text = _add_newlines(segments[i]["text"], row_max_size)

            start = start_at_track + segments[i]["start"]
            duration = segments[i]["end"] - segments[i]["start"]
            captions = {
                "subtitle": text,
                "font": font,
                "color": color,
                "size": size,
                "start_at_track": int(round(start * 100)) * 10000,
                "duration": int(round(duration * 100)) * 10000,
            }
            captions['clip_settings'] = {"transform_y": transform_y, "transform_x": transform_x}
            end_time = start + duration
            captions_group.append(captions)
        return (captions_group, resultText, end_time,)


NODE_CLASS_MAPPINGS = {"JyAudio2CaptionsGroup": JyAudio2CaptionsGroup}
NODE_DISPLAY_NAME_MAPPINGS = {"JyAudio2CaptionsGroup": "音频转字幕组"}


global_var=globals()
newInputs={}
model=global_var.get("p0")
file_path=global_var.get("p1")
start_at_track=global_var.get("p2")
font=global_var.get("p3")
color=global_var.get("p4")
size=global_var.get("p5")
transform_x=global_var.get("p6")
transform_y=global_var.get("p7")
row_max_size=global_var.get("p8",16)
captions_group=global_var.get("p9",[])
all_subtitles=global_var.get("p10","")

ja2cg=JyAudio2CaptionsGroup()
rdata=ja2cg.jy_audio2captions_group(model,file_path,start_at_track,font,color,size,transform_x,transform_y,row_max_size,captions_group,all_subtitles)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]