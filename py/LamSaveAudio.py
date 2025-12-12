import folder_paths
import random
import os
from comfy_api.latest import IO,UI

class LamSaveAudio():
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "audio": ("AUDIO", ),
                            "filename_prefix": ("STRING", {"default": "audio/ComfyUI"}),
                            "quality": (["V0", "128k", "320k"], {"default": "V0"}),
                            },
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("audio_path",)  #返回参数名称

    FUNCTION = "save_audio_out"

    OUTPUT_NODE = False

    CATEGORY = "lam"
    def save_audio_out(self, audio, filename_prefix="ComfyUI", format="mp3", prompt=None, extra_pnginfo=None, quality="128k"):
        results=UI.AudioSaveHelper.save_audio(
                audio,
                filename_prefix=filename_prefix,
                folder_type=IO.FolderType.output,
                cls=None,
                format=format,quality=quality)
        paths=[]
        for  i in range(len(results)):
            subfolder=results[i]['subfolder']
            if  subfolder:
                path=os.path.join(self.output_dir, results[i]['subfolder'],results[i]['filename'])
            else:
                path=os.path.join(self.output_dir, results[i]['filename'])

            paths.append(path)

        return (paths[0] if len(paths)>0 else '',)
    
NODE_CLASS_MAPPINGS = { #节点名称与类名对应关系
    "LamSaveAudio": LamSaveAudio,
}

NODE_DISPLAY_NAME_MAPPINGS = { #节点名称与显示名称对应关系
    "LamSaveAudio": "保存音频输出",
}
