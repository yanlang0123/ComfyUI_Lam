
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageChops, ImageFont
import numpy as np
from pyzbar.pyzbar import decode
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))


class IdentifyingQR:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "qr_image_2_string"
    
    CATEGORY = "lam"
    
    def qr_image_2_string(self,image):
        import cv2
        img = tensor2pil(image)
        strList=[]
        msg=''
        try:
            # 解码二维码
            for qrcode in decode(img):
                print(qrcode.data.decode('utf-8'))
                strList.append(qrcode.data.decode('utf-8'))
            msg=','.join(strList)
        except Exception as e:
            print(e)
            msg=''
        return (msg,)
    
   
    

NODE_CLASS_MAPPINGS = {
    "IdentifyingQR": IdentifyingQR
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IdentifyingQR": "二维码识别"
}
