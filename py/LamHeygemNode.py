import os
import uuid
import requests
import time
import shutil
import torchaudio
from typing import Optional
import folder_paths
import comfy.utils
import hashlib
import io
import random

class LamHeyGemNode:
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "server": ("STRING", {"default": "http://localhost:8383", "tooltip": "请勿修改"}),
                "video_path": ("STRING", {"default": "", "forceInput": True}),
            },
            "optional": {
                "audio": ("AUDIO", {"default": None}),
                "audio_path": ("STRING", {"default": "", "tooltip": "与audio参数二选一"}),
                "chaofen": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("video_path","video_url", "task_id")
    FUNCTION = "process"
    CATEGORY = "lam"

    def process(self,server:str, video_path: str, chaofen: bool = False, audio: Optional[dict] = None, audio_path: str = ""):
        # 生成唯一任务ID
        task_id = str(uuid.uuid4())
        # 优先使用音频路径
        if audio_path and os.path.exists(audio_path):
            audio_output_path = audio_path
        else:
            # 生成临时音频文件
            waveform = audio["waveform"]
            sample_rate = audio["sample_rate"]
            audio_output_path = os.path.join(self.output_dir, f"{task_id}_temp_audio.wav")
            torchaudio.save(audio_output_path, waveform[0], sample_rate)

        # 准备请求数据
        data = {
            "audio_url": audio_output_path,
            "video_url": video_path,
            "code": task_id,
            "watermark_switch": 0,
            "chaofen": 1 if chaofen else 0,
            "pn": 1
        }
        
        # 提交任务
        try:
            response = requests.post(server+"/easy/submit", json=data)
            if response.status_code != 200:
                raise Exception(f"Failed to submit task: {response.text}")
            
            # 创建进度条
            pbar = comfy.utils.ProgressBar(100)
            
            query_response = requests.get(f"{server}/easy/query?code={task_id}")
            if query_response.status_code != 200:
                raise Exception(f"Failed to query task status: {query_response.text}")
            
            status_data = query_response.json()
            status = status_data["data"]["status"]
            # 轮询任务状态
            while status == 1:
                query_response = requests.get(f"{server}/easy/query?code={task_id}")
                if query_response.status_code != 200:
                    raise Exception(f"Failed to query task status: {query_response.text}")
                
                status_data = query_response.json()
                progress = float(status_data["data"].get("progress", 0.0))
                pbar.update_absolute(int(progress))
                status = status_data["data"]["status"]          
                time.sleep(1)
            
            if status_data["data"]["status"] == 2:
                output_video_path = status_data["data"]["result"]
                url = status_data["data"]["url"]
                output_url=f'{server}{url}'

                return (output_video_path,output_url, task_id)
            elif status_data["data"]["status"] == 0:
                raise Exception(f"Task failed: {status_data['data']['msg']}")

        except Exception as e:
            raise Exception(f"HeyGem processing failed: {str(e)}")
        finally:
            if os.path.exists(audio_output_path):
                # os.remove(audio_output_path)
                pass

class LamHeyGemQueryNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "server": ("STRING", {"default": "http://localhost:8383", "tooltip": "请勿修改"}),
                "task_id": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "FLOAT")
    RETURN_NAMES = ("status", "result", "progress")
    FUNCTION = "query"
    CATEGORY = "lam"

    def query(self,server:str,task_id: str):
        if not task_id:
            return ("error", "No task ID provided", 0.0)
            
        try:
            query_response = requests.get(f"{server}/easy/query?code={task_id}")
            if query_response.status_code != 200:
                raise Exception(f"Failed to query task status: {query_response.text}")
            
            status_data = query_response.json()
            return (
                status_data["data"]["msg"],
                status_data["data"].get("result", ""),
                float(status_data["data"].get("progress", 0.0))
            )
            
        except Exception as e:
            return ("error", str(e), 0.0)

NODE_CLASS_MAPPINGS = {
    "LamHeyGemNode": LamHeyGemNode,
    "LamHeyGemQueryNode": LamHeyGemQueryNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamHeyGemNode": "HeyGem对口型",
    "LamHeyGemQueryNode": "HeyGem任务状态",
}