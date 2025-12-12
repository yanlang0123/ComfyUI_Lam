import os
import sys
import subprocess
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class ZhPromptTranslator:

    def __init__(self):
        self.zh_langs = {
            "eng_Latn": "英语",
            "zho_Hans": "中文（简体）",
            "zho_Hant": "中文（繁体）",
            "spa_Latn": "西班牙语",
            "fra_Latn": "法语",
            "deu_Latn": "德语",
            "jpn_Jpan": "日语",
            "kor_Hang": "韩语",
            "rus_Cyrl": "俄语",
            "arb_Arab": "阿拉伯语",
            "por_Latn": "葡萄牙语"
        }
        self.model = None
        self.tokenizer = None
        
    def translate(self,chinese_str: str,to_lang:str="eng_Latn") -> str:
        # 使用分词器对文本进行编码，将文本转换为模型输入所需的张量格式
        inputs = self.tokenizer(chinese_str, return_tensors="pt") 
        # 生成翻译的令牌序列，强制生成中文（简体）作为目标语言（修改获取语言ID的方式）
        translated_tokens = self.model.generate(
            **inputs, forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(to_lang), max_length=30
        )

        # 将生成的令牌序列解码为可读的文本
        translated_text = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return translated_text
    
    @classmethod
    def INPUT_TYPES(s):
        zh_langs = {
            "eng_Latn": "英语",
            "zho_Hans": "中文（简体）",
            "zho_Hant": "中文（繁体）",
            "spa_Latn": "西班牙语",
            "fra_Latn": "法语",
            "deu_Latn": "德语",
            "jpn_Jpan": "日语",
            "kor_Hang": "韩语",
            "rus_Cyrl": "俄语",
            "arb_Arab": "阿拉伯语",
            "por_Latn": "葡萄牙语"
        }
        zh_langsNames = [zh_langs[key] for key in zh_langs]
        return {
            "required": {
                "text_trans": ("STRING", {"multiline": True, "default": ""}),
                "model_type": (["600M","1.3B"],),
                "to_lang": (zh_langsNames,),
            },
            "optional": {
                "textList": ("LIST",),
            },
        }

    RETURN_TYPES = ("STRING","LIST",)
    FUNCTION = "translation"
    CATEGORY = "lam"

    def translation(self, text_trans,model_type,to_lang,textList=[]):
        if self.model is None:
            modelDir = os.path.join(os.path.abspath(os.path.join(__file__, "../../models")),'nllb-200-distilled-'+model_type)
            if not os.path.exists(modelDir):
                # 执行download.py 下载模型
                download_script = os.path.abspath(os.path.join(__file__, "../../download.py"))
                model_name = f"nllb-200-distilled-{model_type}"
                downloadCmd = [sys.executable, download_script, model_name]
                # 打印下载日志，等待下载完成
                proc = subprocess.Popen(downloadCmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
                for line in iter(proc.stdout.readline, ''):
                    print(line, end='')
                proc.wait()
                if proc.returncode != 0:
                    raise Exception(f"模型下载失败，返回码: {proc.returncode}")
                print("下载完成")

            self.model = AutoModelForSeq2SeqLM.from_pretrained(modelDir)
            self.tokenizer = AutoTokenizer.from_pretrained(modelDir, src_lang="ron_Latn")
            
        to_lang_key = ''
        for key, value in self.zh_langs.items():
            if value == to_lang:
                to_lang_key = key
                break

        target_text = self.translate(text_trans,to_lang_key)
        targetList=[]
        for text in textList:
            targetList.append(self.translate(text,to_lang_key))
        
        return (target_text,targetList)
    
   
NODE_CLASS_MAPPINGS = {
    "ZhPromptTranslator": ZhPromptTranslator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZhPromptTranslator": "中文或其他翻译"
}



