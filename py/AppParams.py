from server import PromptServer
from .src.wechat.WechatAuthUtils import *
from aiohttp import web
import copy

basePath=folder_paths.folder_names_and_paths['custom_nodes'][0][0]
@PromptServer.instance.routes.post("/lam/setAppParams")
async def setAppParams(request):
    try:
        json_data =  await request.json()
        appName=json_data.get("appName")
        appType=json_data.get("appType")
        appDesc=json_data.get("appDesc")
        workflow=json_data.get("workflow")
        file = os.path.join(basePath,'ComfyUI_Lam','config','workflow',appName+'.json')
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, ensure_ascii=False, indent=4)
            f.close()
        paramList = json_data.get("paramList")
        common={
            'filename': appName+'.json',
            'replyText':appDesc,
            'params':{}
        }
        if appType!='default':
            common['type']=appType

        for param in paramList:
            common['params'][param['id']]=param
        Config().commands[appName]=common
        Config().save_config()
        data={'msg':'修改配置成功','success':True}
        return web.Response(text=json.dumps(data), content_type='application/json')
    except Exception as e:
        logging.error('修改配置异常:'+str(e))
        data={'msg':'修改配置异常','success':False}
        return web.Response(text=json.dumps(data), content_type='application/json')


@PromptServer.instance.routes.get("/lam/getAdminNo")
async def getAdminNo(request):
    data={'data':Config().wechat['adminNo'],'success':True}
    return web.Response(text=json.dumps(data), content_type='application/json')


@PromptServer.instance.routes.get("/lam/getInitData")
async def getInitData(request):
    data={'data':{'base':Config().base,'commands':Config().commands},'success':True}
    return web.Response(text=json.dumps(data), content_type='application/json')

@PromptServer.instance.routes.post("/lam/updateAppData")
async def updateAppData(request):
    try:
        json_data =  await request.json()
        appTitle=json_data.get("appTitle")
        appLogo=json_data.get("appLogo")
        freeSize=json_data.get("freeSize")
        authorIds=json_data.get("authorIds")
        commandNames=json_data.get("commands")
        Config().base['appTitle']=appTitle
        Config().base['appLogo']=appLogo
        Config().base['authorIds']=authorIds
        Config().base['freeSize']=freeSize
        commons=copy.deepcopy(Config().commands)
        #判断commandNames是否为空字典
        if commandNames is None or len(commandNames.keys())<=0:
            Config().commands={}
        else:
            for commandName in commons:
                if commandName not in commandNames:
                    #删除文件
                    filePath = os.path.join(basePath,'ComfyUI_Lam','config','workflow',Config().commands[commandName]['filename'])
                    os.remove(filePath)
                    Config().commands.pop(commandName)
        Config().save_config()
        data={'msg':'修改配置成功','success':True}
        return web.Response(text=json.dumps(data), content_type='application/json')
    except Exception as e:
        logging.error('修改配置异常:'+str(e))
        data={'msg':'修改配置异常','success':False}
        return web.Response(text=json.dumps(data), content_type='application/json')
    

class AppParams:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
               "appName": ("STRING", {"default":""}),
               "appType": (["default","paint-board","picture-book"],),
               "appDesc": ("STRING", {"default":""}),
            }
        }
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "add_app_params"

    CATEGORY = "lam"

    def add_app_params(self,**kwargs):
        return 

NODE_CLASS_MAPPINGS = {
    "AppParams": AppParams
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "AppParams": "应用参数管理"
}
