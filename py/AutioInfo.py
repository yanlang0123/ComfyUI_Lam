import os
import subprocess
import json

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

    def get_audio_info(self, autio_path):
        if not os.path.exists(autio_path):
            raise ValueError(f"File does not exist: {autio_path}")
        
        # 尝试动态查找 ffprobe 路径
        import shutil
        ffprobe_exe = shutil.which("ffprobe")
        if not ffprobe_exe:
            # 常见位置探测
            possible_paths = [
                r"D:\ffmpeg\bin\ffprobe.exe",
                r"C:\ffmpeg\bin\ffprobe.exe",
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "ffmpeg", "bin", "ffprobe.exe")
            ]
            for p in possible_paths:
                if os.path.exists(p):
                    ffprobe_exe = p
                    break
        
        if not ffprobe_exe:
            ffprobe_exe = "ffprobe" # 回退
            
        # 使用 ffprobe 直接获取信息
        cmd = [
            ffprobe_exe, 
            '-v', 'quiet', 
            '-print_format', 'json', 
            '-show_format', 
            '-show_streams', 
            autio_path
        ]
        
        try:
            # 在 Windows 上，如果路径包含中文，subprocess.run 的首个参数最好是绝对路径
            # 或者使用 shell=True (但要注意风险)
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                # 尝试不指定 encoding 再次尝试
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    raise RuntimeError(f"ffprobe 返回错误 (code {result.returncode}): {result.stderr}")
            
            data = json.loads(result.stdout)
            
            # 找到音频流
            audio_stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'audio'), None)
            format_info = data.get('format', {})
            
            if not audio_stream:
                raise ValueError("No audio stream found in file")
            
            duration = float(format_info.get('duration', 0))
            frame_rate = int(audio_stream.get('sample_rate', 0))
            channels = int(audio_stream.get('channels', 0))
            
            # 比特深度 (bits_per_sample 并不总是存在，尤其是压缩格式)
            bit_depth = int(audio_stream.get('bits_per_sample', 0))
            if bit_depth == 0:
                # 常见回退方案：根据采样格式推断，或者由于 ComfyUI 内部通常转为 16bit 或 32float
                # 这里我们模仿 pydub 的默认行为，或者保持 0
                sample_fmt = audio_stream.get('sample_fmt', '')
                if 's16' in sample_fmt: bit_depth = 16
                elif 's32' in sample_fmt or 'flt' in sample_fmt: bit_depth = 32
                else: bit_depth = 16 # 绝大多数情况解码后是 16bit
            
            # 比特率 (kbps)
            bit_rate_str = format_info.get('bit_rate', '0')
            bit_rate = int(bit_rate_str) / 1000 if bit_rate_str.isdigit() else 0
            
            # 如果 format_info 里没拿到比特率，尝试计算
            if bit_rate == 0 and duration > 0:
                # 粗略估计
                file_size = os.path.getsize(autio_path)
                bit_rate = (file_size * 8) / duration / 1000
                
            return (duration, frame_rate, channels, bit_depth, bit_rate,)
            
        except Exception as e:
            raise RuntimeError(f"获取音频信息失败: {str(e)}")


NODE_CLASS_MAPPINGS = {
    "AutioInfo": AutioInfo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AutioInfo": "获取音频信息"
}
