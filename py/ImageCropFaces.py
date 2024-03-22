
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageChops, ImageFont
import numpy as np
import os
import torch
# Tensor to PIL
#获取组节点
confdir = os.path.abspath(os.path.join(__file__, "../../config"))
if not os.path.exists(confdir):
    os.mkdir(confdir)
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0)

class ImageCropFaces:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "crop_padding_factor": ("FLOAT", {"default": 0.25, "min": 0.0, "max": 2.0, "step": 0.01}),
                "cascade_xml": ([
                                "lbpcascade_animeface.xml",
                                "haarcascade_frontalface_default.xml", 
                                "haarcascade_frontalface_alt.xml", 
                                "haarcascade_frontalface_alt2.xml",
                                "haarcascade_frontalface_alt_tree.xml",
                                "haarcascade_profileface.xml",
                                "haarcascade_upperbody.xml",
                                "haarcascade_eye.xml"
                                ],),
                }
        }
    
    RETURN_TYPES = ("IMAGE", "LIST")
    FUNCTION = "image_crop_face"
    
    CATEGORY = "lam"
    
    def image_crop_face(self, image, cascade_xml=None, crop_padding_factor=0.25):
        return self.crop_face(tensor2pil(image), cascade_xml, crop_padding_factor)
    
    def crop_face(self, image, cascade_name=None, padding=0.25):
    
        import cv2

        img = np.array(image.convert('RGB'))

        face_location = None

        cascades = [ os.path.join(os.path.join(confdir, 'res'), 'lbpcascade_animeface.xml'), 
                    os.path.join(os.path.join(confdir, 'res'), 'haarcascade_frontalface_default.xml'), 
                    os.path.join(os.path.join(confdir, 'res'), 'haarcascade_frontalface_alt.xml'), 
                    os.path.join(os.path.join(confdir, 'res'), 'haarcascade_frontalface_alt2.xml'), 
                    os.path.join(os.path.join(confdir, 'res'), 'haarcascade_frontalface_alt_tree.xml'), 
                    os.path.join(os.path.join(confdir, 'res'), 'haarcascade_profileface.xml'), 
                    os.path.join(os.path.join(confdir, 'res'), 'haarcascade_upperbody.xml') ]
                    
        if cascade_name:
            for cascade in cascades:
                if os.path.basename(cascade) == cascade_name:
                    cascades.remove(cascade)
                    cascades.insert(0, cascade)
                    break

        faces = None
        if not face_location:
            for cascade in cascades:
                if not os.path.exists(cascade):
                    print(f"Unable to find cascade XML file at `{cascade}`. Did you pull the latest files from https://github.com/WASasquatch/was-node-suite-comfyui repo?")
                    return (pil2tensor(Image.new("RGB", (512,512), (0,0,0))), False)
                face_cascade = cv2.CascadeClassifier(cascade)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                if len(faces) != 0:
                    print(f"Face found with: {os.path.basename(cascade)}")
                    break
            if len(faces) == 0:
                print("No faces found in the image!")
                return (pil2tensor(Image.new("RGB", (512,512), (0,0,0))), False)
        else: 
            print("Face found with: face_recognition model")
            faces = face_location
            
        face_imgs=[]
        face_crop_datas=[]
        one_size=None
        for i, (x, y, w, h) in enumerate(faces):
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
            face_crop_datas.append((original_size, (left, top, right, bottom)))
        
        # Return face image and coordinates
        return (torch.stack(face_imgs), face_crop_datas)
    

NODE_CLASS_MAPPINGS = {
    "ImageCropFaces": ImageCropFaces
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageCropFaces": "多人面部裁剪"
}
