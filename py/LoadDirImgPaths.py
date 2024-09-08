import os

class LoadDirImgPaths:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_img_dir": ("STRING",{"default": ""}),
            }
        }
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("图片路径列表",)
    FUNCTION = "get_img_paths"

    CATEGORY = "lam"

    def get_img_paths(self,input_img_dir):
        if not os.path.exists(input_img_dir):
            raise Exception('路径不存在')
        files_name=[]
        for root, dirs, files in os.walk(input_img_dir):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff')):
                    files_name.append(os.path.join(root, file))

        return (files_name, )

NODE_CLASS_MAPPINGS = {
    "LoadDirImgPaths": LoadDirImgPaths
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadDirImgPaths": "获取路径图片地址"
}
