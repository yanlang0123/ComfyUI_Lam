from PIL import Image
import numpy as np
import torch
import os
import folder_paths
from .src.utils.uitls import AlwaysEqualProxy,AlwaysTupleZero

class RoleManagement:
    def __init__(self):
        self.input_role_dir = os.path.join(folder_paths.get_input_directory(), 'role')
        if not os.path.exists(self.input_role_dir):
            os .makedirs(self.input_role_dir)

    @classmethod
    def INPUT_TYPES(cls):
        input_role_dir = os.path.join(folder_paths.get_input_directory(), 'role')
        if not os.path.exists(input_role_dir):
            os .makedirs(input_role_dir)
        files = [f for f in os.listdir(input_role_dir) if os.path.isdir(os.path.join(input_role_dir, f))]
        return {
            "required": {
                "role": (sorted(files), ),
            }
        }
    RETURN_TYPES = AlwaysTupleZero(AlwaysEqualProxy("*"),) #"IMAGE","IMAGE","STRING",
    RETURN_NAMES = ("调试参数",) #"脸部图","姿态图","表情",
    FUNCTION = "get_role"

    CATEGORY = "lam"

    def get_role(self, **kwargs):
        params = {}
        for arg in kwargs:
            params[arg] = kwargs[arg]
        #video_path = folder_paths.get_annotated_filepath(video,self.input_role_dir)
        return (params, )

NODE_CLASS_MAPPINGS = {
    "RoleManagement": RoleManagement
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "RoleManagement": "角色管理"
}
