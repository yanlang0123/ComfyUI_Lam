import folder_paths
import cv2
import os
import torch
import numpy as np
from ffmpy import FFmpeg

class LamLoadVideo:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'autio')
        if not os.path.exists(self.output_dir):
            os .makedirs(self.output_dir)
    @classmethod
    def INPUT_TYPES(s):
        input_dir = os.path.join(folder_paths.get_input_directory(), 'video')
        
        if not os.path.exists(input_dir):
            os .makedirs(input_dir)
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {
                    "videoPath": ("STRING", {"forceInput": True}),
                    "sample_start_idx": ("INT", {"default": 1, "min": 1, "max": 10000}),
                    "n_sample_frames": ("INT", {"default": 0, "min": 0, "max": 100000}),
                    "extract_audio": ([True,False], ),
                    "filename_prefix": ("STRING", {"default": "comfyUI"}),
                    },
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("IMAGE","INT","INT","STRING",)
    RETURN_NAMES = ("图片","帧率","总帧数","音频文件名",)
    FUNCTION = "load_image"
    OUTPUT_NODE = True

    def load_image(self, videoPath,sample_start_idx,n_sample_frames,extract_audio,filename_prefix):
        if os.path.exists(videoPath) == False:
            raise Exception('视频文件不存在')
        cap = cv2.VideoCapture(videoPath)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        flag = cap.isOpened()
        if not flag:
            print("\033[31mLine 65 error\033[31m: open" + videoPath + "error!")

        sample_frames = []
        count=0
        while True:
            flag, image = cap.read()
            if not flag:  # 如果已经读取到最后一帧则退出
                break
            count+=1
            if sample_start_idx>count:
                continue
            if n_sample_frames>0:
                if (sample_start_idx+n_sample_frames)<=count:
                    break
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            image = image.squeeze()
            sample_frames.append(image)
        cap.release()   # 释放资源
        filePathName=''
        if extract_audio:
            full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
            file = f"{filename}_{counter:05}_.mp3"
            filePathName=os.path.join(full_output_folder, file)
            ff = FFmpeg(inputs={videoPath: None},outputs={filePathName: '-f {} -vn'.format('mp3')})
            ff.run()
        return {"ui": {"text": "音频提取成功，保存路径："+filePathName if extract_audio else '需要提取音频请设置extract_audio为True'}, "result": (torch.stack(sample_frames),fps,frames,filePathName,)}

NODE_CLASS_MAPPINGS = {
    "LamLoadVideo": LamLoadVideo
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "LamLoadVideo": "视频加载"
}
