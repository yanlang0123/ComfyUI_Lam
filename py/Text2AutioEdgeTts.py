import asyncio
import edge_tts
import numpy as np
import folder_paths
import os
class Text2AutioEdgeTts:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'autio')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    @classmethod
    def INPUT_TYPES(cls):
        VOICES=['zh-CN-XiaoxiaoNeural','zh-CN-XiaoyiNeural','zh-CN-YunjianNeural','zh-CN-YunxiNeural','zh-CN-YunxiaNeural',
'zh-CN-YunyangNeural','zh-CN-liaoning-XiaobeiNeural','zh-CN-shaanxi-XiaoniNeural','zh-HK-HiuGaaiNeural',
'zh-HK-HiuMaanNeural','zh-HK-WanLungNeural','zh-TW-HsiaoChenNeural','zh-TW-HsiaoYuNeural','zh-TW-YunJheNeural']
        return {
            "required": {
                "voice": (VOICES, ),
                "filename_prefix": ("STRING", {"default": "comfyUI"}),
                "text": ("STRING", {"multiline": True})
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("音频地址",)
    FUNCTION = "text_2_autio"
    OUTPUT_NODE = False

    CATEGORY = "lam"

    def text_2_autio(self,voice,filename_prefix,text):
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        file = f"{filename}_{counter:05}_.mp3"
        autio_path=os.path.join(full_output_folder, file)
        asyncio.run(edge_tts_text_2_aution(voice,text,autio_path))
        return {"ui": {"text": "音频保存成功文件地址："+os.path.join(full_output_folder, file),
        'autios':[{'filename':file,'type':'output','subfolder':'autio'}]}, "result": (autio_path, )}


async def edge_tts_text_2_aution(VOICE,TEXT,OUTPUT_FILE) -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

NODE_CLASS_MAPPINGS = {
    "Text2AutioEdgeTts": Text2AutioEdgeTts
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Text2AutioEdgeTts": "微软文本转语音"
}
