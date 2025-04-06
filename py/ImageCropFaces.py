
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageChops, ImageFont
import numpy as np
import os
import torch
from lam_tools import tensor2pil,pil2tensor
import folder_paths
try:
    from insightface.app import FaceAnalysis
    IS_INSIGHTFACE_INSTALLED = True
except ImportError:
    pass
THRESHOLDS = { # from DeepFace
        "VGG-Face": {"cosine": 0.68, "euclidean": 1.17, "L2_norm": 1.17},
        "Facenet": {"cosine": 0.40, "euclidean": 10, "L2_norm": 0.80},
        "Facenet512": {"cosine": 0.30, "euclidean": 23.56, "L2_norm": 1.04},
        "ArcFace": {"cosine": 0.68, "euclidean": 4.15, "L2_norm": 1.13},
        "Dlib": {"cosine": 0.07, "euclidean": 0.6, "L2_norm": 0.4},
        "SFace": {"cosine": 0.593, "euclidean": 10.734, "L2_norm": 1.055},
        "OpenFace": {"cosine": 0.10, "euclidean": 0.55, "L2_norm": 0.55},
        "DeepFace": {"cosine": 0.23, "euclidean": 64, "L2_norm": 0.64},
        "DeepID": {"cosine": 0.015, "euclidean": 45, "L2_norm": 0.17},
        "GhostFaceNet": {"cosine": 0.65, "euclidean": 35.71, "L2_norm": 1.10},
    }
INSIGHTFACE_DIR = os.path.join(folder_paths.models_dir, "insightface")
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

class InsightFace:
    def __init__(self, provider="CPU", name="buffalo_l"):
        self.face_analysis = FaceAnalysis(name=name, root=INSIGHTFACE_DIR, providers=[provider + 'ExecutionProvider',])
        self.face_analysis.prepare(ctx_id=0, det_size=(640, 640))
        self.thresholds = THRESHOLDS["ArcFace"]

    def get_face(self, image):
        for size in [(size, size) for size in range(640, 256, -64)]:
            self.face_analysis.det_model.input_size = size
            faces = self.face_analysis.get(image)
            if len(faces) > 0:
                return sorted(faces, key=lambda x:(x['bbox'][2]-x['bbox'][0])*(x['bbox'][3]-x['bbox'][1]), reverse=True)
        return None

    def get_embeds(self, image):
        face = self.get_face(image)
        if face is not None:
            face = face[0].normed_embedding
        return face
    
    def get_bbox(self, image, padding=0, padding_percent=0):
        faces = self.get_face(np.array(image))
        img = []
        x = []
        y = []
        w = []
        h = []
        for face in faces:
            x1, y1, x2, y2 = face['bbox']
            width = x2 - x1
            height = y2 - y1
            x1 = int(max(0, x1 - int(width * padding_percent) - padding))
            y1 = int(max(0, y1 - int(height * padding_percent) - padding))
            x2 = int(min(image.width, x2 + int(width * padding_percent) + padding))
            y2 = int(min(image.height, y2 + int(height * padding_percent) + padding))
            crop = image.crop((x1, y1, x2, y2))
            img.append(T.ToTensor()(crop).permute(1, 2, 0).unsqueeze(0))
            x.append(x1)
            y.append(y1)
            w.append(x2 - x1)
            h.append(y2 - y1)
        return (img, x, y, w, h)
    
    def get_keypoints(self, image):
        face = self.get_face(image)
        if face is not None:
            shape = face[0]['kps']
            right_eye = shape[0]
            left_eye = shape[1]
            nose = shape[2]
            left_mouth = shape[3]
            right_mouth = shape[4]
            
            return [left_eye, right_eye, nose, left_mouth, right_mouth]
        return None

    def get_landmarks(self, image, extended_landmarks=False):
        face = self.get_face(image)
        if face is not None:
            shape = face[0]['landmark_2d_106']
            landmarks = np.round(shape).astype(np.int64)

            main_features = landmarks[33:]
            left_eye = landmarks[87:97]
            right_eye = landmarks[33:43]
            eyes = landmarks[[*range(33,43), *range(87,97)]]
            nose = landmarks[72:87]
            mouth = landmarks[52:72]
            left_brow = landmarks[97:106]
            right_brow = landmarks[43:52]
            outline = landmarks[[*range(33), *range(48,51), *range(102, 105)]]
            outline_forehead = outline

            return [landmarks, main_features, eyes, left_eye, right_eye, nose, mouth, left_brow, right_brow, outline, outline_forehead]
        return None    
class FaceAnalysisModels:
    @classmethod
    def INPUT_TYPES(s):
        libraries = []
        if IS_INSIGHTFACE_INSTALLED:
            libraries.append("insightface")
            libraries.append("auraface")

        return {"required": {
            "library": (libraries, ),
            "provider": (["CPU", "CUDA", "DirectML", "OpenVINO", "ROCM", "CoreML"], ),
        }}

    RETURN_TYPES = ("ANALYSIS_MODELS", )
    FUNCTION = "load_models"
    CATEGORY = "FaceAnalysis"

    def load_models(self, library, provider):
        out = {}

        if library == "insightface":
            out = InsightFace(provider=provider)
        elif library == "auraface":
            out = InsightFace(provider=provider, name="auraface")

        return (out, )
    
NODE_CLASS_MAPPINGS = {
    "LamFaceAnalysisModels": FaceAnalysisModels,
    "ImageCropFaces": ImageCropFaces
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "LamFaceAnalysisModels": "人脸分析模型",
    "ImageCropFaces": "多人面部裁剪"
}
