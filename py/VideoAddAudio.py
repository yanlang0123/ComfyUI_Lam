import folder_paths
import cv2
import os
import torch
import numpy as np

class VideoAddAudio:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'video')
        if not os.path.exists(self.output_dir):
            os .makedirs(self.output_dir)
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                        "videoPath": ("STRING", {"forceInput": True}),
                        "audioPath": ("STRING", {"forceInput": True}),
                        "filename_prefix": ("STRING", {"default": "comfyUI"}),
                    },
                }

    CATEGORY = "lam"
    RETURN_TYPES = ()
    FUNCTION = "video_add_audio"
    OUTPUT_NODE = True

    def video_add_audio(self, videoPath,audioPath,filename_prefix):
        if os.path.exists(videoPath) == False:
            raise Exception('视频文件不存在')
        if os.path.exists(audioPath) == False:
            raise Exception('音频文件不存在')
        _ext_video = os.path.basename(videoPath).strip().split('.')[-1]
        _ext_audio = os.path.basename(audioPath).strip().split('.')[-1]
        if _ext_audio not in ['mp3', 'wav']:
            raise Exception('只支持mp3和wav格式的音频')
        _codec = 'copy'
        if _ext_audio == 'wav':
            _codec = 'aac'
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        file = f"{filename}_{counter:05}_.mp4"
        result=os.path.join(full_output_folder, file)
        #插入音频
        cmd = r'ffmpeg -y -hide_banner -loglevel error -i "%s" -i "%s" -vcodec copy "%s"' % (videoPath, audioPath, result)
        os.system(cmd)  
        return {"ui": {"text": ["视频插入音频成功，保存路径："+result],
        'videos':[{'filename':file,'type':'output','subfolder':'video'}]}}

NODE_CLASS_MAPPINGS = {
    "VideoAddAudio": VideoAddAudio
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoAddAudio": "视频插入音频"
}
