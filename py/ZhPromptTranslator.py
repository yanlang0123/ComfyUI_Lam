import json
import re
import os
import csv
import string
from collections import OrderedDict
from transformers import MarianMTModel,MarianTokenizer

#获取组节点
confdir = os.path.abspath(os.path.join(__file__, "../../config"))
if not os.path.exists(confdir):
    os.mkdir(confdir)

def sort_dict_by_key_length(d):
    sorted_keys = sorted(d.keys(), key=lambda x: len(x),reverse=True)
    sorted_dict = OrderedDict()
    for key in sorted_keys:
        sorted_dict[key] = d[key]
    return sorted_dict

# 读取 csv 文件到内存中缓存起来
def load_csv(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        cache = OrderedDict(reader)
        cache = sort_dict_by_key_length(cache)

    return cache

def contains_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    return bool(pattern.search(text))

def remove_unnecessary_spaces(text):
    """Removes unnecessary spaces between characters."""
    pattern = r"\)\s*\+\+|\)\+\+\s*"
    replacement = r")++"
    return re.sub(pattern, replacement, text)



def replace_text(text, cache):
    for key, value in cache.items():
        if key in text:
            text = text.replace(key, value + ' ')
    return text




class ZhPromptTranslator:

    def __init__(self):
        self.my_translations = os.path.join(confdir,"translations.csv")
        self.model = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-zh-en').cuda()
        self.tokenizer = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-zh-en')
        self.tokenizer.src_lang = "zh_CN"
    def translate(self,chinese_str: str) -> str:
        # 对中文句子进行分词
        input_ids = self.tokenizer.encode(chinese_str, return_tensors="pt").cuda()

        # 进行翻译
        output_ids = self.model.generate(input_ids)

        # 将翻译结果转换为字符串格式
        english_str = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        #如果最后有一个.，则去掉
        if english_str[-1] == '.':
            english_str = english_str[:-1]
        return english_str
    
    def process_text(self,text):
        # 将中文全角标点符号替换为半角标点符号
        text = text.translate(str.maketrans('，。！？；：‘’“”（）【】', ',.!?;:\'\'\"\"()[]'))
        # 按逗号分割成数组
        text_array = text.split(',')
        # 对数组中每个字符串进行处理
        for i in range(len(text_array)):
            # 如果字符串以 < 开头 > 结尾，则是Lora，跳过不处理
            if text_array[i].startswith('<') and text_array[i].endswith('>'):
                continue
            # 判断是否只包含英文字符
            if all(char in string.printable + ' ' for char in text_array[i]):
                continue
            else:
                # 调用 transfer 函数进行翻译
                text_array[i] = self.translate(text_array[i])
        # 重新用逗号连接成字符串并返回
        return ','.join(text_array)
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_trans": ("STRING", {"multiline": True, "default": ""}),
                # "trans_switch": (["enabled", "disabled"],),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "translation"
    CATEGORY = "lam"

    def translation(self, text_trans, ):

        if text_trans == "undefined":
            text_trans = ""

        target_text = ""

        print("prompt: ", text_trans)

        cache = load_csv(self.my_translations)

        if contains_chinese(text_trans):
            text_trans = remove_unnecessary_spaces(text_trans)
            modified_text = replace_text(text_trans, cache)
            print("modified_text: " + modified_text)

            target_text = self.process_text(modified_text)
            target_text = re.sub('♪','', target_text)
        else:
            target_text = text_trans

        print("target: " + target_text)

        return (target_text,)
    
NODE_CLASS_MAPPINGS = {
    "ZhPromptTranslator": ZhPromptTranslator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZhPromptTranslator": "中文翻译"
}



