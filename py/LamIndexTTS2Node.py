import os
import uuid
import time
import torchaudio
from typing import Optional
import folder_paths
import comfy.utils
import random
import requests
import time
import json
import os
from comfy_api.latest import IO,UI

class IndexTTSClient:
    def __init__(self, base_url="http://localhost:5000",output_path="outputs"):
        self.base_url = base_url
        self.output_path = output_path
    
    def initialize_tts(self):
        """调用接口初始化TTS模型"""
        if self.is_model_loaded():
            return True
        json_data = requests.post(f"{self.base_url}/initialize").json()
        if json_data.get("status") == "success":
            return True
        else:
            return False
    
    def unload_model(self):
        """调用接口卸载模型"""
        if not self.is_model_loaded():
            return True
        json_data = requests.post(f"{self.base_url}/unload").json()
        if json_data.get("status") == "success":
            return True
        else:
            return False
        
    def is_model_loaded(self):
        """检查模型是否已加载"""
        json_data = requests.get(f"{self.base_url}/is_loaded").json()
        return json_data.get("is_loaded")
    def get_task_status(self):
        """获取当前任务状态"""
        try:
            response = requests.get(f"{self.base_url}/task/status")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_task_history(self, limit=10):
        """获取任务历史"""
        try:
            response = requests.get(f"{self.base_url}/task/history", params={"limit": limit})
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_task_result(self, task_id):
        """获取任务结果"""
        try:
            response = requests.get(f"{self.base_url}/task/result/{task_id}")
            if response.status_code == 200:
                # 保存音频文件
                filename = os.path.join(self.output_path,f"output_{task_id}.wav") 
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return {"status": "success", "filename": filename}
            else:
                return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def preview_segments(self, text, max_tokens=100):
        """获取文本分句预览"""
        try:
            data = {
                "text": text,
                "max_tokens_per_segment": max_tokens
            }
            response = requests.post(f"{self.base_url}/preview_segments", json=data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def generate_speech(self, text, prompt_audio_path=None, emo_ref_audio_path=None, 
                       emo_control_method=0, emo_weight=1.0, emo_text="", emo_random=False,
                       emotion_vectors=None, **kwargs):
        """生成语音
        
        参数:
        text: 要转换为语音的文本
        prompt_audio_path: 音色参考音频文件路径
        emo_ref_audio_path: 情感参考音频文件路径
        emo_control_method: 情感控制方式 (0-3)
        emo_weight: 情感权重
        emo_text: 情感描述文本
        emo_random: 是否启用情感随机采样
        emotion_vectors: 情感向量列表 [vec1, vec2, ..., vec8]
        **kwargs: 其他高级参数
        """
        # 检查是否有任务正在进行
        status = self.get_task_status()
        if "current_task" in status and status["current_task"] is not None:
            return {"error": "已有任务正在处理中，请稍后再试"}
        
        # 准备表单数据
        data = {
            "text": text,
            "emo_control_method": str(emo_control_method),
            "emo_weight": str(emo_weight),
            "emo_text": emo_text,
            "emo_random": "true" if emo_random else "false",
        }
        
        # 添加情感向量
        if emotion_vectors and len(emotion_vectors) == 8:
            for i, vec in enumerate(emotion_vectors, 1):
                data[f"vec{i}"] = str(vec)
        
        # 添加高级参数
        advanced_params = {
            "do_sample": True,
            "top_p": 0.8,
            "top_k": 30,
            "temperature": 0.8,
            "length_penalty": 0.0,
            "num_beams": 3,
            "repetition_penalty": 10.0,
            "max_mel_tokens": 1500,
            "max_text_tokens_per_segment": 100
        }
        advanced_params.update(kwargs)
        
        for key, value in advanced_params.items():
            if isinstance(value, bool):
                data[key] = "true" if value else "false"
            else:
                data[key] = str(value)
        
        # 准备文件
        files = {}
        if prompt_audio_path and os.path.exists(prompt_audio_path):
            files["prompt_audio"] = open(prompt_audio_path, 'rb')
        
        if emo_ref_audio_path and os.path.exists(emo_ref_audio_path):
            files["emo_ref_audio"] = open(emo_ref_audio_path, 'rb')
        
        try:
            # 发送请求
            response = requests.post(f"{self.base_url}/generate", data=data, files=files)
            result = response.json()
            
            # 关闭文件
            for file in files.values():
                file.close()
                
            return result
        except Exception as e:
            # 确保文件被关闭
            for file in files.values():
                file.close()
            return {"error": str(e)}
    
    def wait_for_task_completion(self, task_id, check_interval=2, timeout=300):
        """等待任务完成
        
        参数:
        task_id: 任务ID
        check_interval: 检查间隔(秒)
        timeout: 超时时间(秒)
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_task_status()
            # 检查任务是否已完成
            if status.get("current_task") is None:
                # 检查任务历史
                history = self.get_task_history(limit=1)
                if "tasks" in history:
                    for task in history["tasks"]:
                        if task.get("id") == task_id:
                            if task.get("status") == "completed":
                                return {"status": "completed", "task": task}
                            elif task.get("status") == "failed":
                                return {"status": "failed", "error": task.get("error", "未知错误")}
            
            # 任务仍在处理中
            print(f"任务 {task_id} 仍在处理中...")
            time.sleep(check_interval)
        
        return {"status": "timeout", "error": "任务处理超时"}
    
class LamIndexTTS2AdvancedParams:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "do_sample": ([True, False], {"default": True,"tooltip": "是否使用采样"}),
                "temperature": ("FLOAT", {"default": 0.8, "min": 0.1, "max":2.0, "step": 0.1,"tooltip": "采样温度"}),
                "top_p": ("FLOAT", {"default": 0.8, "min": 0.0, "max":1.0, "step": 0.01,"tooltip": "采样概率"}),
                "top_k": ("INT", {"default": 30, "min": 0, "max":100, "step": 1,"tooltip": "采样数量"}),
                "num_beams": ("INT", {"default": 3, "min": 1, "max":10, "step": 1,"tooltip": "num_beams"}),
                "repetition_penalty": ("FLOAT", {"default": 10.0, "min": 0.1, "max":20.0, "step": 0.1,"tooltip": "repetition_penalty"}),
                "length_penalty": ("FLOAT", {"default": 0.0, "min": -2.0, "max":2.0, "step": 0.1,"tooltip": "length_penalty"}),
                "max_mel_tokens": ("INT", {"default": 1500, "min": 50, "max":1815, "step": 10,"tooltip": "生成Token最大数量，过小导致音频被截断"}),
                #"initial_value": ("STRING",{"default": 100,"min": 20, "max":600, "step": 10,"tooltip": "分句最大Token数"}),
            }
        }

    RETURN_TYPES = ("ADVANCED_PARAMS", )
    RETURN_NAMES = ("高级参数",)
    FUNCTION = "process"

    OUTPUT_NODE = False
    
    CATEGORY = "lam"

    def process(self,**kwargs):
        return (kwargs,)
    
class LamIndexTTS2UnloadModel:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "server": ("STRING", {"default": "http://localhost:5000", "tooltip": "请勿修改"}),
            }
        }
    RETURN_TYPES = ("BOOL", )
    RETURN_NAMES = ("isOk", )
    FUNCTION = "process"

    OUTPUT_NODE = False

    CATEGORY = "lam"
    def process(self,server:str):
        client = IndexTTSClient(server)
        result = client.unload_model()
        return (result,)

class LamIndexTTS2Node0():
    def __init__(self):
        self.audio_dir = folder_paths.get_output_directory()
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = ""
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "server": ("STRING", {"default": "http://localhost:5000", "tooltip": "请勿修改"}),
                "audio": ("AUDIO,STRING", {"default": "", "forceInput": True, "tooltip": "参考音频地址"}),
                "text": ("STRING",{"default": "","multiline": True,"tooltip": "合成内容"}),
            },
            "optional": {
                "params": ("ADVANCED_PARAMS", ),
                "audio_dir": ("STRING", {"default": "", "forceInput": True, "tooltip": "文件夹"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("audio_path","task_id",)

    FUNCTION = "process"

    OUTPUT_NODE = False

    CATEGORY = "lam"

    def process(self,server:str,audio,text:str,params={},audio_dir=""):
        if isinstance(audio, str):
            audio_path = audio
        else:
            # 生成临时音频文件
            results=UI.AudioSaveHelper.save_audio(
                audio,
                filename_prefix="ComfyUI",
                folder_type=IO.FolderType.temp,
                cls=None,
                format="mp3")
            paths=[]
            for  i in range(len(results)):
                subfolder=results[i]['subfolder']
                if  subfolder:
                    path=os.path.join(self.output_dir, results[i]['subfolder'],results[i]['filename'])
                else:
                    path=os.path.join(self.output_dir, results[i]['filename'])
                paths.append(path)
            audio_path = paths[0]

        if audio_dir !="":
            audio_dir=os.path.join(self.audio_dir,audio_dir)
        else:
            audio_dir=self.audio_dir
        client = IndexTTSClient(server,audio_dir)
        is_ok = client.is_model_loaded()
        if not is_ok:
            client.initialize_tts()

        result = client.generate_speech(text=text,prompt_audio_path=audio_path
                ,emo_control_method=0  # 使用音色参考音频相同的情感
                ,**params)
        if "error" in result:
            raise Exception(result["error"])
        else:
            task_id = result.get("task_id")
            print(f"任务已提交，任务ID: {task_id}")
            
            # 等待任务完成
            wait_result = client.wait_for_task_completion(task_id)
            print(f"任务状态: {wait_result['status']}")
            
            if wait_result["status"] == "completed":
                # 获取任务结果
                result = client.get_task_result(task_id)
                if "filename" in result:
                    print(f"音频已保存到: {result['filename']}")
                    return (result["filename"],task_id,)
                
            print(f"获取结果失败: {wait_result}")
            raise Exception("获取结果失败")
                    

class LamIndexTTS2Node1():
    def __init__(self):
        self.audio_dir = folder_paths.get_output_directory()
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = ""
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "server": ("STRING", {"default": "http://localhost:5000", "tooltip": "请勿修改"}),
                "audio": ("AUDIO,STRING", {"default": "", "forceInput": True, "tooltip": "音色参考音频地址"}),
                "ref_audio": ("AUDIO,STRING", {"default": "", "forceInput": True, "tooltip": "情感参考音频地址"}),
                "text": ("STRING",{"default": "","multiline": True,"tooltip": "合成内容"}),
            },
            "optional": {
                "params": ("ADVANCED_PARAMS", ),
                "audio_dir": ("STRING", {"default": "", "forceInput": True, "tooltip": "文件夹"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("audio_path","task_id",)
    FUNCTION = "process"

    OUTPUT_NODE = False

    CATEGORY = "lam"

    def process(self,server:str,audio,ref_audio,text:str,params={},audio_dir=""):
        if isinstance(audio, str):
            audio_path = audio
        else:
            results=UI.AudioSaveHelper.save_audio(
                audio,
                filename_prefix="ComfyUI",
                folder_type=IO.FolderType.temp,
                cls=None,
                format="mp3")
            paths=[]
            for  i in range(len(results)):
                subfolder=results[i]['subfolder']
                if  subfolder:
                    path=os.path.join(self.output_dir, results[i]['subfolder'],results[i]['filename'])
                else:
                    path=os.path.join(self.output_dir, results[i]['filename'])
                paths.append(path)
            audio_path = paths[0]

        if isinstance(ref_audio, str):
            ref_audio_path = ref_audio
        else:
            results=UI.AudioSaveHelper.save_audio(
                audio,
                filename_prefix="ComfyUI",
                folder_type=IO.FolderType.temp,
                cls=None,
                format="mp3")
            paths=[]
            for  i in range(len(results)):
                subfolder=results[i]['subfolder']
                if  subfolder:
                    path=os.path.join(self.output_dir, results[i]['subfolder'],results[i]['filename'])
                else:
                    path=os.path.join(self.output_dir, results[i]['filename'])
                paths.append(path)
            ref_audio_path = paths[0]

        if audio_dir !="":
            audio_dir=os.path.join(self.audio_dir,audio_dir)
        else:
            audio_dir=self.audio_dir
        client = IndexTTSClient(server,audio_dir)
        is_ok = client.is_model_loaded()
        if not is_ok:
            client.initialize_tts()

        result = client.generate_speech(text=text,prompt_audio_path=audio_path
                ,emo_ref_audio_path=ref_audio_path,emo_control_method=1  # 使用音色参考音频相同的情感
                ,**params
            )
        if "error" in result:
            raise Exception(result["error"])
        else:
            task_id = result.get("task_id")
            print(f"任务已提交，任务ID: {task_id}")
            
            # 等待任务完成
            wait_result = client.wait_for_task_completion(task_id)
            print(f"任务状态: {wait_result['status']}")
            
            if wait_result["status"] == "completed":
                # 获取任务结果
                result = client.get_task_result(task_id)
                if "filename" in result:
                    print(f"音频已保存到: {result['filename']}")
                    return (result["filename"],task_id,)
                
            print(f"获取结果失败: {wait_result}")
            raise Exception("获取结果失败")

class LamIndexTTS2Node2():
    def __init__(self):
        self.audio_dir = folder_paths.get_output_directory()
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = ""
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "server": ("STRING", {"default": "http://localhost:5000", "tooltip": "请勿修改"}),
                "audio": ("AUDIO,STRING", {"default": "", "forceInput": True, "tooltip": "参考音频地址"}),
                "vec1": ("FLOAT", {"default": 0.0, "min": 0.0, "max":1.4, "step": 0.05,"tooltip": "喜"}),
                "vec2": ("FLOAT", {"default": 0.0, "min": 0.0, "max":1.4, "step": 0.05,"tooltip": "怒"}),
                "vec3": ("FLOAT", {"default": 0.0, "min": 0.0, "max":1.4, "step": 0.05,"tooltip": "哀"}),
                "vec4": ("FLOAT", {"default": 0.0, "min": 0.0, "max":1.4, "step": 0.05,"tooltip": "惧"}),
                "vec5": ("FLOAT", {"default": 0.0, "min": 0.0, "max":1.4, "step": 0.05,"tooltip": "厌恶"}),
                "vec6": ("FLOAT", {"default": 0.0, "min": 0.0, "max":1.4, "step": 0.05,"tooltip": "低落"}),
                "vec7": ("FLOAT", {"default": 0.0, "min": 0.0, "max":1.4, "step": 0.05,"tooltip": "惊喜"}),
                "vec8": ("FLOAT", {"default": 0.0, "min": 0.0, "max":1.4, "step": 0.05,"tooltip": "平静"}),
                "text": ("STRING",{"default": "","multiline": True,"tooltip": "合成内容"}),
            },
            "optional": {
                "params": ("ADVANCED_PARAMS", ),
                "audio_dir": ("STRING", {"default": "", "forceInput": True, "tooltip": "文件夹"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("audio_path","task_id",)
    FUNCTION = "process"

    OUTPUT_NODE = False

    CATEGORY = "lam"

    def process(self,server:str,audio,vec1:float,vec2:float,vec3:float,vec4:float,vec5:float,vec6:float,vec7:float,vec8:float,text:str,params={},audio_dir=""):
        task_id = str(uuid.uuid4())
        if isinstance(audio, str):
            audio_path = audio
        else:
            results=UI.AudioSaveHelper.save_audio(
                audio,
                filename_prefix="ComfyUI",
                folder_type=IO.FolderType.temp,
                cls=None,
                format="mp3")
            paths=[]
            for  i in range(len(results)):
                subfolder=results[i]['subfolder']
                if  subfolder:
                    path=os.path.join(self.output_dir, results[i]['subfolder'],results[i]['filename'])
                else:
                    path=os.path.join(self.output_dir, results[i]['filename'])
                paths.append(path)
            audio_path = paths[0]

        if audio_dir !="":
            audio_dir=os.path.join(self.audio_dir,audio_dir)
        else:
            audio_dir=self.audio_dir
        client = IndexTTSClient(server,audio_dir)
        emotion_vectors=[vec1,vec2,vec3,vec4,vec5,vec6,vec7,vec8]
        is_ok = client.is_model_loaded()
        if not is_ok:
            client.initialize_tts()

        result = client.generate_speech(text=text,prompt_audio_path=audio_path
                ,emotion_vectors=emotion_vectors,emo_control_method=2  # 使用音色参考音频相同的情感
                ,**params
            )
        if "error" in result:
            raise Exception(result["error"])
        else:
            task_id = result.get("task_id")
            print(f"任务已提交，任务ID: {task_id}")
            
            # 等待任务完成
            wait_result = client.wait_for_task_completion(task_id)
            print(f"任务状态: {wait_result['status']}")
            
            if wait_result["status"] == "completed":
                # 获取任务结果
                result = client.get_task_result(task_id)
                if "filename" in result:
                    print(f"音频已保存到: {result['filename']}")
                    return (result["filename"],task_id,)
                
            print(f"获取结果失败: {wait_result}")
            raise Exception("获取结果失败")

class LamIndexTTS2Node3():
    def __init__(self):
        self.audio_dir = folder_paths.get_output_directory()
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = ""
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "server": ("STRING", {"default": "http://localhost:5000", "tooltip": "请勿修改"}),
                "audio": ("AUDIO,STRING", {"default": "", "forceInput": True, "tooltip": "参考音频地址"}),
                "text": ("STRING",{"default": "","multiline": True,"tooltip": "合成内容"}),
                "emo_text": ("STRING", {"default": "", "tooltip": "情感描述文本"}),
            },
            "optional": {
                "params": ("ADVANCED_PARAMS", ),
                "audio_dir": ("STRING", {"default": "", "forceInput": True, "tooltip": "文件夹"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("audio_path","task_id",)
    FUNCTION = "process"

    OUTPUT_NODE = False

    CATEGORY = "lam"

    def process(self,server:str,audio,text:str,emo_text:str,params={},audio_dir=""):
        task_id = str(uuid.uuid4())
        if isinstance(audio, str):
            audio_path = audio
        else:
            results=UI.AudioSaveHelper.save_audio(
                audio,
                filename_prefix="ComfyUI",
                folder_type=IO.FolderType.temp,
                cls=None,
                format="mp3")
            paths=[]
            for  i in range(len(results)):
                subfolder=results[i]['subfolder']
                if  subfolder:
                    path=os.path.join(self.output_dir, results[i]['subfolder'],results[i]['filename'])
                else:
                    path=os.path.join(self.output_dir, results[i]['filename'])
                paths.append(path)
            audio_path = paths[0]

        if audio_dir !="":
            audio_dir=os.path.join(self.audio_dir,audio_dir)
        else:
            audio_dir=self.audio_dir
        client = IndexTTSClient(server,audio_dir)
        is_ok = client.is_model_loaded()
        if not is_ok:
            client.initialize_tts()
            
        result = client.generate_speech(text=text,prompt_audio_path=audio_path
                ,emo_text=emo_text,emo_control_method=3  # 使用音色参考音频相同的情感
                ,**params
            )
        if "error" in result:
            raise Exception(result["error"])
        else:
            task_id = result.get("task_id")
            print(f"任务已提交，任务ID: {task_id}")
            
            # 等待任务完成
            wait_result = client.wait_for_task_completion(task_id)
            print(f"任务状态: {wait_result['status']}")
            
            if wait_result["status"] == "completed":
                # 获取任务结果
                result = client.get_task_result(task_id)
                if "filename" in result:
                    print(f"音频已保存到: {result['filename']}")
                    return (result["filename"],task_id,)
                
            print(f"获取结果失败: {wait_result}")
            raise Exception("获取结果失败")



NODE_CLASS_MAPPINGS = {
    "LamIndexTTS2AdvancedParams": LamIndexTTS2AdvancedParams,
    "LamIndexTTS2UnloadModel": LamIndexTTS2UnloadModel,
    "LamIndexTTS2Node0": LamIndexTTS2Node0,
    "LamIndexTTS2Node1": LamIndexTTS2Node1,
    "LamIndexTTS2Node2": LamIndexTTS2Node2,
    "LamIndexTTS2Node3": LamIndexTTS2Node3,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamIndexTTS2AdvancedParams": "IndexTTS2高级参数",
    "LamIndexTTS2UnloadModel": "IndexTTS2-卸载模型",
    "LamIndexTTS2Node0": "IndexTTS2-音色情感同时参考",
    "LamIndexTTS2Node1": "IndexTTS2-音色情感分别参考",
    "LamIndexTTS2Node2": "IndexTTS2-音色参考+情感向量",
    "LamIndexTTS2Node3": "IndexTTS2-音色参考+情感描述",
}