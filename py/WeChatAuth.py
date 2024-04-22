from server import PromptServer
from aiohttp import web
import os
import json
from .src.wechat.WechatAuthUtils import *
from .src.wechat.DataBaseUtil import DataBaseUtil
import xml.etree.ElementTree as ET
import time
import logging
import queue
import random
import types
import execution
import uuid
import folder_paths
def send_sync(self, event, data, sid=None): #继承父类的send_sync方法
    if sid and hasattr(self, "user_command") and sid in getattr(self,'user_command'):
        if event == "executing" and data['node'] is None and data['prompt_id'] == self.user_command[sid]['prompt_id']:
            history=self.prompt_queue.get_history(prompt_id=data['prompt_id'])[data['prompt_id']]
            #print("历史记录======：",history)
            if Config().wechat['isEnterprise'] and ('isWeb' not in self.user_command[sid] or self.user_command[sid]['isWeb']==False):
                imagePaths=[]
                videoPaths=[]
                for node_id in history['outputs']:
                    node_output = history['outputs'][node_id]
                    if 'images' in node_output:
                        for image in node_output['images']:
                            basePath=''
                            if 'output' == image['type']:
                                basePath=folder_paths.get_output_directory()
                            elif 'temp' == image['type']:
                                basePath=folder_paths.get_temp_directory()
                            elif 'input' == image['type']:
                                basePath=folder_paths.get_input_directory()
                            
                            if image['subfolder']:
                                basePath=os.path.join(basePath,image['subfolder'])

                            imagePaths.append(os.path.join(basePath,image['filename']))
                    if 'gifs' in node_output:
                        for image in node_output['gifs']:
                            basePath=''
                            if 'output' in image['type']:
                                basePath=folder_paths.get_output_directory()
                            elif 'temp' in image['type']:
                                basePath=folder_paths.get_temp_directory()
                            elif 'input' in image['type']:
                                basePath=folder_paths.get_input_directory()
                            
                            if image['subfolder']:
                                basePath=os.path.join(basePath,image['subfolder'])
                            
                            if 'format' in image:
                                if image['format'].startswith('video'):
                                    videoPaths.append(os.path.join(basePath,image['filename']))
                                    continue

                            imagePaths.append(os.path.join(basePath,image['filename']))

                logging.info("imagePaths: " + str(imagePaths)+" videoPaths: " + str(videoPaths))
                for imagePath in imagePaths:
                    mediaId=getMediaId(imagePath,'image')
                    sendServiceImageMessge(mediaId,sid)
                for videoPath in videoPaths:
                    mediaId=getMediaId(videoPath,'video')
                    sendServiceVideoMessge(mediaId,'AI生成','AI生成视频',sid)
            self.user_command[sid]['status']='wcomplete'
            now = time.localtime()
            end_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
            db=DataBaseUtil()
            db.update_data('wcomplete', end_time, json.dumps(history['outputs']),data['prompt_id'])
            db.close_con()

    self.loop.call_soon_threadsafe(
        self.messages.put_nowait, (event, data, sid))
def update_dict(dictionary, keys, value):
    if len(keys) == 1:
        dictionary[keys[0]] = value
    else:
        key = keys.pop(0)
        if isinstance(dictionary[key], dict):
            update_dict(dictionary[key], keys, value)
        elif isinstance(dictionary[key], list):
            for item in dictionary[key]:
                update_dict(item, keys[:], value)
        else:
            raise ValueError("Invalid data structure")
def setPost(self,FromUserName):
    self.user_command[FromUserName]['status']='waiting' #prepare:准备 waiting:待执行  wcomplete完成
    params=self.user_command[FromUserName]
    logging.info(str(params))
    basePath=folder_paths.folder_names_and_paths['custom_nodes'][0][0]
    comand=Config().wechat['commands'][params['command']]
    filePath = os.path.join(basePath,'ComfyUI_Lam','config','workflow',comand['filename'])
    if os.path.exists(filePath)==False:
        logging.warning("文件不存在："+filePath)
        return None
    f = open(filePath,'r', encoding='utf-8')
    json_data = json.load(f)
    f.close()
    for key in comand['params']:
        keys=comand['params'][key]['keys'][:]
        if key in params:
            update_dict(json_data,keys,params[key])
    
    json_data={"prompt":json_data,"client_id":params['openId']}
    logging.info(json_data)
    json_data = self.trigger_on_prompt(json_data)
    if "number" in json_data:
        number = float(json_data['number'])
    else:
        number = self.number
        if "front" in json_data:
            if json_data['front']:
                number = -number

        self.number += 1

    if "prompt" in json_data:
        prompt = json_data["prompt"]
        valid = execution.validate_prompt(prompt)
        extra_data = {}
        if "extra_data" in json_data:
            extra_data = json_data["extra_data"]

        if "client_id" in json_data:
            extra_data["client_id"] = json_data["client_id"]
        if valid[0]:
            prompt_id = str(uuid.uuid4())
            outputs_to_execute = valid[2]
            self.prompt_queue.put((number, prompt_id, prompt, extra_data, outputs_to_execute))
            now = time.localtime()
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
            self.user_command[FromUserName]['prompt_id']=prompt_id 
            db=DataBaseUtil()
            db.insert_data( params['openId'], json.dumps(params), prompt_id,'waiting',start_time, '', '')
            db.close_con()
            return prompt_id
        else:
            self.user_command[FromUserName]['status']='prepare' # prepare:准备 waiting:待执行  wcomplete完成
            logging.warning("invalid prompt: {}".format(valid[1]))
            return None
        
def getTaskRanking(self,FromUserName):
    if 'prompt_id' not in self.user_command[FromUserName]:
        return '您还没有排队，请先发送您的指令'
    prompt_id=self.user_command[FromUserName]['prompt_id']
    current_queue = self.prompt_queue.get_current_queue()
    print(current_queue)
    for i in range(len(current_queue[0])):
        if current_queue[0][i][1] == prompt_id:
            return '您的任务正在执行。'
    for i in range(len(current_queue[1])):
        if current_queue[1][i][1] == prompt_id:
            return '当前排队人数：'+str(len(current_queue[1]))+'人,您当前的位置在'+current_queue[1][i][0]+'号。'
    return '您还没有排队，请先发送您的指令'

@PromptServer.instance.routes.get("/wechatauth/getHistorys")
async def getHistorys(request):
    if "openId" in request.rel_url.query:
        openId=request.rel_url.query['openId']
        db=DataBaseUtil()
        datas=db.get_many_data(openId)
        db.close_con()
        return web.Response(text=json.dumps(datas), content_type='application/json')
    else:
        return web.Response(status=404)
    
@PromptServer.instance.routes.post("/wechatauth/addTask")
async def addTask(request):
    post = await request.post()
    print(post.keys())
    command = post.get("command")
    if command == None:
        msg = '指令不能为空！'
        data={'msg':msg,'success':False}
        return web.Response(text=json.dumps(data), content_type='application/json')

    openId = post.get("openId")
    if openId == None:
        msg = '用户编码不能为空！'
        data={'msg':msg,'success':False}
        return web.Response(text=json.dumps(data), content_type='application/json')
    
    if hasattr(PromptServer.instance,'user_command') and openId in PromptServer.instance.user_command and PromptServer.instance.user_command[openId]['status']=='waiting':
        msg = '您已经在队列中，请勿重复提交！'
        data={'msg':msg,'success':False}
        return web.Response(text=json.dumps(data), content_type='application/json')

    adminNo=base64_decode(Config().wechat['adminNo'])
    if adminNo!=openId:
        db=DataBaseUtil()
        data=db.get_user_frequency(openId)
        if data[0]==None:
            db.user_recharge(openId,Config().wechat['freeSize'])
            data=db.get_user_frequency(openId)
        countd=db.get_user_task_count(openId)
        db.close_con()
        if countd[0] >=data[0]:
            msg='非常抱歉，您的免费使用次数已用完，如需继续使用，请扫描右上角二维码，联系管理员。'
            data={'msg':msg,'success':False}
            return web.Response(text=json.dumps(data), content_type='application/json')
    
    params=Config().wechat['commands'][command]['params']
    paramName=''
    userData={'openId':openId,'command':command,'status':'prepare','isWeb':True}
    for param in params:
        val=post.get(param)
        if params[param]['isRequired'] and val==None:
            paramName= params[param]['zhName']
            break
        if val:
            userData[param]=val

    if paramName:
        msg = '参数"'+paramName+'"不能为空！'
        data={'msg':msg,'success':False}
        return web.Response(text=json.dumps(data), content_type='application/json')
    
    if 'seed' in userData:
        if userData['seed'].isdigit()==False or int(userData['seed'])==-1:
            userData['seed']=''.join(random.sample('123456789012345678901234567890',14))

    if hasattr(PromptServer.instance,"user_command")==False:
        setattr(PromptServer.instance,"user_command",{})

    PromptServer.instance.user_command[openId]=userData
    resp=setPost(PromptServer.instance,openId)
    if resp!=None:
        data={'msg':'任务成功加入队列请等待','prompt_id':resp,'success':True}
        return web.Response(text=json.dumps(data), content_type='application/json')
    
@PromptServer.instance.routes.get("/wechatauth/getCommands")
async def getCommands(request):
    commands=Config().wechat['commands']
    return web.Response(text=json.dumps(commands), content_type='application/json')

@PromptServer.instance.routes.get("/wechatauth/app")
async def app(request):
    if "openId" in request.rel_url.query:
        openId=request.rel_url.query['openId']
        openId=base64_decode(openId)
        basePath = folder_paths.folder_names_and_paths['custom_nodes'][0][0]
        htmlPtah = os.path.join(basePath, 'ComfyUI_Lam', 'pages','app.html')
        # 打开文件
        with open(htmlPtah, 'r', encoding='utf-8') as file:
            # 读取文件内容
            html_content = file.read()

        html_content = html_content.replace('{{openId}}', openId)
        return web.Response(text=html_content, content_type='text/html')
        #return web.FileResponse(htmlPtah)
    else:
        return web.Response(status=404)
    
@PromptServer.instance.routes.get("/wechatauth/handleMessage")
async def handleMessageGet(request):
    if "echostr" in request.rel_url.query:
        echostr=request.rel_url.query['echostr']
        return web.Response(text=echostr)
    else:
        return web.Response(text="121212")

@PromptServer.instance.routes.post("/wechatauth/handleMessage")
async def handleMessagePost(request):
    # 读取请求体数据
    body = await request.read()
    # 将字节转换为字符串
    data_str = body.decode('utf-8')
    data = ET.fromstring(data_str)
    ToUserName = data.find('ToUserName').text
    FromUserName = data.find('FromUserName').text
    MsgType = data.find('MsgType').text
    logging.info(data_str)
    CreateTime = int(time.time())
    if hasattr(PromptServer.instance,"user_command")==False:
        setattr(PromptServer.instance,"user_command",{})
        
    #判断是否为准备状态
    isPrepare=FromUserName in PromptServer.instance.user_command and PromptServer.instance.user_command[FromUserName]['status']=='prepare'
    isWaiting=FromUserName in PromptServer.instance.user_command and PromptServer.instance.user_command[FromUserName]['status']=='waiting'
    # 如果发送的是消息请求，
    if MsgType == 'text': #语音屏蔽or MsgType == 'voice'
        try:
            MsgId = data.find("MsgId").text
            if MsgType == 'text':
                Content = data.find('Content').text  # 文本消息内容
            elif MsgType == 'voice':
                Content = data.find('Recognition').text  # 语音识别结果，UTF8编码
            # 调用回复函数判断接受的信息，然后返回对应的内容
            reply_content,otherName=receive_msg(Content,isPrepare,isWaiting)
            logging.info("reply_content:"+reply_content+',otherName:'+str(otherName))
            if reply_content=='menu' and otherName:
                if Config().wechat['isEnterprise']:
                    sendServiceMenuMessage('您可以执行以下操作：','欢迎再次光临',otherName, FromUserName)
                else:
                    msgStr='您可以执行以下操作指令：\n '
                    for i in range(len(otherName)):
                        msgStr+=otherName[i]['content']+'\n'
                    out = reply_text(FromUserName, ToUserName, CreateTime, msg)
                    return web.Response(text=out, content_type='application/xml')

            elif reply_content=='command' and otherName:
                adminNo=base64_decode(Config().wechat['adminNo'])
                msg=''
                isAdopt=True
                if adminNo!=FromUserName:
                    db=DataBaseUtil()
                    data=db.get_user_frequency(FromUserName)
                    if data[0]==None:
                        db.user_recharge(FromUserName,Config().wechat['freeSize'])
                        data=db.get_user_frequency(FromUserName)
                    countd=db.get_user_task_count(FromUserName)
                    db.close_con()
                    if countd[0] >=data[0]:
                        isAdopt=False
                        msg='非常抱歉，您的免费使用次数已用完,如需继续使用，请联系管理员。微信号：\n'+Config().wechat['adminWeChat']
                    
                if isAdopt:
                    #添加指令的代码
                    PromptServer.instance.user_command[FromUserName]={'openId':FromUserName,'status':'prepare','command':otherName,'seed':''.join(random.sample('123456789012345678901234567890',14))}
                    msg,comlist=getCommandMsg(Config().wechat['commands'][otherName],Config().wechat['isEnterprise'])
                    if comlist:
                        sendServiceMenuMessage(msg,Config().wechat['commands'][otherName]['replyText'],comlist, FromUserName)
                        return web.Response(status=200)
                out = reply_text(FromUserName, ToUserName, CreateTime, msg)
                return web.Response(text=out, content_type='application/xml')
            elif reply_content=='query' and otherName:
                if otherName=='查询排队情况':
                    msg=''
                    if isWaiting:
                        msg=getTaskRanking(PromptServer.instance,FromUserName)
                    else:
                        msg='您还没有排队，请先发送您的指令'    

                    out = reply_text(FromUserName, ToUserName, CreateTime, msg)
                    return web.Response(text=out, content_type='application/xml')
                elif otherName == '我的编号':
                    out = reply_text(FromUserName, ToUserName, CreateTime, base64_encode(FromUserName))
                    return web.Response(text=out, content_type='application/xml')
            elif reply_content=='ok':
                if otherName and len(otherName)>0:
                    PromptServer.instance.user_command[FromUserName]['prompt']=PromptServer.instance.user_command[FromUserName]['prompt']+otherName if 'prompt' in PromptServer.instance.user_command[FromUserName] else otherName
                params=Config().wechat['commands'][PromptServer.instance.user_command[FromUserName]['command']]['params']
                paramName=''
                for param in params:
                    if params[param]['isRequired'] and param not in PromptServer.instance.user_command[FromUserName]:
                        paramName= params[param]['zhName']
                        break
                if paramName!='':
                    out = reply_text(FromUserName, ToUserName, CreateTime, '任务缺乏参数“'+paramName+'”请补充后再提交')
                    return web.Response(text=out, content_type='application/xml')
                resp=setPost(PromptServer.instance,FromUserName)
                if resp!=None:
                    serverAddress=Config().wechat['serverAddress']+'wechatauth/app?openId='+base64_encode(FromUserName)
                    imgUrl='http://mmbiz.qpic.cn/sz_mmbiz_jpg/EpicUicwgk0IGpbYZicuGSXUBaIFWbuDZmBbmDO9PleONOz3FJ3eANEmRicD0eR7mF6PCkxSPxVicbDclQldFKDlHRA/0'
                    out = reply_news(FromUserName, ToUserName, CreateTime, '任务加入队列提醒','任务已加入队列请等待。或可点击访问详情，使用更多功能！',imgUrl,serverAddress)
                    #out = reply_text(FromUserName, ToUserName, CreateTime, '任务已加入队列请等待,详情请访问：\n'+serverAddress)
                    return web.Response(text=out, content_type='application/xml')
            elif reply_content=='recharge' and otherName:
                adminNo=base64_decode(Config().wechat['adminNo'])
                msg=''
                if adminNo==FromUserName:
                    data=otherName.split('加')
                    openId=base64_decode(data[0])
                    tount=int(data[1])
                    if openId and tount>0:
                        db=DataBaseUtil()
                        fdata=db.get_user_frequency(openId)
                        if fdata[0] and fdata[0]>0:
                            db.user_recharge(openId,tount)
                            msg='次数加入成功'
                        else:
                            msg='用户不存在'

                        db.close_con()
                    else:
                        msg='用户编码错误'
                else:
                    msg='无效的指令'
                out = reply_text(FromUserName, ToUserName, CreateTime, msg)
                return web.Response(text=out, content_type='application/xml')
            elif isPrepare:
                msg=''
                if reply_content and otherName!=None:
                    commandName=PromptServer.instance.user_command[FromUserName]['command']
                    if reply_content in Config().wechat['commands'][commandName]['params']:
                        if 'options' in Config().wechat['commands'][commandName]['params'][reply_content]:
                            PromptServer.instance.user_command[FromUserName][reply_content]=Config().wechat['commands'][commandName]['params'][reply_content]['options'][otherName]
                        else:
                            PromptServer.instance.user_command[FromUserName][reply_content]=otherName
                        msg='已填选'+Config().wechat['commands'][commandName]['params'][reply_content]['zhName']+':'+otherName
                else:
                    PromptServer.instance.user_command[FromUserName]['prompt']=PromptServer.instance.user_command[FromUserName]['prompt']+reply_content if 'prompt' in PromptServer.instance.user_command[FromUserName] else reply_content
                    msg='已填入提示词：'+reply_content
                out = reply_text(FromUserName, ToUserName, CreateTime, msg)
                return web.Response(text=out, content_type='application/xml')
            else:
                out = reply_text(FromUserName, ToUserName, CreateTime, reply_content)
                logging.info(out)
                return web.Response(text=out, content_type='application/xml')
        except Exception as e:
            logging.error('消息处理异常:'+str(e))
    elif MsgType == 'image': #图片
        if isPrepare:
            PicUrl=data.find('PicUrl').text
            PromptServer.instance.user_command[FromUserName]['image']=PicUrl
        else:
            out = reply_text(FromUserName, ToUserName, CreateTime, '请先选择指令')
            return web.Response(text=out, content_type='application/xml')
    elif MsgType == 'event': #事件
        try:
            Event = data.find('Event').text
            Event_key = data.find('EventKey').text
            CreateTime = int(time.time())
            # 判断事件，并返回内容
            reply_content = receive_event(Event,Event_key)
            if reply_content:
                out = reply_text(FromUserName, ToUserName, CreateTime, reply_content)
                return web.Response(text=out, content_type='application/xml')
        except Exception as e:
            logging.error('事件处理异常:'+str(e))
    return web.Response(status=200)

PromptServer.instance.send_sync=types.MethodType(send_sync,PromptServer.instance)

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
