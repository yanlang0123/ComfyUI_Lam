from server import PromptServer
from aiohttp import web
import os
import json
from .src.wechat.WechatAuthUtils import *
from .src.wechat.DataBaseUtil import DataBaseUtil
from .src.wechat.tool_register import dispatch_tool,get_lm4_tools
import xml.etree.ElementTree as ET
import time
import logging
import queue
import random
import types
import execution
import uuid
import folder_paths
from comfy.cli_args import args
from .src.wechat.redisSub import PubSub,run_with_reconnect,r
from threading import Thread, current_thread
from typing import List, Literal, NamedTuple, Optional
import copy
import asyncio
from zhipuai import ZhipuAI
 
# 创建一个指定长度的队列
maxsize = 10  # 队列的最大长度
client=None
userHistory={}
if len(Config().ai.keys())>0:
    client = ZhipuAI(api_key=Config().ai['api_key'])

def chat_completion(userId):
    tools=get_lm4_tools()
    response = client.chat.completions.create(
            model=Config().ai['model'], # 填写需要调用的模型名称
            messages=userHistory[userId]['messages'],
            tools=tools if Config().ai['is_tools'] else [],
            tool_choice="auto" if Config().ai['is_tools'] else None, #参数设置为 “none” 来强制 API 不返回任何函数的调用。目前函数调用仅支持 auto 模式
            #tool_choice={"type": "function", "function": {"name": "get_ticket_price"}}, #以强制模型生成调用get_ticket_price的参数
        )
    return response
async def ai_auto_reply(msg,userId):
    if client==None or len(msg.strip())==0:
        return 
    if userId not in userHistory or time.time()-userHistory[userId]['time']>5*60:
        userHistory[userId]={'time':time.time(),'messages':[{"role": "system", "content": Config().ai['sys_pompt']}]}
    else:
        while len(userHistory[userId]['messages'])>=maxsize:
            userHistory[userId]['messages'].pop(1)
    userHistory[userId]['messages'].append({"role": "user", "content": msg})
    userHistory[userId]['time'] = time.time()
    try:
        response=chat_completion(userId)
        while response.choices[0].finish_reason=='tool_calls' and len(response.choices[0].message.tool_calls)>0:
            message_handle(response.choices[0].message,userId=userId)
            response = chat_completion(userId)
        userHistory[userId]['messages'].append(nested_object_to_dict(response.choices[0].message))
        reply_text = response.choices[0].message.content
        sendServiceTextMessge(reply_text,userId)
    except Exception as e:
        print(e)
        msg= "AI助手发生错误，您可以发送“帮助”查看使用说明，或联系管理员"
        sendServiceTextMessge(msg,userId)

def message_handle(message,fuctionf=None,userId=''):
    if fuctionf:
        fuction = fuctionf.function
        function_args={}
        if isinstance(fuction.arguments,dict):
            function_args = fuction.arguments
        else:
            function_args = json.loads(fuction.arguments)
        logging.info(f"Tool Name {fuction.name} Rrguments: {fuction.arguments}")
        try:
            if fuction.name == 'resetting_chat_record':
                userHistory[userId]['time']=0
                observation={"success": True,"res": "重置成功" ,"res_type": "text"}
            elif fuction.name == 'generate_image':
                function_args['userId']=userId
                observation=generate_image(**function_args)
            else:
                observation = dispatch_tool(fuction.name, function_args)
        except Exception as e:
            observation = f'api调用错误: {e}'
        if isinstance(observation, dict):
            res = str(observation['res']) if 'res_type' in observation else str(observation)
            tool_response = res
        else:
            tool_response = observation if isinstance(observation, str) else str(observation)
        userHistory[userId]['messages'].append(nested_object_to_dict(message))
        userHistory[userId]['messages'].append({
            "role":"tool",
            "tool_call_id": fuctionf.id,
            "content":tool_response
        })
    else:
        if len(message.tool_calls)>0:
            for call in message.tool_calls:
                message_handle(message,call,userId=userId)
                
def generate_image(prompt,userId,command='文生图'):
    if hasattr(PromptServer.instance,'user_command') and userId in PromptServer.instance.user_command and PromptServer.instance.user_command[userId]['status']=='waiting':
        msg = '您已经在队列中，请勿重复提交！'
        data={'res':msg,'success':False,"res_type": "text"}
        return data

    adminNo=base64_decode(Config().wechat['adminNo'])
    if adminNo!=userId and Config().wechat['freeSize']>0:
        db=DataBaseUtil()
        if db.isUsable:
            data=db.get_user_frequency(userId)
            if data[0]==None:
                db.user_recharge(userId,Config().wechat['freeSize'])
                data=db.get_user_frequency(userId)
            countd=db.get_user_task_count(userId)
            
            if countd[0] >=data[0]:
                msg='非常抱歉，您的免费使用次数已用完，如需继续使用，请扫描右上角二维码，联系管理员。'
                data={'res':msg,'success':False,"res_type": "text"}
                return data
    
    params=Config().wechat['commands'][command]['params']
    paramName=''
    userData={'openId':userId,'command':command,'status':'prepare'}
    if 'type' in Config().wechat['commands'][command]:
        userData['type']=Config().wechat['commands'][command]['type']
    
    if "prompt" in params:
        userData['prompt']=prompt

    if paramName:
        msg = '参数"'+paramName+'"不能为空！'
        data={'res':msg,'success':False,"res_type": "text"}
        return data
    
    if 'seed' in userData:
        if userData['seed'].isdigit()==False or int(userData['seed'])==-1:
            userData['seed']=''.join(random.sample('123456789012345678901234567890',14))
    else:
        userData['seed']=''.join(random.sample('123456789012345678901234567890',14))

    if hasattr(PromptServer.instance,"user_command")==False:
        setattr(PromptServer.instance,"user_command",{})

    PromptServer.instance.user_command[userId]=userData
    resp=setPost(PromptServer.instance,userId)
    if resp!=None:
        while True:
            if userId in PromptServer.instance.user_command and PromptServer.instance.user_command[userId]['status']=='waiting':
                time.sleep(0.5)
            else:
                break
        PromptServer.instance.user_command.pop(userId,None)
        data = {"success": True, "res": "生成成功", "res_type": "image"}
        return data
    else:
        msg='非常抱歉，服务器正忙，请稍后再试！'
        data={'res':msg,'success':False,"res_type": "text"}
        return data
@run_with_reconnect
def subscribe(p):
    while True:
        msg = p.parse_response()
        if msg[0]=='message' and len(msg)==3:
            message=json.loads(msg[2])
            if message['event']=='addTask':
                if Config().redis['isSection']==False:
                    ckptSetCount(message)
                prompt(PromptServer.instance,message['data'])
            elif message['event']=='taskDone':
                task_done(PromptServer.instance.prompt_queue,message['item_id'],message['data'])
            elif message['event']=='sendImage':
                base64_to_file(message['data'],message['filename'],message['type'],message['subfolder'])
            elif message['event']=='dowFile':
                filedata=r.get(message['filename'])
                base64_to_file(filedata,message['filename'],message['type'],message['subfolder'])
                r.delete(message['filename'])
            elif str(message['event'])=='2':
                filedata = Image.open(BytesIO(base64_to_b64decode(message['data'][1])))
                data=tuple([message['data'][0],filedata,message['data'][2]])
                send_sync(PromptServer.instance,message['event'],data,sid=message['sid'],port=message['port'])
            else:
                send_sync(PromptServer.instance,message['event'],message['data'],sid=message['sid'],port=message['port'])
        
    
@run_with_reconnect
def ckptSetCount(message):
    if 'ckptName' in message and message['ckptName']:
        val=r.get('ckpt:'+Config().redis['basePath']+':'+message['ckptName'])
        if val==None:
            val=3
        else:
            val=int(val)+1
        r.set('ckpt:'+Config().redis['basePath']+':'+message['ckptName'],val)
        keys=r.keys('ckpt:'+Config().redis['basePath']+':*')
        for key in keys:
            val=int(r.get(key))
            if val<=1:
                r.delete(key)
            else:
                r.set(key,val-1)
                
@run_with_reconnect
def sendPublish(channel,data):
    if Config().redis['basePath'] == channel:
        jsondata=json.loads(data)
        if jsondata['event']=='addTask':
            ckptSetCount(jsondata)
            rdata=prompt(PromptServer.instance,jsondata['data'])
            if "error" in rdata:
                unique_id=""
                class_type=""
                message=""
                if isinstance(rdata["error"], dict):
                    class_type=rdata["error"]["type"]
                    message=rdata["error"]["message"]
                else:
                    message=str(rdata["error"])

                if "node_errors" in rdata and isinstance(rdata["node_errors"], dict):
                    unique_id = next(iter(rdata["node_errors"]))  # 获取第一个键
                    if len(rdata["node_errors"][unique_id]['errors'])>0:
                        class_type=rdata["node_errors"][unique_id]['errors'][0]["message"]
                        message=rdata["node_errors"][unique_id]['errors'][0]["details"]

                mes = {
                        "prompt_id": jsondata['data']["prompt_id"] if "prompt_id" in jsondata['data'] else '',
                        "node_id": unique_id,
                        "node_type": class_type,
                        "executed": [],
                        "exception_message": message,
                        "exception_type": "ExecutionBlocked",
                        "traceback": [],
                        "current_inputs": [],
                        "current_outputs": [],
                    }
                send_sync(PromptServer.instance,'execution_error', mes, sid=PromptServer.instance.client_id)
            return 
    r.publish(channel,data)

@run_with_reconnect
def refresh_heartbeat(prefix=''):
    print('----心跳线程-----')
    while True:
        val=r.get(prefix+'heartbeat:'+Config().redis['basePath'])
        if val==None:
            val=0
        r.setex(prefix+'heartbeat:'+Config().redis['basePath'], 3, val)
        time.sleep(2)

@run_with_reconnect
def send_sync(self, event, data, sid=None,port=None): #继承父类的send_sync方法
    
    if r :
        if Config().redis['isMain']==False and event not in ['crystools.monitor']:
            mainPath=r.get('mainPath')
            if mainPath:
                if event=='status' and Config().redis['isSection']==False:
                    val=data['status']['exec_info']['queue_remaining']
                    r.setex('heartbeat:'+Config().redis['basePath'], 3, val)
                if event=='executed':
                    if 'images' in data['output']:
                        for img in data['output']['images']:
                            # imgStr=image_to_base64(img['filename'],img['type'],img['subfolder'])
                            # filename=base64_encode(Config().redis['basePath'])+img['filename']
                            # msg={'event':'sendImage','port':Config().redis['basePath'],'filename':filename,'data':imgStr
                            #     ,'type':img['type'],'subfolder':img['subfolder']}
                            # sendPublish(mainPath, json.dumps(msg))
                            # img['filename']=filename
                            filename=base64_encode(Config().redis['basePath'])+img['filename']
                            filedata=file_to_base64(img['filename'],img['type'],img['subfolder'])
                            r.set(filename,filedata)
                            msg={'event':'dowFile','port':Config().redis['basePath'],'filename':filename,'type':img['type'],'subfolder':img['subfolder']}
                            sendPublish(mainPath, json.dumps(msg))
                            img['filename']=filename
                    elif 'gifs' in data['output']:
                        for img in data['output']['gifs']:
                            filename=base64_encode(Config().redis['basePath'])+img['filename']
                            filedata=file_to_base64(img['filename'],img['type'],img['subfolder'])
                            r.set(filename,filedata)
                            msg={'event':'dowFile','port':Config().redis['basePath'],'filename':filename,'type':img['type'],'subfolder':img['subfolder']}
                            sendPublish(mainPath, json.dumps(msg))
                            img['filename']=filename
                elif str(event)=='2':
                    # 创建一个BytesIO对象，用于临时存储图像数据
                    image_data = io.BytesIO()
                    # 将图像保存到BytesIO对象中，格式为JPEG
                    data[1].save(image_data, format='JPEG')
                    filedata=base64_to_b64encode(image_data.getvalue())
                    datalist=[data[0],filedata,data[2]]
                    data=datalist
                msg={'event':event,'port':Config().redis['basePath'],'data':data,'sid':sid}
                sendPublish(mainPath, json.dumps(msg))
                return 
        elif event=='status':
            if port==None:
                val=data['status']['exec_info']['queue_remaining']
                r.setex('heartbeat:'+Config().redis['basePath'], 3, val)
            keys = r.keys('heartbeat:*')
            queue_remaining=0
            for key in keys:
                val=r.get(key)
                if val:
                    queue_remaining+=int(val)

            data['status']['exec_info']['queue_remaining']=queue_remaining

    if hasattr(self,"clientObjPromptId")==False:
        setattr(self,"clientObjPromptId",{})
    if event=='execution_start':
        self.clientObjPromptId[sid]=data['prompt_id']

    if isinstance(data, dict) and 'prompt_id' in data and  data['prompt_id'] in self.clientObjPromptId.values():
        nSid = next(key for key, value in self.clientObjPromptId.items() if value == data['prompt_id'])
        if nSid:
            sid=nSid

    if sid and hasattr(self, "user_command") and sid in getattr(self,'user_command'):
        if event == "executing" and data['node'] is None and data['prompt_id'] == self.user_command[sid]['prompt_id']:
            history=self.prompt_queue.get_history(prompt_id=data['prompt_id'])[data['prompt_id']]
            #print("历史记录======：",history)
            if Config().wechat['isEnterprise'] and ('isWeb' not in self.user_command[sid] or self.user_command[sid]['isWeb']==False):
                textMsgs=[]
                imagePaths=[]
                videoPaths=[]
                for node_id in history['outputs']:
                    node_output = history['outputs'][node_id]
                    if 'wechat_text' in node_output:
                        for text in node_output['wechat_text']:
                            textMsgs.append(text)
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
                if len(textMsgs):
                    text='\n'.join(textMsgs)
                    sendServiceTextMessge(text,sid)
            self.user_command[sid]['status']='wcomplete'
            now = time.localtime()
            end_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
            db=DataBaseUtil()
            if db.isUsable:
                db.update_data('wcomplete', end_time, json.dumps(history['outputs']),data['prompt_id'])
                
            self.user_command[sid].update({'status':'prepare','waitKey':'','seed':''.join(random.sample('123456789012345678901234567890',14))})
        elif  event == "execution_error" and hasattr(self, "user_command") and data['prompt_id'] == self.user_command[sid]['prompt_id']:
            db=DataBaseUtil()
            if db.isUsable:
                db.delete_data(data['prompt_id'])
                
            self.user_command[sid].update({'status':'prepare','waitKey':'','seed':''.join(random.sample('123456789012345678901234567890',14))})

    self.loop.call_soon_threadsafe(
        self.messages.put_nowait, (event, data, sid))
    
MAXIMUM_HISTORY_SIZE = 10000
def task_done(self, item_id,history_result,status: Optional['PromptQueue.ExecutionStatus']=None):
    print('----------task_done--------')
    if status==None:
        self.history[item_id] = history_result
        self.server.send_sync("executing", { "node": None, "prompt_id": item_id }, self.server.client_id)
        return
    
    with self.mutex:
        prompt = self.currently_running.pop(item_id)
        if len(self.history) > MAXIMUM_HISTORY_SIZE:
            self.history.pop(next(iter(self.history)))

        status_dict: Optional[dict] = None
        if status is not None:
            status_dict = copy.deepcopy(status._asdict())

        self.history[prompt[1]] = {
            "prompt": prompt,
            "outputs": {},
            'status': status_dict,
        }
        self.history[prompt[1]].update(history_result)
        if r and Config().redis['isMain']==False :
            mainPath=r.get('mainPath')
            if mainPath:
                sendPublish(mainPath, json.dumps({'event':'taskDone','data':self.history[prompt[1]],'item_id':prompt[1]}))
        self.server.queue_updated()
        
    
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
        
def getCkptName(prompt):
    name=None
    for k,v in prompt.items():
        for k1,v1 in v['inputs'].items():
            if type(v1)==str and k1.startswith('ckpt_name'):
                name=v1
                break
        if name!=None:
            break
    return name

def setPost(self,FromUserName):
    self.user_command[FromUserName]['status']='waiting' #prepare:准备 waiting:待执行  wcomplete完成
    params=self.user_command[FromUserName]
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
    now = time.localtime()
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
    prompt_id=str(uuid.uuid4())
    if r and Config().redis['isMain']:
        self.user_command[FromUserName]['prompt_id']=prompt_id 
        data=selServer(json_data,prompt_id)
        if data:
            db=DataBaseUtil()
            if db.isUsable:
                db.insert_data( params['openId'], json.dumps(params), prompt_id,'waiting',start_time, '', '')
                
            return data
                    
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
            outputs_to_execute = valid[2]
            self.prompt_queue.put((number, prompt_id, prompt, extra_data, outputs_to_execute))
            self.user_command[FromUserName]['prompt_id']=prompt_id 
            db=DataBaseUtil()
            if db.isUsable:
                db.insert_data( params['openId'], json.dumps(params), prompt_id,'waiting',start_time, '', '')
                
            return prompt_id
        else:
            self.user_command[FromUserName]['status']='prepare' # prepare:准备 waiting:待执行  wcomplete完成
            logging.warning("invalid prompt: {}".format(valid[1]))
            return None
        
@run_with_reconnect
def selServer(json_data,prompt_id):
    json_data['prompt_id']=prompt_id
    name=None
    if Config().redis['modelPriority']==True :
        name=getCkptName(json_data['prompt'])
        if name:
            ckkeys=r.keys('ckpt:*:'+name)
            nport=None
            for ckkey in ckkeys:
                ns=ckkey.split(":")
                nport=':'.join(ns[1:3])
                break
            if nport:
                nval = r.get('heartbeat:'+nport)
                if nval!=None:
                    sendPublish(nport, json.dumps({'event':'addTask','data':json_data,'ckptName':name}))
                    return {"prompt_id": prompt_id, "number": 1, "node_errors": []}
                
    keys=r.keys('heartbeat:*')
    if len(keys)>1:
        nameSize={}
        for key in keys:
            val=r.get(key)
            if val!=None :
                ns=key.split(":")
                print(':'.join(ns[1:]))
                ckkeys=r.keys('ckpt:'+':'.join(ns[1:])+':*')
                if int(val)==0 and len(ckkeys)==0:
                    sendPublish(':'.join(ns[1:]), json.dumps({'event':'addTask','data':json_data,'ckptName':name}))
                    return {"prompt_id": prompt_id, "number": 1, "node_errors": []}
                else:
                    nameSize[':'.join(ns[1:])]=int(val)+len(ckkeys)
        print('nameSize:',nameSize)
        minKey=min(key for key, value in nameSize.items() if value == min(nameSize.values()))
        sendPublish(minKey, json.dumps({'event':'addTask','data':json_data,'ckptName':name}))
        return {"prompt_id": prompt_id, "number": 1, "node_errors": []}
    return None

def get_route_keys(endKey, prompt,uniqueIds):
    keys=[]
    for k1,v1 in prompt[endKey]['inputs'].items():
        if type(v1)==list:
            if v1[0] == uniqueIds:
                continue
            keys.append(v1[0])
            keys.extend(get_route_keys(v1[0],prompt,uniqueIds))
    return keys

def section_handle(json_data):
    prompt=json_data['prompt']
    sectionNodeKeys=[x for x in prompt.keys() if 'class_type' in prompt[x] and prompt[x]['class_type']=='SectionEnd']
    for endNum in sectionNodeKeys:
        startNum=prompt[endNum]['inputs']['section'][0]
        server=prompt[startNum]['inputs']['server']
        if server=='default':
            continue
        if 'sectype' in prompt[startNum]['inputs'] and prompt[startNum]['inputs']['sectype']==1:
            continue

        childPrompt={}
        selAllNum=get_route_keys(endNum,prompt,startNum)
        if len(selAllNum)==0:
            prompt[startNum]['inputs']['server']='default'
            continue
        selAllNum=list(set(selAllNum))
        for selNum in selAllNum:
            childPrompt[selNum]=prompt[selNum]
            prompt.pop(selNum, None)
        childPrompt[startNum]=copy.deepcopy(prompt[startNum])
        childPrompt[endNum]=copy.deepcopy(prompt[endNum])
        prompt[startNum]['inputs']['data']=json.dumps({'prompt':childPrompt,'client_id':json_data['client_id']})
        prompt[endNum]['inputs']['images']=[startNum,1]
    return json_data
def trigger_on_prompt(self,json_data,isRun=True):
    if isRun and r and Config().redis['isMain']:
        prompt_id=str(uuid.uuid4())
        data=selServer(json_data,prompt_id)
        if data:
            return data
    json_data=section_handle(json_data)
    return self.old_trigger_on_prompt(json_data)

def prompt(self,json_data):
    json_data=section_handle(json_data)
    json_data = self.old_trigger_on_prompt(json_data)
    if 'prompt_id' in json_data:
        prompt_id=json_data['prompt_id']
    else:
        prompt_id = str(uuid.uuid4())
    try:
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
                if 'prompt_id' in json_data:
                    prompt_id=json_data['prompt_id']
                else:
                    prompt_id = str(uuid.uuid4())
                outputs_to_execute = valid[2]
                self.prompt_queue.put((number, prompt_id, prompt, extra_data, outputs_to_execute))
                response = {"prompt_id": prompt_id, "number": number, "node_errors": valid[3]}
                return response
            else:
                logging.warning("invalid prompt: {}".format(valid[1]))
                return {"error": valid[1], "node_errors": valid[3]}

        else:
            return {"error": "no prompt", "node_errors": []}
    except Exception as e:
        print('prompt处理异常',e)
        return {"error": "prompt处理异常",'node_errors':[]}
    
        
def getTaskRanking(self,FromUserName):
    if 'prompt_id' not in self.user_command[FromUserName]:
        return '您还没有排队，请先发送您的指令'
    prompt_id=self.user_command[FromUserName]['prompt_id']
    current_queue = self.prompt_queue.get_current_queue()
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
        page_number=1
        if 'page_number' in request.rel_url.query:
            page_number=int(request.rel_url.query['page_number'])

        db=DataBaseUtil()
        if db.isUsable:
            datas=db.get_many_data(openId,page_number=page_number)
            
        else:
            datas=[]
        rdataList=[]
        if "type" in request.rel_url.query:
            for data in datas:
                jd=json.loads(data[2])
                if 'type' in jd and request.rel_url.query['type']==jd['type']:
                    rdataList.append(data)
        else:
            rdataList=datas
        return web.Response(text=json.dumps(rdataList), content_type='application/json')
    else:
        data={'msg':'openId 不能为空！','success':False}
        return web.Response(text=json.dumps(data), content_type='application/json')
    
@PromptServer.instance.routes.post("/wechatauth/addTask")
async def addTask(request):
    try:
        if 'api_is_used' in Config().base and Config().base['api_is_used']==False:
            logging.error('服务限制访问')
            data={'msg':'服务限制访问','success':False}
            return web.Response(text=json.dumps(data), content_type='application/json')
        
        post = await request.post()
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
        if adminNo!=openId and Config().wechat['freeSize']>0:
            db=DataBaseUtil()
            if db.isUsable:
                data=db.get_user_frequency(openId)
                if data[0]==None:
                    db.user_recharge(openId,Config().wechat['freeSize'])
                    data=db.get_user_frequency(openId)
                countd=db.get_user_task_count(openId)
                
                if countd[0] >=data[0]:
                    msg='非常抱歉，您的免费使用次数已用完，如需继续使用，请扫描右上角二维码，联系管理员。'
                    data={'msg':msg,'success':False}
                    return web.Response(text=json.dumps(data), content_type='application/json')
        
        params=Config().wechat['commands'][command]['params']
        paramName=''
        userData={'openId':openId,'command':command,'status':'prepare','isWeb':True}
        if 'type' in Config().wechat['commands'][command]:
            userData['type']=Config().wechat['commands'][command]['type']
        
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
        else:
            userData['seed']=''.join(random.sample('123456789012345678901234567890',14))

        if hasattr(PromptServer.instance,"user_command")==False:
            setattr(PromptServer.instance,"user_command",{})

        PromptServer.instance.user_command[openId]=userData
        resp=setPost(PromptServer.instance,openId)
        if resp!=None:
            data={'msg':'任务成功加入队列请等待','prompt_id':resp,'success':True}
            return web.Response(text=json.dumps(data), content_type='application/json')
        else:
            data={'msg':'任务加入队列失败','success':False}
            return web.Response(text=json.dumps(data), content_type='application/json')
    except Exception as e:
        logging.error('任务加入队列处理异常:'+str(e))
        data={'msg':'任务加入队列失败','success':False}
        return web.Response(text=json.dumps(data), content_type='application/json')
    
@PromptServer.instance.routes.get("/wechatauth/getCommands")
async def getCommands(request):
    commands=Config().wechat['commands']
    comms={}
    if "type" in request.rel_url.query:
        type=request.rel_url.query['type']
        for key in commands:
            if 'type' in commands[key] and commands[key]['type']==type:
                comms[key] = commands[key]
    else:
        for key in commands:
            if 'type' not in commands[key]:
                comms[key] = commands[key]
    #type: paint-board
    return web.Response(text=json.dumps(comms), content_type='application/json')

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
        
    startTime=time.time()
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
            reply_content,otherName=receive_msg(Content,isPrepare,isWaiting,FromUserName)
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
                    if db.isUsable:
                        data=db.get_user_frequency(FromUserName)
                        if data[0]==None:
                            db.user_recharge(FromUserName,Config().wechat['freeSize'])
                            data=db.get_user_frequency(FromUserName)
                        countd=db.get_user_task_count(FromUserName)
                        
                        if countd[0] >=data[0]:
                            isAdopt=False
                            msg='非常抱歉，您的免费使用次数已用完,如需继续使用，请联系管理员。微信号：\n'+Config().wechat['adminWeChat']
                        
                if isAdopt:
                    #添加指令的代码
                    if FromUserName in PromptServer.instance.user_command:
                        PromptServer.instance.user_command[FromUserName].update({'openId':FromUserName,'status':'prepare','command':otherName,'waitKey':'','prompt':'','seed':''.join(random.sample('123456789012345678901234567890',14))})
                    else:
                        PromptServer.instance.user_command[FromUserName]={'openId':FromUserName,'status':'prepare','command':otherName,'waitKey':'','seed':''.join(random.sample('123456789012345678901234567890',14))}

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
                elif otherName == '退出':
                    if isPrepare:
                        PromptServer.instance.user_command.pop(FromUserName,None)
                        out = reply_text(FromUserName, ToUserName, CreateTime, '已退出')
                        return web.Response(text=out, content_type='application/xml')
                    else:
                        out = reply_text(FromUserName, ToUserName, CreateTime, '非指令模式无需退出')
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
                    if openId == 'config':
                        Config().reload()
                        msg='配置文件已更新'
                    elif openId and tount>0:
                        db=DataBaseUtil()
                        if db.isUsable:
                            fdata=db.get_user_frequency(openId)
                            if fdata[0] and fdata[0]>0:
                                db.user_recharge(openId,tount)
                                msg='次数加入成功'
                            else:
                                msg='用户不存在'

                            
                        else:
                            msg='数据库连接失败'
                    else:
                        msg='用户编码错误'
                else:
                    msg='无效的指令'
                out = reply_text(FromUserName, ToUserName, CreateTime, msg)
                return web.Response(text=out, content_type='application/xml')
            elif isPrepare:
                msg=''
                commandName=PromptServer.instance.user_command[FromUserName]['command']
                if reply_content in Config().wechat['commands'][commandName]['params'] and 'type' in Config().wechat['commands'][commandName]['params'][reply_content] and Config().wechat['commands'][commandName]['params'][reply_content]['type']=='image':
                    PromptServer.instance.user_command[FromUserName]['waitKey']=reply_content
                    msg='待上传图片参数'+Config().wechat['commands'][commandName]['params'][reply_content]['zhName']
                elif reply_content and otherName!=None:
                    if reply_content in Config().wechat['commands'][commandName]['params']:
                        if 'options' in Config().wechat['commands'][commandName]['params'][reply_content]:
                            PromptServer.instance.user_command[FromUserName][reply_content]=Config().wechat['commands'][commandName]['params'][reply_content]['options'][otherName]
                        else:
                            PromptServer.instance.user_command[FromUserName][reply_content]=otherName
                        msg='已填选'+Config().wechat['commands'][commandName]['params'][reply_content]['zhName']+':'+otherName
                else:
                    PromptServer.instance.user_command[FromUserName]['prompt']= reply_content
                    msg='已填入提示词：'+reply_content
                out = reply_text(FromUserName, ToUserName, CreateTime, msg)
                return web.Response(text=out, content_type='application/xml')
            else:
                # 调用异步函数而不等待其结果
                asyncio.create_task(ai_auto_reply(reply_content,FromUserName))
                return web.Response(status=200)
        except Exception as e:
            logging.error('消息处理异常:'+str(e))
    elif MsgType == 'image': #图片
        if isPrepare:
            PicUrl=data.find('PicUrl').text
            commandName=PromptServer.instance.user_command[FromUserName]['command']
            msg=''
            if PromptServer.instance.user_command[FromUserName]['waitKey']:
                PromptServer.instance.user_command[FromUserName][PromptServer.instance.user_command[FromUserName]['waitKey']]=PicUrl
                msg='已上传图片参数'+Config().wechat['commands'][commandName]['params'][PromptServer.instance.user_command[FromUserName]['waitKey']]['zhName']
                PromptServer.instance.user_command[FromUserName]['waitKey']=''
            elif 'image' in Config().wechat['commands'][commandName]['params']:
                PromptServer.instance.user_command[FromUserName]['image']=PicUrl
                msg='已上传图片参数'+Config().wechat['commands'][commandName]['params']['image']['zhName']

            out = reply_text(FromUserName, ToUserName, CreateTime, msg)
            return web.Response(text=out, content_type='application/xml')
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

custom_nodes_path=folder_paths.get_folder_paths('custom_nodes')[0]
custom_nodes_path=os.path.join(custom_nodes_path,'AIGODLIKE-ComfyUI-Translation')
custom_nodes_path=os.path.join(custom_nodes_path,Config().base.get('language','zh-CN'),'Nodes') 
NODE_LANGEUAGE_DISPLAY_NAME_MAPPINGS={}
if os.path.exists(custom_nodes_path):
    for file in os.listdir(custom_nodes_path):
        if file.endswith('.json'):
            json_file=os.path.join(custom_nodes_path, file)
            if os.path.isfile(json_file):
                f = open(json_file,'r', encoding='utf-8')
                data = json.load(f)
                f.close()
                for key in data:
                    if 'title' in data[key]:
                         NODE_LANGEUAGE_DISPLAY_NAME_MAPPINGS[key]=data[key]['title']

PromptServer.instance.send_sync=types.MethodType(send_sync,PromptServer.instance)
PromptServer.instance.old_trigger_on_prompt=PromptServer.instance.trigger_on_prompt
PromptServer.instance.trigger_on_prompt=types.MethodType(trigger_on_prompt,PromptServer.instance)
setattr(PromptServer.instance,"displayName",NODE_LANGEUAGE_DISPLAY_NAME_MAPPINGS)
if hasattr(PromptServer.instance,"pub")==False and r: #添加订阅消息
    setattr(PromptServer.instance,"pub",PubSub().subscribe(Config().redis['basePath']))
    if Config().redis['isMain']:
        r.set('mainPath',Config().redis['basePath'])
    keys=r.keys('ckpt:'+Config().redis['basePath']+':*')
    for key in keys:
        r.delete(key)
    prefix=''
    if Config().redis['isSection']:
        prefix='section'
    Thread(target=refresh_heartbeat,daemon=True, args=(prefix,)).start()
    Thread(target=subscribe,daemon=True, args=(PromptServer.instance.pub,)).start()
    if PromptServer.instance.prompt_queue:
        PromptServer.instance.prompt_queue.task_done=types.MethodType(task_done,PromptServer.instance.prompt_queue)

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
