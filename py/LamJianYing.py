from .JianYingDraft.utils.dataStruct import TransitionData, AnimationData
from .JianYingDraft.utils.innerBizTypes import *
from .JianYingDraft.utils import tools
from .JianYingDraft.core.draft import Draft
from .JianYingDraft.core.otherSettings import Clip_settings

import os
import folder_paths
import zipfile
import shutil
import uuid
import json

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
            },
            "optional": {
                "meida_group":("MEIDA_GROUP",),
                "animation_in":("ANIMATION_IN",),
                "animation_group":("ANIMATION_GROUP",),
                "animation_out":("ANIMATION_OUT",),
            }
        }

    RETURN_TYPES = ("ANIMATION_MEIDA","MEIDA_GROUP",)
    RETURN_NAMES = ("带动画图片/视频","图片/视频组",)

    OUTPUT_NODE = False     #是否为输出节点

    FUNCTION = "animation_video"

    CATEGORY = "lam"

    def animation_video(self, file_path, start_in_media, start_at_track, duration,meida_group=[], animation_in:AnimationData=None, animation_group:AnimationData=None, animation_out:AnimationData=None):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        meida_group=[*meida_group]
        animation_datas: list[AnimationData] = []
        if animation_in:
            animation_datas.append(animation_in)
        if animation_group:
            animation_datas.append(animation_group)
        if animation_out:
            animation_datas.append(animation_out)
        meida={"media_file_full_name": file_path, "start_in_media": int(start_in_media*1000000), "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000), "animation_datas": animation_datas}
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

    def jy_media(self, file_path, start_in_media, start_at_track, duration,meida_group=[]):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        meida_group=[*meida_group]
        meida={"media_file_full_name": file_path, "start_in_media": int(start_in_media*1000000), "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000)}
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

    def jy_audio(self, file_path, start_in_media, start_at_track, duration,audio_group=[]):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        audio_group=[*audio_group]
        audio={"media_file_full_name": file_path, "start_in_media": int(start_in_media*1000000), "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000)}
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
                "color": ("STRING",{"default": "#FFFFFF","tooltip": "字幕颜色"}),
                "size": ("FLOAT", {"default": 8.0, "min": 0.0, "max":300, "step": 1.0,"tooltip": "字幕大小"}),
                "transform_x": ("FLOAT", {"default": 0.0, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "水平位移, 单位为半个画布宽"}),
                "transform_y": ("FLOAT", {"default": -0.8, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "垂直位移, 单位为半个画布高"}),
                "start_at_track": ("FLOAT", {"default": 1.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "草稿添加时间（秒）"}),
                "duration": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
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

    def jy_captions(self, text, color,size,transform_x,transform_y, start_at_track, duration,captions_group=[]):
        captions_group=[*captions_group]
        captions={"subtitle": text,"color":color,"size":size, "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000)}
        captions['clip_settings']=Clip_settings(transform_y=transform_y,transform_x=transform_x)
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
                "effect": (list(effectDict.keys()),),
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
                "transition": (list(transitionDict.keys()),),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
                "meida_out":("MEIDA",),
            },
            "optional": {
                "meida_in":("MEIDA",),
                "meida_group":("MEIDA_GROUP",)
            }
        }

    RETURN_TYPES = ("TRANSITION","MEIDA_GROUP",)
    RETURN_NAMES = ("转场","图片/视频组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_transition"

    CATEGORY = "lam"

    def jy_transition(self, transition, duration,meida_out,meida_in=None,meida_group=[]):
        meida_group=[*meida_group]
        #添加转场
        transition_data: TransitionData = tools.generate_transition_data(
            name_or_resource_id=transition,  # 转场名称（可以是内置的转场名称，也可以是剪映本身的转场资源id）
            duration=int(duration*1000000),  # 转场持续时间 
        )
        meida_out['transition_data']=transition_data
        meida_group.append(meida_out)
        transition=[meida_out]
        if meida_in:
            meida_group.append(meida_in)
            transition.append(meida_in)
        return (transition,meida_group,)
    
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
                "animation": (list(animationInDict.keys()),),
                "start": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "入场动画的起始时间永远为0（即便设置了其他起始时间，也会被忽略）(秒)"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("ANIMATION_IN",)
    RETURN_NAMES = ("入场动画",)
    OUTPUT_NODE = False
    FUNCTION = "jy_animation_in"

    CATEGORY = "lam"

    def jy_animation_in(self, animation, start, duration):
        return (tools.generate_animation_data(
            name_or_resource_id=animation,  # 动画名称（可以是内置的动画名称，也可以是剪映本身的动画资源id）
            start=int(start*1000000),  # 入场动画的起始时间永远为0（即便设置了其他起始时间，也会被忽略）。（这是一个相对素材片段的时间，不是时间轴上的绝对时间）
            duration=int(duration*1000000),  # 动画持续时间
            animation_type="in",  # 动画类型
        ),)

class JyAnimationGroup:
    """
    入场动画
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "animation": (list(animationGroupDict.keys()),),
                "start": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "动画开始时间(秒)"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("ANIMATION_GROUP",)
    RETURN_NAMES = ("入场动画",)
    OUTPUT_NODE = False
    FUNCTION = "jy_animation_group"

    CATEGORY = "lam"

    def jy_animation_group(self, animation, start, duration):
        return (tools.generate_animation_data(
            name_or_resource_id=animation,  # 动画名称（可以是内置的动画名称，也可以是剪映本身的动画资源id）
            start=int(start*1000000),  # 动画开始时间
            duration=int(duration*1000000), # 动画持续时间
            animation_type="group",  # 动画类型
        ),)
    
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
                "animation": (list(animationOutDict.keys()),),
                "start": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "出场动画的起始时间永远为0（具体的时间会根据素材片段的长度自动计算)(秒)"}),
                "duration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("ANIMATION_OUT",)
    RETURN_NAMES = ("出场动画",)
    OUTPUT_NODE = False
    FUNCTION = "jy_animation_out"

    CATEGORY = "lam"

    def jy_animation_out(self, animation, start, duration):
        return (tools.generate_animation_data(
            name_or_resource_id=animation,  # 动画名称（可以是内置的动画名称，也可以是剪映本身的动画资源id）
            start=int(start*1000000),  # 出场动画的起始时间永远为0（具体的时间会根据素材片段的长度自动计算）。（这是一个相对素材片段的时间，不是时间轴上的绝对时间）
            duration=int(duration*1000000),  # 动画持续时间
            animation_type="out",  # 动画类型
        ),)
    

class JyMultiMediaGroup:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "meida0": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
            },
            "optional": {
                "meida1": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
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
                "color": ("STRING",{"default": "#FFFFFF","tooltip": "字幕颜色"}),
                "size": ("FLOAT", {"default": 8.0, "min": 0.0, "max":300, "step": 1.0,"tooltip": "字幕大小"}),
                "transform_x": ("FLOAT", {"default": 0.0, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "水平位移, 单位为半个画布宽"}),
                "transform_y": ("FLOAT", {"default": -0.8, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "垂直位移, 单位为半个画布高"}),
            },
            "optional": {
                "captions_group":("CAPTIONS_GROUP",)
            }
        }

    RETURN_TYPES = ("CAPTIONS_GROUP",)
    RETURN_NAMES = ("字幕组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_audio2captions_group"

    CATEGORY = "lam"

    def jy_audio2captions_group(self,model, file_path,start_at_track,color,size,transform_x,transform_y,captions_group=[]):
        import whisper
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        model = whisper.load_model(model)
        result = model.transcribe(file_path)
        segments = result["segments"]
        captions_group=[*captions_group]
        for i in range(len(segments)):
            text = segments[i]["text"]
            start=start_at_track+segments[i]["start"]
            end=segments[i]["end"]
            duration=end-start
            captions={"subtitle": text,"color":color,"size":size, "start_at_track": int(start*1000000), "duration": int(duration*1000000)}
            captions['clip_settings']=Clip_settings(transform_y=transform_y,transform_x=transform_x)
            captions_group.append(captions)
        return (captions_group,)

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
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("草稿时长",)
    FUNCTION = "save_draft"
    
    OUTPUT_NODE = True
    CATEGORY = "lam"

    def save_draft(self,medias,draft_name,width,height,audios=None,effects=None,captions=None):
        draft = Draft(draft_name,width,height)
        mediaList = [m for m in medias]
        if audios:
            mediaList.extend([a for a in audios])
        for m in mediaList:
            draft.add_media(**m)
        
        if effects:
            for e in effects:
                draft.add_effect(**e)
        
        if captions:
            for c in captions:
                draft.add_subtitle(**c)

        draft.save()
        
        timeSize=draft.calc_draft_duration()
        return (timeSize/1000000,)

importStr=r"""import json
import os
import shutil

def replace_text(contentText, data):
    for i in data:
        primary=i["primary"]
        newfile=i["newfile"]
        #获取newfile的绝对路径
        newfile=os.path.abspath(newfile)
        #替换
        contentText.replace(primary,newfile)
    return contentText

inputPath=input("请输入剪映草稿目录:")
if not inputPath:
    inputPath=r"C:\Users\Administrator\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft/"
#当前目录文件夹名称
folderName=os.path.basename(os.getcwd())
print(f"正在处理“{folderName}”目录下的剪映草稿...")

data=json.load(open("file_counter.json"))
contentText=""
with open("draft_content.json","r") as f:
    contentText=f.read()

with open("draft_content.json","w") as f:
    f.write(replace_text(contentText,data))

with open("draft_meta_info.json","r") as f:
    contentText=f.read()

with open("draft_meta_info.json","w") as f:
    f.write(replace_text(contentText,data))

newDraftsPath=os.path.join(inputPath,folderName)
os.makedirs(newDraftsPath,exist_ok=True)

shutil.copyfile("draft_content.json",os.path.join(newDraftsPath,"draft_content.json"))
shutil.copyfile("draft_meta_info.json",os.path.join(newDraftsPath,"draft_meta_info.json"))"""

importBat='''python importDraft.py
pause
'''
class JySaveOutDraft:
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
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("草稿时长",)
    FUNCTION = "save_draft"
    
    OUTPUT_NODE = True
    CATEGORY = "lam"

    def save_draft(self,medias,draft_name,width,height,audios=None,effects=None,captions=None):
        draft = Draft(draft_name,width,height,draft_root=self.output_dir)
        mediaList = [m for m in medias]
        if audios:
            mediaList.extend([a for a in audios])

        fileList=[]
        fileCounter=[]
        for m in mediaList:
            draft.add_media(**m)
            fileList.append(m['media_file_full_name'])
        
        if effects:
            for e in effects:
                draft.add_effect(**e)
        
        if captions:
            for c in captions:
                draft.add_subtitle(**c)
        draft.save()
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
        timeSize=draft.calc_draft_duration()
        results=[]
        results.append({
            "filename": draft_name+".zip",
            "subfolder": '',
            "type": self.type
        })
        return {"ui": {"down": results}, "result": (timeSize/1000000,)} 

NODE_CLASS_MAPPINGS = {
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
}

NODE_DISPLAY_NAME_MAPPINGS = {
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
}
