import folder_paths
from nodes import SaveImage
import random
from PIL import Image,ImageOps
import os
import numpy as np
import json
from PIL.PngImagePlugin import PngInfo
from comfy.cli_args import args

class LamSaveOnly(SaveImage):
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                {
                    "images": ("IMAGE", ), 
                    "filename_prefix": ("STRING", {"default": "ComfyUI"})
                }
                }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def save_images(self, images, filename_prefix="ComfyUI"):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            filename_with_batch_num = filename.replace(
                "%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file),
                     pnginfo=metadata, compress_level=self.compress_level)
            counter += 1
        return (images,)
    
NODE_CLASS_MAPPINGS = {
    "LamSaveOnly": LamSaveOnly
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamSaveOnly": "仅保存图片"
}
