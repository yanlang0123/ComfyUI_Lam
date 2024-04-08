import server
from aiohttp import web
import os
import json


dir = os.path.abspath(os.path.join(__file__, "../../styles"))
if not os.path.exists(dir):
    os.mkdir(dir)

@server.PromptServer.instance.routes.get("/lam/getStyles")
def getStyles(request):
    if "name" in request.rel_url.query:
        name = request.rel_url.query["name"]
        file = os.path.join(dir, name+'.json')
        zhFile = os.path.join(dir, 'zh_CN.json')
        if os.path.isfile(zhFile):
            f = open(zhFile,'r', encoding='utf-8')
            zhData = json.load(f)
            f.close()

        if os.path.isfile(file):
            f = open(file,'r', encoding='utf-8')
            data = json.load(f)
            f.close()
            if data:
                ndata=[]
                if zhData:
                    for d in data:
                        nd={}
                        name=d['name'].replace('-',' ')
                        words=name.split(' ')
                        key=' '.join(word.upper() if word.lower() in ['mre','sai','3d'] else word.capitalize() for word in words)
                        img_name='_'.join(words).lower()
                        nd['zhName']=zhData[key] if key in zhData else key
                        nd["name"]=d['name']
                        nd['imgName']=img_name
                        ndata.append(nd)
                return web.json_response(ndata)
    return web.Response(status=404)

class StyleSelecto:
    """
    提示词选择工具
    """
    def __init__(self):
        dir = os.path.abspath(os.path.join(__file__, "../../styles"))
        if not os.path.exists(dir):
            os.mkdir(dir)
        self.styleAll={}
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".json") and file.split(".")[0].find("styles")!=-1:
                    f = open(os.path.join(root, file), 'r', encoding='utf-8')
                    data = json.load(f)
                    f.close()
                    for d in data:
                        self.styleAll[d['name']] = d
    
    @classmethod
    def INPUT_TYPES(self):
        dir = os.path.abspath(os.path.join(__file__, "../../styles"))
        #获取目录全部yml文件名
        files_name=[]
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".json") and file.split(".")[0].find("styles")!=-1:
                    files_name.append(file.split(".")[0])

        return {
            "required": {
                "prompt": ("STRING", {"forceInput": True}),
                "style_type":(files_name, ),

            },
            "optional": {
                "negative_prompt":("STRING",{"forceInput": True}),
                "i": ("INT",{"forceInput": True}),
            },
            "hidden": {"unique_id": "UNIQUE_ID","wprompt":"PROMPT"},
        }

    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ("正向提示词","反向提示词","i项风格名称",)

    FUNCTION = "get_style"

    #OUTPUT_NODE = False

    CATEGORY = "lam"

    def get_style(self,prompt,style_type,unique_id,wprompt,negative_prompt="",i=None):
        values = []
        if unique_id in wprompt:
            if wprompt[unique_id]["inputs"]['styles']:
                #分割字符串
                values = wprompt[unique_id]["inputs"]['styles'].split(',')
        styleName=''
        if i!=None:
            if len(values)>0:
                styleName=values[i]
                if 'prompt' in self.styleAll[values[i]]:
                    prompt=self.styleAll[values[i]]['prompt'].format(prompt=prompt)
                if 'negative_prompt' in self.styleAll[values[i]]:
                    negative_prompt+=','+self.styleAll[values[i]]['negative_prompt']
            else:
                keysl=list(self.styleAll.keys())
                styleName=keysl[i]
                if 'prompt' in self.styleAll[keysl[i]]:
                    prompt=self.styleAll[keysl[i]]['prompt'].format(prompt=prompt)
                if 'negative_prompt' in self.styleAll[keysl[i]]:
                    negative_prompt+=','+self.styleAll[keysl[i]]['negative_prompt']
        else:
            for val in values:
                if 'prompt' in self.styleAll[val]:
                    prompt=self.styleAll[val]['prompt'].format(prompt=prompt)
                if 'negative_prompt' in self.styleAll[val]:
                    negative_prompt+=','+self.styleAll[val]['negative_prompt']

        return (prompt,negative_prompt,styleName)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "StyleSelecto": StyleSelecto
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "StyleSelecto": "风格选择器"
}
