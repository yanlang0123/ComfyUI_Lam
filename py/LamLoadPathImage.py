from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageChops, ImageFont
import folder_paths
import os 
import numpy as np
import torch
import random
import requests
import io

class LamLoadPathImage:

    def __init__(self):
        self.input_dir = folder_paths.input_directory

    @classmethod
    def INPUT_TYPES(cls):
        return {
                "required": {
                    "image_path": ("STRING", {"default": './ComfyUI/input/example.png', "multiline": False}), 
                    "RGBA": (["false","true"],),
                },
                "optional": {
                    "filename_text_extension": (["true", "false"],),
                }
            }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("image", "mask", "filename_text")
    FUNCTION = "load_image"
    
    CATEGORY = "lam"

    def load_image(self, image_path, RGBA='false', filename_text_extension="true"):
    
        RGBA = (RGBA == 'true')

        if image_path.startswith('http'):
            from io import BytesIO
            i = self.download_image(image_path)
        else:
            try:
                i = Image.open(image_path)
            except OSError:
                print(f"The image `{image_path.strip()}` specified doesn't exist!")
                i = Image.new(mode='RGB', size=(512, 512), color=(0, 0, 0))
        if not i:
            return
            
        image = i
        if not RGBA:
            image = image.convert('RGB')
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
        
        if filename_text_extension == "true":
            filename = os.path.basename(image_path)
        else:
            filename = os.path.splitext(os.path.basename(image_path))[0]
            
        return (image, mask, filename)

    def download_image(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(io.BytesIO(response.content))
            return img
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: ({url}): {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection Error: ({url}): {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: ({url}): {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: ({url}): {err}")

NODE_CLASS_MAPPINGS = {
    "LamLoadPathImage": LamLoadPathImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamLoadPathImage": "加载网络图片或本地图片"
}