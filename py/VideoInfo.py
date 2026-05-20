import os
import cv2

class VideoInfo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("FLOAT", "INT", "INT", "INT", "INT",)
    RETURN_NAMES = ("视频时长（秒）", "视频总帧数", "视频帧率（FPS）", "视频宽度", "视频高度")

    FUNCTION = "get_video_info"
    CATEGORY = "lam"

    def get_video_info(self, video_path):
        if not os.path.exists(video_path):
            raise ValueError("File does not exist")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        duration = 0.0
        if fps > 0:
            duration = float(frame_count) / float(fps)
        
        cap.release()
        
        return (duration, int(frame_count), int(fps), width, height,)

NODE_CLASS_MAPPINGS = {
    "VideoInfo": VideoInfo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoInfo": "获取视频信息"
}
