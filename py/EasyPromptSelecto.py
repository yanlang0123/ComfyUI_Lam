from server import PromptServer
from aiohttp import web
import json
import os
import yaml

#获取组节点
gdir = os.path.abspath(os.path.join(__file__, "../../groupNode"))
if not os.path.exists(gdir):
    os.mkdir(gdir)

@PromptServer.instance.routes.get("/lam/groupNode")
async def get_groupNode(request):
    file=os.path.join(gdir, "groupNodes.json")
    if os.path.isfile(file):
        f = open(file,'r', encoding='utf-8')
        data = json.load(f)
        return web.json_response(data)
    return web.Response(status=404)



@PromptServer.instance.routes.post("/lam/groupNode")
async def save_groupNode(request):
    json_data = await request.json()
    file=os.path.join(gdir, "groupNodes.json")
    if os.path.isfile(file):
        f = open(file,'r', encoding='utf-8')
        data = json.load(f)
    for key in list(json_data.keys()):
        data[key] = json_data[key]
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return web.Response(status=201)

@PromptServer.instance.routes.post("/lam/delGroupNode")
async def del_groupNode(request):
    json_data = await request.json()
    file=os.path.join(gdir, "groupNodes.json")
    if os.path.isfile(file):
        f = open(file,'r', encoding='utf-8')
        data = json.load(f)
    if 'name' in list(json_data.keys()):
        if json_data['name'] in data:
            del data[json_data['name']]
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return web.Response(status=201)

#获取提示词
dir = os.path.abspath(os.path.join(__file__, "../../tags"))
if not os.path.exists(dir):
    os.mkdir(dir)

@PromptServer.instance.routes.get("/lam/getPrompt")
def getPrompt(request):
    if "name" in request.rel_url.query:
        name = request.rel_url.query["name"]
        file = os.path.join(dir, name+'.yml')
        if os.path.isfile(file):
            f = open(file,'r', encoding='utf-8')
            data = yaml.load(f, Loader=yaml.FullLoader)
            f.close()
            #转json
            if data:
                return web.json_response(data)
    return web.Response(status=404)

class EasyPromptSelecto:
    """
    提示词选择工具
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        dir = os.path.abspath(os.path.join(__file__, "../../tags"))
        if not os.path.exists(dir):
            os.mkdir(dir)
        #获取目录全部yml文件名
        files_name=[]
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".yml"):
                    files_name.append(file.split(".")[0])

        return {
            "required": {
                "text": ("STRING",{"default": ""}),
                "prompt_type":(files_name, ),
            },
            "hidden": {"unique_id": "UNIQUE_ID","wprompt":"PROMPT"},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("提示词",)

    FUNCTION = "translate"

    #OUTPUT_NODE = False

    CATEGORY = "lam"

    def translate(self,prompt_type,unique_id,wprompt,text=''):
        values = ''
        if unique_id in wprompt:
            if wprompt[unique_id]["inputs"]['tags']:
                #分割字符串
                values = wprompt[unique_id]["inputs"]['tags']
        return (text+values,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "EasyPromptSelecto": EasyPromptSelecto
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyPromptSelecto": "提示词选择工具"
}
