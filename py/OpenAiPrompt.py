import json
from openai import OpenAI
import base64
from PIL import Image
import io
import numpy as np
from lam_tools import tensor2pil,pil2tensor

def encode_image(image_path: str) -> str:
    """将图像编码为 base64 字符串"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

class OpenAiPrompt:
    """
    ChatGLM3接口调用
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "server_url": ("STRING",{"default": "https://dashscope.aliyuncs.com/compatible-mode/v1"}),
                "api_key": ("STRING",{"default": ""}),
                "model_name": ("STRING",{"default": "qwen3-max-preview"}),
                "system_prompt": ("STRING", {"multiline": True,"default":""}),
                "text": ("STRING", {"multiline": True}),
            },
            "optional": {
                "messages":("LIST",),
                "images": ("IMAGE,STRING", )
            }
        }

    RETURN_TYPES = ("STRING","LIST",)
    RETURN_NAMES = ("结果","messages",)

    FUNCTION = "translate"

    #OUTPUT_NODE = False

    CATEGORY = "lam"

    def translate(self, server_url,api_key,model_name,system_prompt,text,messages=None,images=None):
        client = OpenAI(api_key=api_key,base_url=server_url)
        if messages is None:
            messages = []
            if system_prompt and len(system_prompt.strip())>0:
                messages.append({"role": "system", "content": system_prompt})
                
        if images!=None:
            content=[]
            content.append({"type": "text", "text": text})
            if isinstance(images, str):
                # 图像理解示例
                image_base64 = encode_image(images)
                content.append({"type": "image_url", "image_url": {"url":f"data:image/jpeg;base64,{image_base64}"}})
            else:
                img = tensor2pil(images)
                output = io.BytesIO()
                img.save(output, format="JPEG")
                image_base64 = base64.b64encode(output.getvalue()).decode('utf-8')
                content.append({"type": "image_url", "image_url": {"url":f"data:image/jpeg;base64,{image_base64}"}})
            messages.append({"role": "user", "content": content})
        else:
            messages.append({"role": "user", "content": text})

        completion = client.chat.completions.create(model=model_name,messages=messages,top_p=0.8,temperature=0.7)
        messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        return (completion.choices[0].message.content,messages,)

NODE_CLASS_MAPPINGS = {
    "OpenAiPrompt": OpenAiPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAiPrompt": "OpenAi工具"
}
