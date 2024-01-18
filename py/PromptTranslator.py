from PIL import Image
import numpy as np
import os
import time
import requests
import json

#获取组节点
confdir = os.path.abspath(os.path.join(__file__, "../../config"))
if not os.path.exists(confdir):
    os.mkdir(confdir)

class PromptTranslator:
    def __init__(self):
        self.data={"apiKey": "", "secretKey": "", "access_token": ""}
        self.baiduPath=os.path.join(confdir,'baidu.json')
        if os.path.exists(self.baiduPath):
            with open(self.baiduPath,'r') as f:
                self.data = json.load(f)


    @classmethod
    def INPUT_TYPES(cls):
        baidu=os.path.join(confdir,'baidu.json')
        data={"apiKey": "", "secretKey": "", "access_token": "","changTime":""}
        if not os.path.exists(baidu):
            with open(baidu, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            with open(baidu,'r') as f:
                data = json.load(f)

        return {
            "required": {
                "apiKey": ("STRING",{"default": data.get('apiKey','')}),
                "secretKey": ("STRING",{"default": data.get('secretKey','')}),
                "fromLang": (['auto','en','zh'], ),
                "toLang": (['en','zh'], ),
                "text": ("STRING", {"multiline": True,"default":""}),
            },
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("翻译结果",)
    FUNCTION = "translator"
    OUTPUT_NODE = True

    CATEGORY = "lam"

    def translator(self,apiKey,secretKey,fromLang,toLang,text):
        if self.data and self.data['access_token'] and (time.time()-float(self.data['changTime']))/ (24 * 3600) <= 29:
            accessToken=self.data['access_token']
        else:
            accessToken=self.getAccessToken(apiKey,secretKey)
            if accessToken:
                self.data['apiKey']=apiKey
                self.data['secretKey']=secretKey
                self.data['access_token']=accessToken
                self.data['changTime']=time.time()
                with open(self.baiduPath,'w',encoding='utf-8') as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=4)

        url = 'https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=' + accessToken
        headers = {'Content-Type': 'application/json'}
        payload = {'q': text, 'from': fromLang, 'to': toLang, 'termIds' : ''}
        # Send request
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
        if 'error_code' in result:
            return { "ui": { "text":"翻译失败:"+result['error_msg']},"result": (text) }
        else:
            return { "ui": { "text":"翻译结果："+result['result']['trans_result'][0]['dst']},"result": (result['result']['trans_result'][0]['dst'],)}

    def getAccessToken(self,apiKey,secretKey):
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={apiKey}&client_secret={secretKey}"
        payload = ""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()
        if 'error' in data:
            return None
        else:
            return data['access_token']

NODE_CLASS_MAPPINGS = {
    "PromptTranslator": PromptTranslator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptTranslator": "百度翻译"
}
