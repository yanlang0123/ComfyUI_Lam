from comfy_extras.nodes_video import SaveVideo
import folder_paths
import random
import os
from typing import Optional, Literal
from comfy.comfy_types import IO, FileLocator, ComfyNodeABC
from comfy_api.input import ImageInput, AudioInput, VideoInput
from comfy_api.util import VideoContainer, VideoCodec, VideoComponents

class LamSaveVideo(SaveVideo):
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type: Literal["output"] = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video": (IO.VIDEO, {"tooltip": "The video to save."}),
                "filename_prefix": ("STRING", {"default": "video/ComfyUI", "tooltip": "The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes."}),
                "format": (VideoContainer.as_input(), {"default": "auto", "tooltip": "The format to save the video as."}),
                "codec": (VideoCodec.as_input(), {"default": "auto", "tooltip": "The codec to use for the video."}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_path",)  #返回参数名称

    FUNCTION = "save_audio_out"

    OUTPUT_NODE = False

    CATEGORY = "lam"
    def save_audio_out(self, video: VideoInput, filename_prefix, format, codec, prompt=None, extra_pnginfo=None):
        data=super().save_video(video, filename_prefix, format, codec, prompt, extra_pnginfo)
        results=data['ui']['images']
        paths=[]
        for  i in range(len(results)):
            subfolder=results[i]['subfolder']
            if  subfolder:
                path=os.path.join(self.output_dir, results[i]['subfolder'],results[i]['filename'])
            else:
                path=os.path.join(self.output_dir, results[i]['filename'])

            paths.append(path)

        data['result']=(paths[0] if len(paths)>0 else '',)
        return data
    
NODE_CLASS_MAPPINGS = { #节点名称与类名对应关系
    "LamSaveVideo": LamSaveVideo,
}

NODE_DISPLAY_NAME_MAPPINGS = { #节点名称与显示名称对应关系
    "LamSaveVideo": "保存视频输出",
}
