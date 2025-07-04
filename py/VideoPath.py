from PIL import Image
import numpy as np
import torch
import os
import folder_paths

class VideoPath:
    def __init__(self):
        self.input_video_dir = folder_paths.get_input_directory()
        if not os.path.exists(self.input_video_dir):
            os .makedirs(self.input_video_dir)

    @classmethod
    def INPUT_TYPES(cls):
        input_video_dir = folder_paths.get_input_directory()
        if not os.path.exists(input_video_dir):
            os .makedirs(input_video_dir)
        files = [f for f in os.listdir(input_video_dir) if os.path.isfile(os.path.join(input_video_dir, f))]
        files = folder_paths.filter_files_content_types(files, ["video"])
        return {
            "required": {
                "video": (sorted(files), {"video_upload": True} ),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("视频地址",)
    FUNCTION = "get_video_path"

    CATEGORY = "lam"

    def get_video_path(self,video):
        video_path = folder_paths.get_annotated_filepath(video,self.input_video_dir)
        return (video_path, )
    
    @classmethod
    def IS_CHANGED(cls, video):
        video_path = folder_paths.get_annotated_filepath(video)
        mod_time = os.path.getmtime(video_path)
        # Instead of hashing the file, we can just use the modification time to avoid
        # rehashing large files.
        return mod_time

    @classmethod
    def VALIDATE_INPUTS(cls, video):
        if not folder_paths.exists_annotated_filepath(video):
            return "Invalid video file: {}".format(video)

        return True

NODE_CLASS_MAPPINGS = {
    "VideoPath": VideoPath
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoPath": "获取视频地址"
}
