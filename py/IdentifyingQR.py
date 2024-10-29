import numpy as np
import cv2
from cv2.wechat_qrcode import WeChatQRCode
import os
def tensor2pil(image):
    return cv2.cvtColor(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR)


class IdentifyingQR:
    def __init__(self):
        modelDir = os.path.abspath(os.path.join(__file__, "../../qr_mode"))
        self.detector = WeChatQRCode(detector_prototxt_path=modelDir+"/detect.prototxt", 
                        detector_caffe_model_path=modelDir+"/detect.caffemodel",
                        super_resolution_prototxt_path=modelDir+"/sr.prototxt",
                          super_resolution_caffe_model_path=modelDir+"/sr.caffemodel")
        
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
        scales = [0.5, 0.75, 1.0, 1.25, 1.5]
        img = tensor2pil(image)
        for scale in scales:
            # 缩放图像
            scaled_image = cv2.resize(img, None, fx=scale, fy=scale)
            # 检测二维码
            res, points = self.detector.detectAndDecode(scaled_image)
            # 如果检测到二维码
            if points:
                print(f'二维码在缩放比例 {scale} 下被检测到')
                return res
        
        return ('',)
    
   
    

NODE_CLASS_MAPPINGS = {
    "IdentifyingQR": IdentifyingQR
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IdentifyingQR": "二维码识别"
}
