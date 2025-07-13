from pydub import AudioSegment
import os

class AutioInfo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "autio_path": ("STRING",{"default": ""}),
            }
        }
    
    RETURN_TYPES = ("FLOAT","INT","INT","INT","INT",)
    RETURN_NAMES = ("音频时长（秒）","音频采样率","音频通道数","比特深度（位）","比特率（kbps）")

    FUNCTION = "get_audio_info"
    CATEGORY = "lam"

    def get_audio_info(self,autio_path):
        if not os.path.exists(autio_path):
            raise ValueError("File does not exist")
        
        audio = AudioSegment.from_file(autio_path)
        duration = len(audio) / 1000.0  # 音频时长（秒）
        frame_rate = audio.frame_rate  # 采样率
        channels = audio.channels  # 声道数
        bit_depth = audio.sample_width * 8  # 比特深度（位）
        bit_rate = (audio.frame_rate * audio.channels * audio.sample_width * 8) / 1000  # 比特率（kbps）
        return (duration,frame_rate, channels, bit_depth, bit_rate,)


NODE_CLASS_MAPPINGS = {
    "AutioInfo": AutioInfo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AutioInfo": "获取音频信息"
}
