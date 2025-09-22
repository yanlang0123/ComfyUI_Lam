import json
from openai import OpenAI

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
                "messages":("LIST",)
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("结果",)

    FUNCTION = "translate"

    #OUTPUT_NODE = False

    CATEGORY = "lam"

    def translate(self, server_url,api_key,model_name,system_prompt,text,messages=None):
        client = OpenAI(api_key=api_key,base_url=server_url)
        if messages is None:
            messages = []
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": text})
        completion = client.chat.completions.create(model=model_name,messages=messages,
                                                    top_p=0.8,
                                                    temperature=0.7)
        messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        return (completion.choices[0].message.content,messages,)

NODE_CLASS_MAPPINGS = {
    "OpenAiPrompt": OpenAiPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAiPrompt": "OpenAi工具"
}
