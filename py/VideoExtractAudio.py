import folder_paths
import os
import numpy as np

class VideoExtractAudio:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'audio')
        if not os.path.exists(self.output_dir):
            os .makedirs(self.output_dir)
    @classmethod
    def INPUT_TYPES(s):
        input_dir = os.path.join(folder_paths.get_input_directory(), 'video')
        
        if not os.path.exists(input_dir):
            os .makedirs(input_dir)
        return {"required":
                    {
                    "videoPath": ("STRING", {"forceInput": True}),
                    "filename_prefix": ("STRING", {"default": "comfyUI"}),
                    },
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("音频地址",)
    FUNCTION = "load_image"
    OUTPUT_NODE = False

    def load_image(self, videoPath,filename_prefix):
        if os.path.exists(videoPath) == False:
            raise Exception('视频文件不存在')
    
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        file = f"{filename}_{counter:05}_.mp3"
        filePathName=os.path.join(full_output_folder, file)
        #提取音频
        cmd = r"ffmpeg -y -hide_banner -loglevel error -i %s %s"%(videoPath, filePathName)
        os.system(cmd)  
        return (filePathName,)

NODE_CLASS_MAPPINGS = {
    "VideoExtractAudio": VideoExtractAudio
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoExtractAudio": "视频提取音频"
}
