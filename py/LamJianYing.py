import os
import folder_paths
import zipfile
import shutil
import uuid
import json
from . import pyJianYingDraft as draft
from .pyJianYingDraft import Intro_type,Outro_type,Group_animation_type, Transition_type, trange, tim
import difflib

def correct_string(a, b):
    # 使用SequenceMatcher找到最佳匹配
    matcher = difflib.SequenceMatcher(None, a, b)
    
    # 获取匹配块
    matches = matcher.get_matching_blocks()
    
    # 构建纠正后的字符串
    corrected = ""
    prev_start=0
    prev_end = 0
    for match in matches:
        # 添加不匹配的部分（从A中取）
        if prev_end<=0 :
            prev_start=match.a - match.b
            prev_end=match.a - match.b
        if match.a > prev_start+len(b):
            continue
        if match.a > prev_end:
            corrected += a[prev_end:match.a]
        
        # 添加匹配的部分
        corrected += a[match.a:match.a + match.size]
        prev_end = match.a + match.size
    
    return corrected

def add_newlines(text, max_length):
    """在指定长度处添加换行符"""
    result = []
    for i in range(0, len(text), max_length):
        result.append(text[i:i + max_length])
    return '\n'.join(result)
class JyAudioTrack:
    """
    音频轨道
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio_group":("AUDIO_GROUP",),
                "track_name": ("STRING",{"default": "audio","tooltip": "轨道名称"}),
            }
        }

    RETURN_TYPES = ("TRACK",)
    RETURN_NAMES = ("轨道",)

    OUTPUT_NODE = False     #是否为输出节点

    FUNCTION = "get_track"

    CATEGORY = "lam"

    def get_track(self, audio_group, track_name):
        track={"track_type": draft.Track_type.audio,"track_name":track_name,"group":audio_group}
        return (track,)
    
class JyMediaTrack:
    """
    视频/图片轨道
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "meida_group":("MEIDA_GROUP",),
                "track_name": ("STRING",{"default": "audio","tooltip": "轨道名称"}),
            }
        }

    RETURN_TYPES = ("TRACK",)
    RETURN_NAMES = ("轨道",)

    OUTPUT_NODE = False     #是否为输出节点

    FUNCTION = "get_track"

    CATEGORY = "lam"

    def get_track(self, meida_group, track_name):
        track={"track_type": draft.Track_type.video,"track_name":track_name,"group":meida_group}
        return (track,)
    
class JyCaptionsTrack:
    """
    字幕轨道
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "captions_group":("CAPTIONS_GROUP",),
                "track_name": ("STRING",{"default": "audio","tooltip": "轨道名称"}),
            }
        }

    RETURN_TYPES = ("TRACK",)
    RETURN_NAMES = ("轨道",)

    OUTPUT_NODE = False     #是否为输出节点

    FUNCTION = "get_track"

    CATEGORY = "lam"

    def get_track(self, captions_group, track_name):
        track={"track_type": draft.Track_type.text,"track_name":track_name,"group":captions_group}
        return (track,)
    
class JyEffectTrack:
    """
    特效轨道
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "effect_group":("EFFECT_GROUP",),
                "track_name": ("STRING",{"default": "audio","tooltip": "轨道名称"}),
            }
        }

    RETURN_TYPES = ("TRACK",)
    RETURN_NAMES = ("轨道",)

    OUTPUT_NODE = False     #是否为输出节点

    FUNCTION = "get_track"

    CATEGORY = "lam"

    def get_track(self, effect_group, track_name):
        track={"track_type": draft.Track_type.effect,"track_name":track_name,"group":effect_group}
        return (track,)
    
class JyMediaAnimation:
    """
    带动画图片/视频
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING",{"default": "","tooltip": "图片/视频地址"}),
                "start_in_media": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "视频开始时间（秒）"}),
                "start_at_track": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "草稿添加时间（秒）"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
                "volume": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 20.0, "step": 0.01,"tooltip": "音量"}),
            },
            "optional": {
                "meida_group":("MEIDA_GROUP",),
                "animation_in":("ANIMATION_IN",),
                "animation_group":("ANIMATION_GROUP",),
                "animation_out":("ANIMATION_OUT",),
            }
        }

    RETURN_TYPES = ("MEIDA","MEIDA_GROUP",)
    RETURN_NAMES = ("带动画图片/视频","图片/视频组",)

    OUTPUT_NODE = False     #是否为输出节点

    FUNCTION = "animation_video"

    CATEGORY = "lam"

    def animation_video(self, file_path, start_in_media, start_at_track, duration,volume,meida_group=[], animation_in=None, animation_group=None, animation_out=None):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        meida_group=[*meida_group]
        animation_datas = []
        if animation_in:
            animation_datas.append(animation_in)
        if animation_group:
            animation_datas.append(animation_group)
        if animation_out:
            animation_datas.append(animation_out)
        meida={"media_file_full_name": file_path, "start_in_media": int(start_in_media*1000000), "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000),"volume":volume, "animation_datas": animation_datas}
        meida_group.append(meida)
        return (meida,meida_group,)

class JyMediaNative:
    """
    不带动画图片/视频
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING",{"default": "","tooltip": "图片/视频地址"}),
                "start_in_media": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "视频开始时间（秒）"}),
                "start_at_track": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "草稿添加时间（秒）"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
                "volume": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 20.0, "step": 0.01,"tooltip": "音量"}),
            },
            "optional": {
                "meida_group":("MEIDA_GROUP",)
            }
        }

    RETURN_TYPES = ("MEIDA","MEIDA_GROUP",)
    RETURN_NAMES = ("图片/视频","图片/视频组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_media"

    CATEGORY = "lam"

    def jy_media(self, file_path, start_in_media, start_at_track, duration,volume,meida_group=[]):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        meida_group=[*meida_group]
        meida={"media_file_full_name": file_path, "start_in_media": int(start_in_media*1000000), "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000),"volume":volume}
        meida_group.append(meida)
        return (meida,meida_group,)

class JyAudioNative:
    """
    音频
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING",{"default": "","tooltip": "音频地址"}),
                "start_in_media": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "音频开始时间（秒）"}),
                "start_at_track": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "草稿添加时间（秒）"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
                "volume": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 20.0, "step": 0.01,"tooltip": "音量"}),
            },
            "optional": {
                "audio_group":("AUDIO_GROUP",)
            }
        }

    RETURN_TYPES = ("JY_AUDIO","AUDIO_GROUP",)
    RETURN_NAMES = ("音频","音频组",)

    OUTPUT_NODE = False
    FUNCTION = "jy_audio"

    CATEGORY = "lam"

    def jy_audio(self, file_path, start_in_media, start_at_track, duration,volume,audio_group=[]):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        audio_group=[*audio_group]
        audio={"media_file_full_name": file_path, "start_in_media": int(start_in_media*1000000), "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000),"volume":volume}
        audio_group.append(audio)
        return (audio,audio_group,)

class JyCaptionsNative:
    """
    字幕
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"default": "","multiline": True,"tooltip": "字幕内容"}),
                "font":(draft.Font_type.get_all_names(),{"default": "宋体","tooltip": "字体"}),
                "color": ("STRING",{"default": "#FFFFFF","tooltip": "字幕颜色"}),
                "size": ("FLOAT", {"default": 8.0, "min": 0.0, "max":300, "step": 1.0,"tooltip": "字幕大小"}),
                "transform_x": ("FLOAT", {"default": 0.0, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "水平位移, 单位为半个画布宽"}),
                "transform_y": ("FLOAT", {"default": -0.8, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "垂直位移, 单位为半个画布高"}),
                "start_at_track": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "草稿添加时间（秒）"}),
                "duration": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
                "row_max_size": ("INT", {"default": 16, "min": 1, "max": 1000, "step": 1,"tooltip": "行最大字符数, 单句超过将自动换行"}),
            },
            "optional": {
                "captions_group":("CAPTIONS_GROUP",)
            }
        }

    RETURN_TYPES = ("JY_CAPTIONS","CAPTIONS_GROUP",)
    RETURN_NAMES = ("字幕","字幕组",)

    OUTPUT_NODE = False
    FUNCTION = "jy_captions"

    CATEGORY = "lam"

    def jy_captions(self, text,font, color,size,transform_x,transform_y, start_at_track, duration,row_max_size,captions_group=[]):
        captions_group=[*captions_group]
        captions={"subtitle": add_newlines(text,row_max_size),"font":font,"color":color,"size":size, "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000)}
        captions['clip_settings']={"transform_y":transform_y,"transform_x":transform_x} #draft.Clip_settings()
        captions_group.append(captions)
        return (captions,captions_group,)

class JyEffectNative:
    """
    特效
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "effect": (list(draft.Video_scene_effect_type.get_all_names()),),
                "start_at_track": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "草稿添加时间（秒）"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            },
            "optional": {
                "effect_group":("EFFECT_GROUP",)
            }
        }

    RETURN_TYPES = ("JY_EFFECT","EFFECT_GROUP",)
    RETURN_NAMES = ("特效","特效组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_effect"

    CATEGORY = "lam"

    def jy_effect(self, effect, start_at_track, duration,effect_group=[]):
        #拷贝一份
        effect_group=[*effect_group]
        effect={"effect_name_or_resource_id": effect, "start": int(start_at_track*1000000), "duration": int(duration*1000000)}
        effect_group.append(effect)
        return (effect,effect_group,)


class JyTransition:
    """
    转场
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "transition": (list(Transition_type.get_all_names()),),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
                "meida_out":("MEIDA",),
            },
            "optional": {
                "meida_group":("MEIDA_GROUP",)
            }
        }

    RETURN_TYPES = ("MEIDA","MEIDA_GROUP",)
    RETURN_NAMES = ("图片/视频","图片/视频组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_transition"

    CATEGORY = "lam"

    def jy_transition(self, transition, duration,meida_out,meida_group=[]):
        meida_group=[*meida_group]
        #添加转场
        transition_data = {
            "transition":transition,  # 转场名称（可以是内置的转场名称，也可以是剪映本身的转场资源id）
            "duration":int(duration*1000000),  # 转场持续时间 
        }
        meida_out['transition_data']=transition_data
        meida_group.append(meida_out)
        return (meida_out,meida_group,)
    
class JyAnimationIn:
    """
    入场动画
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "animation": (list(Intro_type.get_all_names()),),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("ANIMATION_IN",)
    RETURN_NAMES = ("入场动画",)
    OUTPUT_NODE = False
    FUNCTION = "jy_animation_in"

    CATEGORY = "lam"

    def jy_animation_in(self, animation, duration):
        return ({
            "animation":animation,  # 动画名称（可以是内置的动画名称，也可以是剪映本身的动画资源id）
            "duration":int(duration*1000000),  # 动画持续时间
            "animation_type":"in",  # 动画类型
        },)

class JyAnimationGroup:
    """
    中间动画
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "animation": (list(Group_animation_type.get_all_names()),),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("ANIMATION_GROUP",)
    RETURN_NAMES = ("中间动画",)
    OUTPUT_NODE = False
    FUNCTION = "jy_animation_group"

    CATEGORY = "lam"

    def jy_animation_group(self, animation, duration):
        return ({
            "animation":animation,  # 动画名称（可以是内置的动画名称，也可以是剪映本身的动画资源id）
            "duration":int(duration*1000000),  # 动画持续时间
            "animation_type":"group",  # 动画类型
        },)
    
class JyAnimationOut:
    """
    出场动画
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "animation": (list(Outro_type.get_all_names()),),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("ANIMATION_OUT",)
    RETURN_NAMES = ("出场动画",)
    OUTPUT_NODE = False
    FUNCTION = "jy_animation_out"

    CATEGORY = "lam"

    def jy_animation_out(self, animation, duration):
        return ({
            "animation":animation,  # 动画名称（可以是内置的动画名称，也可以是剪映本身的动画资源id）
            "duration":int(duration*1000000),  # 动画持续时间
            "animation_type":"out",  # 动画类型
        },)
    

class JyMultiMediaGroup:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "meida0": ("MEIDA", ),
            },
            "optional": {
                "meida1": ("MEIDA", ),
            }
        }

    RETURN_TYPES = ("MEIDA_GROUP",)
    FUNCTION = "media_group"
    OUTPUT_NODE = False
    CATEGORY = "lam"

    def media_group(self, **kwargs):
       
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('meida'):
                if type(kwargs[arg]) == list:
                    mediaList.extend(kwargs[arg])
                else:
                    mediaList.append(kwargs[arg])

        return (mediaList, )
    
class JyMultiAudioGroup:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio0": ("JY_AUDIO", ),
            },
            "optional": {
                "audio1": ("JY_AUDIO", ),
            }
        }

    RETURN_TYPES = ("AUDIO_GROUP",)
    FUNCTION = "audio_group"
    OUTPUT_NODE = False
    CATEGORY = "lam"

    def audio_group(self, **kwargs):
       
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('audio'):
                mediaList.append(kwargs[arg])

        return (mediaList, )
    
class JyMultiCaptionsGroup:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "captions0": ("JY_CAPTIONS", ),
            },
            "optional": {
                "captions1": ("JY_CAPTIONS", ),
            }
        }

    RETURN_TYPES = ("CAPTIONS_GROUP",)
    FUNCTION = "captions_group"
    OUTPUT_NODE = False
    CATEGORY = "lam"

    def captions_group(self, **kwargs):
       
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('captions'):
                mediaList.append(kwargs[arg])

        return (mediaList, )
    
class JyMultiEffectGroup:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "effect0": ("JY_EFFECT", ),
            },
            "optional": {
                "effect1": ("JY_EFFECT", ),
            }
        }

    RETURN_TYPES = ("EFFECT_GROUP",)
    FUNCTION = "effect_group"
    OUTPUT_NODE = False
    CATEGORY = "lam"

    def effect_group(self, **kwargs):
       
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('effect'):
                mediaList.append(kwargs[arg])

        return (mediaList, )

class JyAudio2CaptionsGroup:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model":(["tiny","base","small","medium","large-v1","large-v2","large-v3"],{"default": "medium"}),
                "file_path": ("STRING",{"default": "","tooltip": "音频地址"}),
                "start_at_track": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "草稿添加时间（秒）"}),
                "font":(draft.Font_type.get_all_names(),{"default": "宋体","tooltip": "字体"}),
                "color": ("STRING",{"default": "#FFFFFF","tooltip": "字幕颜色"}),
                "size": ("FLOAT", {"default": 8.0, "min": 0.0, "max":300, "step": 1.0,"tooltip": "字幕大小"}),
                "transform_x": ("FLOAT", {"default": 0.0, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "水平位移, 单位为半个画布宽"}),
                "transform_y": ("FLOAT", {"default": -0.8, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "垂直位移, 单位为半个画布高"}),
                "row_max_size": ("INT", {"default": 16, "min": 1, "max": 1000, "step": 1,"tooltip": "行最大字符数, 单句超过将自动换行"}),
            },
            "optional": {
                "captions_group":("CAPTIONS_GROUP",),
                "all_subtitles":("STRING",{"forceInput": False})
            }
        }

    RETURN_TYPES = ("CAPTIONS_GROUP","STRING","FLOAT",)
    RETURN_NAMES = ("字幕组","文字内容","结束时间",)
    OUTPUT_NODE = False
    FUNCTION = "jy_audio2captions_group"

    CATEGORY = "lam"


    def jy_audio2captions_group(self,model, file_path,start_at_track,font,color,size,transform_x,transform_y,row_max_size=16,captions_group=[],all_subtitles=""):
        import whisper
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        model = whisper.load_model(model)
        result = model.transcribe(file_path)
        segments = result["segments"]
        resultText = result["text"]
        captions_group=[*captions_group]
        end_time=0
        for i in range(len(segments)):
            text = segments[i]["text"]
            # 字幕自动修正
            text = correct_string(all_subtitles,text) if len(all_subtitles)>0 else text
            # 自动换行
            text = add_newlines(segments[i]["text"],row_max_size)
            
            start=start_at_track+segments[i]["start"]
            duration=segments[i]["end"]-segments[i]["start"]
            captions={"subtitle": text,"font":font,"color":color,"size":size, "start_at_track": int(round(start * 100)) * 10000, "duration": int(round(duration * 100)) * 10000}
            captions['clip_settings']= {"transform_y":transform_y,"transform_x":transform_x} #draft.Clip_settings()
            end_time=start+duration
            captions_group.append(captions)
        return (captions_group,resultText,end_time,)

class JySaveDraft:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "medias": ("MEIDA_GROUP", ),
                "draft_name": ("STRING", {"default": "Draft", "tooltip": "保存的草稿名称"}),
                "width": ("INT", {"default": 1920, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿宽"}),
                "height": ("INT", {"default": 1080, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿高"}),
            },
            "optional": {
                "audios": ("AUDIO_GROUP", ),
                "effects": ("EFFECT_GROUP", ),
                "captions": ("CAPTIONS_GROUP", ),
                "track0": ("TRACK", ),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("草稿时长",)
    FUNCTION = "save_draft"
    
    OUTPUT_NODE = True
    CATEGORY = "lam"

    def save_draft(self,medias,draft_name,width,height,audios=[],effects=[],captions=[],**kwargs):
        tracks=[]
        for arg in kwargs:
            if arg.startswith('track'):
                tracks.append(kwargs[arg])
        maxTime,_=self.save_draft_fun(medias,draft_name,width,height,audios,effects,captions,tracks)
        return (maxTime,)
    
    def add_track_medias(self,script,medias,track_name,maxTime,fileList):
        after_segment=None
        for media in medias:
            #meida={"media_file_full_name": file_path, "start_in_media": int(start_in_media*1000000), "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000),"volume":volume, "animation_datas": animation_datas}
            v_material= None
            if media["duration"]==0:
                v_material=draft.Video_material(media["media_file_full_name"])

            target_timerange=trange(media["start_at_track"],v_material.duration if v_material else media["duration"])
            if media["start_at_track"]<=0:
                if after_segment:
                    target_timerange=trange(after_segment.end,v_material.duration if v_material else media["duration"])
                    
            video_segment = draft.Video_segment(media['media_file_full_name'], target_timerange,volume=media["volume"])
            fileList.append(media['media_file_full_name'])
            #     {
            #     "animation":animation,  # 动画名称（可以是内置的动画名称，也可以是剪映本身的动画资源id）
            #     "duration":int(duration*1000000),  # 动画持续时间
            #     "animation_type":"in",  # 动画类型
            # }
            if "animation_datas" in media:
                for animation in media["animation_datas"]:
                    if animation["animation_type"] == "in":
                        video_segment.add_animation(Intro_type.from_name(animation["animation"]),animation['duration'] if animation['duration']>0 else None)
                    elif animation["animation_type"] == "group":
                        video_segment.add_animation(Group_animation_type.from_name(animation["animation"]),animation['duration'] if animation['duration']>0 else None)
                    elif animation["animation_type"] == "out":
                        video_segment.add_animation(Outro_type.from_name(animation["animation"]),animation['duration'] if animation['duration']>0 else None)
            # transition_data = {
            #     "transition":transition,  # 转场名称（可以是内置的转场名称，也可以是剪映本身的转场资源id）
            #     "duration":int(duration*1000000),  # 转场持续时间 
            # }
            if "transition_data" in media:
                video_segment.add_transition(Transition_type.from_name(media["transition_data"]['transition']),duration=media["transition_data"]['duration'] if media["transition_data"]['duration']>0 else None)
            script.add_segment(video_segment,track_name)
            after_segment=video_segment
            if maxTime<video_segment.end:
                maxTime=video_segment.end
        return maxTime

    def add_track_audios(self,script,audios,track_name,maxTime,fileList):
        after_audio=None
        for audio in audios:
            a_material=None
            if audio["duration"]==0:
                a_material=draft.Audio_material(audio['media_file_full_name'])
            target_timerange=trange(audio["start_at_track"],a_material.duration if a_material else audio["duration"])
            if audio["start_at_track"]<=0:
                if after_audio:
                    target_timerange=trange(after_audio.end,a_material.duration if a_material else audio["duration"])
            
            audio_segment = draft.Audio_segment(audio['media_file_full_name'],
                                target_timerange,  # 片段将位于轨道上的0s-5s（注意5s表示持续时长而非结束时间）
                                volume=audio["volume"])          # 音量设置为60%(-4.4dB)
            fileList.append(audio['media_file_full_name'])
            script.add_segment(audio_segment,track_name)
            after_audio=audio_segment
            if maxTime<audio_segment.end:
                maxTime=audio_segment.end
        return maxTime
    def add_track_captions(self,script,captions,track_name,maxTime):
        # captions={"subtitle": text,"color":color,"size":size, "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000)}
        # captions['clip_settings']=draft.Clip_settings(transform_y=transform_y,transform_x=transform_x)
        after_caption=None
        for caption in captions:
            target_timerange=trange(caption["start_at_track"],caption["duration"])
            if caption["start_at_track"]<=0:
                if after_caption:
                    target_timerange=trange(after_caption.end,caption["duration"])
            r = round(int(caption['color'][1:3], 16)/ 255, 6)
            g = round(int(caption['color'][3:5], 16)/ 255, 6)
            b = round(int(caption['color'][5:7], 16)/ 255, 6)
            text_segment = draft.Text_segment(
                caption["subtitle"], target_timerange,  # 文本片段的首尾与上方视频片段一致
                font=draft.Font_type.from_name(caption['font']),                                      # 设置字体
                style=draft.Text_style(size=float(caption['size']),color=(r,g,b)),                    
                border=draft.Text_border(color=(0, 0, 0.0)),                      # 设置边框颜色为黑色
                clip_settings=draft.Clip_settings(**caption['clip_settings'])     # 位置在屏幕下方
            )
            script.add_segment(text_segment,track_name)
            after_caption=text_segment
            if maxTime<text_segment.end:
                maxTime=text_segment.end
        return maxTime
    def add_track_effects(self,script,effects,track_name,maxTime):
        #effect={"effect_name_or_resource_id": effect, "start": int(start_at_track*1000000), "duration": int(duration*1000000)}
        after_effect=None
        for e in effects:
            target_timerange=trange(e["start"],e["duration"])
            if e["start"]<=0:
                if after_effect:
                    target_timerange=trange(after_effect.end,e["duration"])
                    
            script.add_effect(draft.Video_scene_effect_type.from_name(e['effect_name_or_resource_id']),target_timerange,track_name)
            after_effect=target_timerange
            if maxTime<target_timerange.end:
                maxTime=target_timerange.end
        return maxTime
    def save_draft_fun(self,medias,draft_name,width,height,audios=[],effects=[],captions=[],tracks=[],draft_root=r"C:\Users\Administrator\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft"):
        script = draft.Script_file(draft_name,width,height,draft_root=draft_root)
        maxTime = 0
        fileList=[]
        script.add_track(draft.Track_type.video)
        maxTime=self.add_track_medias(script,medias,draft.Track_type.video.name,maxTime,fileList)
        if len(audios)>0:
            script.add_track(draft.Track_type.audio)
            maxTime=self.add_track_audios(script,audios,draft.Track_type.audio.name,maxTime,fileList)
        if len(captions)>0:
            script.add_track(draft.Track_type.text)
            maxTime=self.add_track_captions(script,captions,draft.Track_type.text.name,maxTime)
        if len(effects)>0:    
            script.add_track(draft.Track_type.effect)
            maxTime=self.add_track_effects(script,effects,draft.Track_type.effect.name,maxTime)
        
        #track={"track_type": draft.Track_type.audio,"track_name":track_name,"group":audio_group}
        for track in tracks:
            script.add_track(track["track_type"],track["track_name"])
            if track["track_type"]==draft.Track_type.video:
                maxTime=self.add_track_medias(script,track["group"],track["track_name"],maxTime,fileList)
            if track["track_type"]==draft.Track_type.audio:
                maxTime=self.add_track_audios(script,track["group"],track["track_name"],maxTime,fileList)
            if track["track_type"]==draft.Track_type.text:
                maxTime=self.add_track_captions(script,track["group"],track["track_name"],maxTime)
            if track["track_type"]==draft.Track_type.effect:
                maxTime=self.add_track_effects(script,track["group"],track["track_name"],maxTime)

        script.save()
        return (maxTime/1000000,fileList)
    
class JySaveNotOutDraft(JySaveDraft):
    OUTPUT_NODE = False

importStr=r"""# -*- coding: utf-8 -*-
import json
import os
import shutil

def replace_text(contentText, data):
    for i in data:
        primary=i["primary"]
        newfile=i["newfile"]
        #获取newfile的绝对路径
        newfile=os.path.abspath(newfile)
        newfile=newfile.replace("\\","/")
        #替换
        contentText=contentText.replace(primary,newfile)
        primary=primary.replace("\\","\\\\")
        contentText=contentText.replace(primary,newfile)
    return contentText

inputPath=input("请输入剪映草稿目录:")
if not inputPath:
    inputPath=r"C:\Users\Administrator\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft/"
#当前目录文件夹名称
folderName=os.path.basename(os.getcwd())
print(f"正在处理“{folderName}”目录下的剪映草稿...")

data=json.load(open("file_counter.json"))
contentText=""
with open("draft_content.json","r",encoding='utf-8') as f:
    contentText=f.read()

with open("draft_content.json","w",encoding='utf-8') as f:
    f.write(replace_text(contentText,data))

with open("draft_meta_info.json","r",encoding='utf-8') as f:
    contentText=f.read()

with open("draft_meta_info.json","w",encoding='utf-8') as f:
    f.write(replace_text(contentText,data))

newDraftsPath=os.path.join(inputPath,folderName)
os.makedirs(newDraftsPath,exist_ok=True)

shutil.copyfile("draft_content.json",os.path.join(newDraftsPath,"draft_content.json"))
shutil.copyfile("draft_meta_info.json",os.path.join(newDraftsPath,"draft_meta_info.json"))"""

importBat='''python importDraft.py
pause
'''
class JySaveOutDraft(JySaveDraft):
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "medias": ("MEIDA_GROUP", ),
                "draft_name": ("STRING", {"default": "Draft", "tooltip": "保存的草稿名称"}),
                "width": ("INT", {"default": 1920, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿宽"}),
                "height": ("INT", {"default": 1080, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿高"}),
            },
            "optional": {
                "audios": ("AUDIO_GROUP", ),
                "effects": ("EFFECT_GROUP", ),
                "captions": ("CAPTIONS_GROUP", ),
                "track0": ("TRACK", ),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("草稿时长",)
    FUNCTION = "save_draft"
    
    OUTPUT_NODE = True
    CATEGORY = "lam"

    def save_draft(self,medias,draft_name,width,height,audios=[],effects=[],captions=[],**kwargs):
        tracks=[]
        for arg in kwargs:
            if arg.startswith('track'):
                tracks.append(kwargs[arg])
        maxTime,fileList=self.save_draft_fun(medias,draft_name,width,height,audios,effects,captions,tracks,draft_root=self.output_dir)
        fileCounter=[]
        folder_to_zip=os.path.join(self.output_dir, draft_name)
        filePath=os.path.join(folder_to_zip, "files")
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        
        for file in fileList:
            #复制文件到当前目录
            newFile=os.path.join(filePath, os.path.basename(file))
            if os.path.exists(newFile):
                newFile=os.path.join(filePath, os.path.splitext(os.path.basename(file))[0]+"_"+str(uuid.uuid4())+os.path.splitext(file)[1])
            shutil.copy(file, newFile)

            fileCounter.append({"primary":file, "newfile":"files/"+os.path.basename(newFile)})
        
        with open(os.path.join(folder_to_zip, "file_counter.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(fileCounter))

        with open(os.path.join(folder_to_zip, "importDraft.py"), "w", encoding="utf-8") as f:
            f.write(importStr)

        with open(os.path.join(folder_to_zip, "导入草稿.bat"), "w", encoding="utf-8") as f:
            f.write(importBat)

        zip_filename=os.path.join(self.output_dir, draft_name+".zip")
        # 创建一个ZipFile对象
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            # os.walk遍历文件夹中的所有文件和子文件夹
            for foldername, subfolders, filenames in os.walk(folder_to_zip):
                for filename in filenames:
                    # 构建完整的文件路径并添加到压缩包中，注意路径的处理以正确反映目录结构
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, folder_to_zip)  # 使用相对路径以保持目录结构
                    zipf.write(file_path, arcname=arcname)
        #删除临时文件夹
        shutil.rmtree(folder_to_zip)
        results=[]
        results.append({
            "filename": draft_name+".zip",
            "subfolder": '',
            "type": self.type
        })
        return {"ui": {"down": results}, "result": (maxTime,)} 
    
class JySaveNoOutDraft(JySaveOutDraft):
    OUTPUT_NODE = False
   

NODE_CLASS_MAPPINGS = {
    "JyAudioTrack":JyAudioTrack,
    "JyMediaTrack":JyMediaTrack,
    "JyCaptionsTrack":JyCaptionsTrack,
    "JyEffectTrack":JyEffectTrack,
    "JyMediaAnimation": JyMediaAnimation,
    "JyMediaNative":JyMediaNative,
    "JyAudioNative":JyAudioNative,
    "JyCaptionsNative":JyCaptionsNative,
    "JyEffectNative":JyEffectNative,
    "JyTransition":JyTransition,
    "JyAnimationIn":JyAnimationIn,
    "JyAnimationGroup":JyAnimationGroup,
    "JyAnimationOut":JyAnimationOut,
    "JyMultiMediaGroup":JyMultiMediaGroup,
    "JyMultiAudioGroup":JyMultiAudioGroup,
    "JyMultiCaptionsGroup":JyMultiCaptionsGroup,
    "JyMultiEffectGroup":JyMultiEffectGroup,
    "JyAudio2CaptionsGroup":JyAudio2CaptionsGroup,
    "JySaveDraft":JySaveDraft,
    "JySaveOutDraft":JySaveOutDraft,
    "JySaveNotOutDraft":JySaveNotOutDraft,
    "JySaveNoOutDraft":JySaveNoOutDraft,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JyAudioTrack": "剪映音频轨道",
    "JyMediaTrack": "剪映图片/视频轨道",
    "JyCaptionsTrack": "剪映字幕轨道",
    "JyEffectTrack": "剪映特效轨道",
    "JyMediaAnimation": "剪映带动画图片/视频",
    "JyMediaNative": "剪映图片/视频",
    "JyAudioNative": "剪映音频",
    "JyCaptionsNative": "剪映字幕",
    "JyEffectNative": "剪映特效",
    "JyTransition": "剪映转场",
    "JyAnimationIn": "入场动画",
    "JyAnimationGroup": "组动画",
    "JyAnimationOut": "出场动画",
    "JyMultiMediaGroup": "图片/视频组",
    "JyMultiAudioGroup": "音频组",
    "JyMultiCaptionsGroup": "字幕组",
    "JyMultiEffectGroup": "特效组",
    "JyAudio2CaptionsGroup": "音频转字幕组",
    "JySaveDraft": "保存草稿",
    "JySaveOutDraft": "临时保存下载",
    "JySaveNotOutDraft":"保存草稿非输出",
    "JySaveNoOutDraft":"临时保存下载非输出",
}
