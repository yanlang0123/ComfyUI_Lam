from PIL import Image
import numpy as np
import torch
import folder_paths
import os
class AudioPath:
    def __init__(self):
        self.input_audio_dir = folder_paths.get_input_directory()
        if not os.path.exists(self.input_audio_dir):
            os.makedirs(self.input_audio_dir)

    @classmethod
    def INPUT_TYPES(cls):
        input_audio_dir = folder_paths.get_input_directory()
        if not os.path.exists(input_audio_dir):
            os .makedirs(input_audio_dir)
        files = folder_paths.filter_files_content_types(os.listdir(input_audio_dir), ["audio"])
        return {
            "required": {
                "audio": (sorted(files),  {"audio_upload": True} ),
                "audioUI": ("AUDIO_UI", {})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("音频地址",)
    FUNCTION = "get_audio_path"

    CATEGORY = "lam"

    def get_audio_path(self,audio,audioUI=None):
        autio_path = folder_paths.get_annotated_filepath(audio,self.input_audio_dir)
        return (autio_path, )
    
    @classmethod
    def IS_CHANGED(cls, audio,audioUI=None):
        input_audio_dir = folder_paths.get_input_directory()
        audio_path = folder_paths.get_annotated_filepath(audio,input_audio_dir)
        mod_time = os.path.getmtime(audio_path)
        return mod_time


NODE_CLASS_MAPPINGS = {
    "AutioPath": AudioPath
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AutioPath": "获取音频地址"
}
