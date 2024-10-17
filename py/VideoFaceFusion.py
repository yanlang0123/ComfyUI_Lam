import cv2
import os
import sys
import torch
import model_management
import numpy as np
from .facelib.utils.face_restoration_helper import FaceRestoreHelper
from .facelib.detection.retinaface import retinaface
from .face_fusion.image_face_fusion import ImageFaceFusion
from PIL import Image
import folder_paths
import imageio
from tqdm import tqdm 
from torchvision.transforms.functional import normalize

def img2tensor(imgs, bgr2rgb=True, float32=True):
    """Numpy array to tensor.

    Args:
        imgs (list[ndarray] | ndarray): Input images.
        bgr2rgb (bool): Whether to change bgr to rgb.
        float32 (bool): Whether to change to float32.

    Returns:
        list[tensor] | tensor: Tensor images. If returned results only have
            one element, just return tensor.
    """

    def _totensor(img, bgr2rgb, float32):
        if img.shape[2] == 3 and bgr2rgb:
            if img.dtype == 'float64':
                img = img.astype('float32')
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img.transpose(2, 0, 1))
        if float32:
            img = img.float()
        return img

    if isinstance(imgs, list):
        return [_totensor(img, bgr2rgb, float32) for img in imgs]
    else:
        return _totensor(imgs, bgr2rgb, float32)


def tensor2img(tensor, rgb2bgr=True, out_type=np.uint8, min_max=(0, 1)):
    """Convert torch Tensors into image numpy arrays.

    After clamping to [min, max], values will be normalized to [0, 1].

    Args:
        tensor (Tensor or list[Tensor]): Accept shapes:
            1) 4D mini-batch Tensor of shape (B x 3/1 x H x W);
            2) 3D Tensor of shape (3/1 x H x W);
            3) 2D Tensor of shape (H x W).
            Tensor channel should be in RGB order.
        rgb2bgr (bool): Whether to change rgb to bgr.
        out_type (numpy type): output types. If ``np.uint8``, transform outputs
            to uint8 type with range [0, 255]; otherwise, float type with
            range [0, 1]. Default: ``np.uint8``.
        min_max (tuple[int]): min and max values for clamp.

    Returns:
        (Tensor or list): 3D ndarray of shape (H x W x C) OR 2D ndarray of
        shape (H x W). The channel order is BGR.
    """
    if not (torch.is_tensor(tensor) or (isinstance(tensor, list) and all(torch.is_tensor(t) for t in tensor))):
        raise TypeError(f'tensor or list of tensors expected, got {type(tensor)}')

    if torch.is_tensor(tensor):
        tensor = [tensor]
    result = []
    for _tensor in tensor:
        _tensor = _tensor.squeeze(0).float().detach().cpu().clamp_(*min_max)
        _tensor = (_tensor - min_max[0]) / (min_max[1] - min_max[0])

        n_dim = _tensor.dim()
        if n_dim == 4:
            img_np = make_grid(_tensor, nrow=int(math.sqrt(_tensor.size(0))), normalize=False).numpy()
            img_np = img_np.transpose(1, 2, 0)
            if rgb2bgr:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        elif n_dim == 3:
            img_np = _tensor.numpy()
            img_np = img_np.transpose(1, 2, 0)
            if img_np.shape[2] == 1:  # gray image
                img_np = np.squeeze(img_np, axis=2)
            else:
                if rgb2bgr:
                    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        elif n_dim == 2:
            img_np = _tensor.numpy()
        else:
            raise TypeError('Only support 4D, 3D or 2D tensor. ' f'But received with dimension: {n_dim}')
        if out_type == np.uint8:
            # Unlike MATLAB, numpy.unit8() WILL NOT round by default.
            img_np = (img_np * 255.0).round()
        img_np = img_np.astype(out_type)
        result.append(img_np)
    if len(result) == 1:
        result = result[0]
    return result

class VideoFaceFusion:
    def __init__(self):
        self.face_helper = None
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'video')
        if not os.path.exists(self.output_dir):
            os .makedirs(self.output_dir)

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"templateVideoPath": ("STRING", {"forceInput": True}),
                    "user_image": ("IMAGE", ),
                    "filename_prefix": ("STRING", {"default": "comfyUI"}),
                    },
                "optional": {
                    "facedetection": (["retinaface_resnet50", "retinaface_mobile0.25", "YOLOv5l", "YOLOv5n"],),
                    "upscale_model": ("UPSCALE_MODEL",),
                    }
                }
                

    CATEGORY = "lam"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("视频文件名",)
    OUTPUT_NODE = True

    FUNCTION = "face_fusion"
    def face_fusion(self,templateVideoPath,user_image,filename_prefix,facedetection,upscale_model=None):
        image_face_fusion = ImageFaceFusion(model_dir=folder_paths.models_dir+'/image-face-fusion')
        if upscale_model:
            device = model_management.get_torch_device()
            upscale_model.to(device)
            if self.face_helper is None:
                self.face_helper = FaceRestoreHelper(1, face_size=512, crop_ratio=(1, 1), det_model=facedetection, save_ext='png', use_parse=True, device=device)
        imageu_np=user_image.numpy()
        imau_shape=imageu_np.shape

        if imau_shape[0]<=0:
            return {"ui": {"text": ["替换人脸照片不能为空"]}, "result": ("",)}

        imageu=imageu_np[0]*255
        imageu=np.uint8(imageu)
        cap = cv2.VideoCapture(templateVideoPath)
        fps = cap.get(cv2.CAP_PROP_FPS)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        flag = cap.isOpened()
        if not flag:
            return {"ui": {"text": ["视频打开失败"]}, "result": ("",)}
        image_list=[]
        for frame_idx in tqdm(range(length), '融合进度:'):
        #while True:
            flag, frame_c = cap.read()
            if not flag:  # 如果已经读取到最后一帧则退出
                break
            frame = cv2.cvtColor(frame_c, cv2.COLOR_BGR2RGB) #bgr转rgb
            image=image_face_fusion.inference(frame_c,imageu)
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #bgr转rgb
            image_list.append(image)
            
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, imau_shape[1], imau_shape[0])
        fileTemp = f"{filename}_{counter:05}_temp.mp4"
        videoPathTemp = os.path.join(full_output_folder, fileTemp)
        file = f"{filename}_{counter:05}_.mp4"
        videoPath = os.path.join(full_output_folder, file)
        with imageio.get_writer(videoPathTemp, fps=fps) as video:
            for i in tqdm(range(len(image_list)), '写入进度:'):
                image=image_list[i]
                if upscale_model is None or self.face_helper is None:
                    video.append_data(image)# 写入视频
                    continue

                image = image.squeeze()
                image = image[:, :, ::-1]
                original_resolution = image.shape[0:2]

                self.face_helper.clean_all()
                self.face_helper.read_image(image)
                self.face_helper.get_face_landmarks_5(only_center_face=False, resize=640, eye_dist_threshold=5)
                self.face_helper.align_warp_face()

                restored_face = None
                for idx, cropped_face in enumerate(self.face_helper.cropped_faces):
                    cropped_face_t = img2tensor(cropped_face / 255., bgr2rgb=True, float32=True)
                    normalize(cropped_face_t, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5), inplace=True)
                    cropped_face_t = cropped_face_t.unsqueeze(0).to(device)

                    try:
                        with torch.no_grad():
                            #output = upscale_model(cropped_face_t, w=strength, adain=True)[0]
                            output = upscale_model(cropped_face_t)[0]
                            restored_face = tensor2img(output, rgb2bgr=True, min_max=(-1, 1))
                        del output
                        torch.cuda.empty_cache()
                    except Exception as error:
                        print(f'\tFailed inference for CodeFormer: {error}', file=sys.stderr)
                        restored_face = tensor2img(cropped_face_t, rgb2bgr=True, min_max=(-1, 1))

                    restored_face = restored_face.astype('uint8')
                    self.face_helper.add_restored_face(restored_face)

                self.face_helper.get_inverse_affine(None)

                restored_img = self.face_helper.paste_faces_to_input_image()
                restored_img = restored_img[:, :, ::-1]

                if original_resolution != restored_img.shape[0:2]:
                    restored_img = cv2.resize(restored_img, (0, 0), fx=original_resolution[1]/restored_img.shape[1], fy=original_resolution[0]/restored_img.shape[0], interpolation=cv2.INTER_LINEAR)

                self.face_helper.clean_all()
                video.append_data(restored_img)# 写入视频

        fileAudio = f"{filename}_{counter:05}_temp.mp3"
        audioFilePathName=os.path.join(full_output_folder, fileAudio)
        #提取音频
        cmd = r"ffmpeg -y -hide_banner -loglevel error -i %s %s"%(templateVideoPath, audioFilePathName)
        os.system(cmd)  
        #插入音频
        cmd = r'ffmpeg -y -hide_banner -loglevel error -i "%s" -i "%s" -vcodec copy "%s"' % (videoPathTemp, audioFilePathName, videoPath)
        os.system(cmd)  
        os.remove(videoPathTemp)
        os.remove(audioFilePathName)
        return {"ui": {"text": ["视频保存成功文件地址："+videoPath],
        'videos':[{'filename':file,'type':'output','subfolder':'video'}]}, "result": (videoPath,)}

NODE_CLASS_MAPPINGS = {
    "VideoFaceFusion": VideoFaceFusion
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoFaceFusion": "视频脸部融合"
}
