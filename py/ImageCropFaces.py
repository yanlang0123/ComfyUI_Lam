
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageChops, ImageFont
import numpy as np
import os
import torch
from lam_tools import tensor2pil,pil2tensor
# Tensor to PIL
#获取组节点
confdir = os.path.abspath(os.path.join(__file__, "../../config"))
if not os.path.exists(confdir):
    os.mkdir(confdir)

def solid_mask(value, width, height):
    out = torch.full((1, height, width), value,
                     dtype=torch.float32, device="cpu")
    return out


def mask_combine(destination, source, x, y, operation="add"):
    output = destination.reshape(
        (-1, destination.shape[-2], destination.shape[-1])).clone()
    source = source.reshape((-1, source.shape[-2], source.shape[-1]))

    left, top = (x, y,)
    right, bottom = (min(left + source.shape[-1], destination.shape[-1]), min(
        top + source.shape[-2], destination.shape[-2]))
    visible_width, visible_height = (right - left, bottom - top,)

    source_portion = source[:, :visible_height, :visible_width]
    destination_portion = destination[:, top:bottom, left:right]

    if operation == "multiply":
        output[:, top:bottom, left:right] = destination_portion * source_portion
    elif operation == "add":
        output[:, top:bottom, left:right] = destination_portion + source_portion
    elif operation == "subtract":
        output[:, top:bottom, left:right] = destination_portion - source_portion
    elif operation == "and":
        output[:, top:bottom, left:right] = torch.bitwise_and(
            destination_portion.round().bool(), source_portion.round().bool()).float()
    elif operation == "or":
        output[:, top:bottom, left:right] = torch.bitwise_or(
            destination_portion.round().bool(), source_portion.round().bool()).float()
    elif operation == "xor":
        output[:, top:bottom, left:right] = torch.bitwise_xor(
            destination_portion.round().bool(), source_portion.round().bool()).float()

    output = torch.clamp(output, 0.0, 1.0)
    return output

def zero_for_non_zero(num):
    return 0 if num < 0 else num

class ImageCropFaces:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "analysis_models": ("ANALYSIS_MODELS", ),
                "image": ("IMAGE",),
                "crop_padding_factor": ("FLOAT", {"default": 0.25, "min": 0.0, "max": 2.0, "step": 0.01}),
                }
        }
    
    RETURN_TYPES = ("IMAGE", "MASKS","BOXS",)
    FUNCTION = "image_crop_face"
    
    CATEGORY = "lam"
    
    def image_crop_face(self,analysis_models,image, crop_padding_factor=0.25):
        return self.crop_face(tensor2pil(image),analysis_models,crop_padding_factor)
    
    def crop_face(self, image, analysis_models, padding=0.25):
    
        import cv2
        
        img = np.array(image.convert('RGB'))

        faces=[]
        if not isinstance(analysis_models, dict):
            if type(analysis_models).__name__=='InsightFace':
                facesData=analysis_models.get_face(np.array(img))
                for face in facesData:
                    x, y, w, h = face.bbox.astype(int)
                    w = w - x
                    h = h - y
                    faces.append([x, y, w, h])
            else:
                facesData = analysis_models.get_face(np.array(img))
                for face in facesData:
                    x, y, w, h = face.left(), face.top(), face.width(), face.height()
                    faces.append([x, y, w, h])
        elif analysis_models["library"] == "insightface":
            facesData = analysis_models["detector"].get(np.array(img))
            for face in facesData:
                x, y, w, h = face.bbox.astype(int)
                w = w - x
                h = h - y
                faces.append([x, y, w, h])

        else:
            facesData = analysis_models["detector"](np.array(img), 1)
            for face in facesData:
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                faces.append([x, y, w, h])
            
        face_imgs=[]
        face_masks=[]
        face_boxs=[]
        one_size=None
        for i, (x, y, w, h) in enumerate(faces):
            if w < 50 and h < 50:
                continue
            # Check if the face region aligns with the edges of the original image
            left_adjust = max(0, -x)
            right_adjust = max(0, x + w - img.shape[1])
            top_adjust = max(0, -y)
            bottom_adjust = max(0, y + h - img.shape[0])

            # Check if the face region is near any edges, and if so, pad in the opposite direction
            if left_adjust < w:
                x += right_adjust
            elif right_adjust < w:
                x -= left_adjust
            if top_adjust < h:
                y += bottom_adjust
            elif bottom_adjust < h:
                y -= top_adjust

            w -= left_adjust + right_adjust
            h -= top_adjust + bottom_adjust
            
            # Calculate padding around face
            face_size = min(h, w)
            y_pad = int(face_size * padding)
            x_pad = int(face_size * padding)
            
            # Calculate square coordinates around face
            center_x = x + w // 2
            center_y = y + h // 2
            half_size = (face_size + max(x_pad, y_pad)) // 2
            top = max(0, center_y - half_size)
            bottom = min(img.shape[0], center_y + half_size)
            left = max(0, center_x - half_size)
            right = min(img.shape[1], center_x + half_size)
            
            # Ensure square crop of the original image
            crop_size = min(right - left, bottom - top)
            if center_x<crop_size // 2 or center_y<crop_size // 2:
                crop_size=min(center_x,center_y)*2

            left = center_x - crop_size // 2
            right = center_x + crop_size // 2
            top = center_y - crop_size // 2
            bottom = center_y + crop_size // 2
            
            # Crop face from original image
            face_img = img[top:bottom, left:right, :]
            
            # Resize image
            size = max(face_img.copy().shape[:2])
            pad_h = (size - face_img.shape[0]) // 2
            pad_w = (size - face_img.shape[1]) // 2
            face_img = cv2.copyMakeBorder(face_img, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_CONSTANT, value=[0,0,0])
            min_size = 64 # Set minimum size for padded image
            if size < min_size:
                size = min_size
            face_img = cv2.resize(face_img, (size, size))
            
            # Convert numpy array back to PIL image
            face_img = Image.fromarray(face_img)

            # Resize image to a multiple of 64
            original_size = face_img.size
            if one_size is None:
                one_size = (((face_img.size[0] // 64) * 64 + 64), ((face_img.size[1] // 64) * 64 + 64))

            face_img=face_img.resize(one_size)

            face_imgs.append(pil2tensor(face_img.convert('RGB')))
            
            face_boxs.append([original_size[1], original_size[0],left, top])

            destination = solid_mask(0.0, img.shape[1], img.shape[0])
            source = solid_mask(1.0, original_size[1], original_size[0])
            face_masks.append(mask_combine(destination, source,left, top, operation="add"))
        
        if len(face_imgs)<=0:
            image = Image.new(mode="RGB", size=(64, 64),color=(255, 255, 255))
            face_imgs.append(torch.from_numpy(np.array(image).astype(np.float32) / 255.0))
        
        
        # Return face image and coordinates
        return (torch.stack(face_imgs), face_masks ,face_boxs, )
    

NODE_CLASS_MAPPINGS = {
    "ImageCropFaces": ImageCropFaces
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageCropFaces": "多人面部裁剪"
}
