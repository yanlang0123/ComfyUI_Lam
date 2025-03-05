
import base64
from PIL import Image
import numpy as np
from io import BytesIO
import torch

class LoadImageBase64:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"image": ("STRING", {"multiline": False})}}

    RETURN_TYPES = ("IMAGE", "MASK")
    CATEGORY = "lam"
    FUNCTION = "load_image"

    def load_image(self, image):
        imgdata = base64.b64decode(image)
        img = Image.open(BytesIO(imgdata))

        if "A" in img.getbands():
            mask = np.array(img.getchannel("A")).astype(np.float32) / 255.0
            mask = 1.0 - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

        img = img.convert("RGB")
        img = np.array(img).astype(np.float32) / 255.0
        img = torch.from_numpy(img)[None,]

        return (img, mask)
    
NODE_CLASS_MAPPINGS = { #节点名称与类名对应关系
    "LamLoadImageBase64": LoadImageBase64,
}

NODE_DISPLAY_NAME_MAPPINGS = { #节点名称与显示名称对应关系
    "LamLoadImageBase64": "Base64图片加载",
}