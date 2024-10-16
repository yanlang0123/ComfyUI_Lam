import requests
import hashlib
import io
import cv2
import json
from .config import Config
import time
import logging
import folder_paths
import base64
from PIL import Image
from io import BytesIO
import os

def nested_object_to_dict(obj):
    if isinstance(obj, list):
        return [nested_object_to_dict(x) for x in obj]
    if isinstance(obj, dict):
        return {k: nested_object_to_dict(v) for k, v in obj.items()}
    if  obj and type(obj) not in (int, float, str):
        return nested_object_to_dict(vars(obj))
    else:
        return obj

def file_to_base64(filename,type='output', subfolder=None):
    if type=="temp":
        output_dir = folder_paths.get_temp_directory()
    else:
        output_dir = folder_paths.get_output_directory()
    if subfolder:
        file_path=os.path.join(output_dir,subfolder,filename)
    else:
        file_path=os.path.join(output_dir,filename)
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode("utf-8")
 
def base64_to_file(base64_string,filename,type='output', subfolder=None):
    image_data = base64.b64decode(base64_string)
    if type=="temp":
        output_dir = folder_paths.get_temp_directory()
    else:
        output_dir = folder_paths.get_output_directory()
    if subfolder:
        file_path=os.path.join(output_dir,subfolder,filename)
    else:
        file_path=os.path.join(output_dir,filename)
    with open(file_path, 'wb') as file:
        file.write(image_data)
    return filename

def base64_to_b64encode(file_data):
    fileData = base64.b64encode(file_data)
    return fileData.decode("utf-8")

def base64_to_b64decode(base64_string):
    fileData = base64.b64decode(base64_string)
    return fileData

def base64_encode(text):
    '''加密'''
    encoded_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    return encoded_text


def base64_decode(encoded_text):
    '''解密'''
    decoded_text = base64.b64decode(encoded_text).decode('utf-8')
    return decoded_text


"""这是一个处理客户发送信息的文件"""


def reply_text(FromUserName, ToUserName, CreateTime, Content):
    """回复文本消息模板"""
    textTpl = """<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[%s]]></MsgType> <Content><![CDATA[%s]]></Content></xml>"""
    out = textTpl % (FromUserName, ToUserName, CreateTime, 'text', Content)
    return out


"""图片文消息"""


def reply_news(FromUserName, ToUserName, CreateTime, Title, Description, PicUrl, Url):
    textTpl = """
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                    <item>
                    <Title><![CDATA[%s]]></Title>
                    <Description><![CDATA[%s]]></Description>
                    <PicUrl><![CDATA[%s]]></PicUrl>
                    <Url><![CDATA[%s]]></Url>
                    </item>
                </Articles>
                </xml>
            """
    out = textTpl % (FromUserName, ToUserName, CreateTime,
                     Title, Description, PicUrl, Url)
    return out


def getCommandMsg(command, isEnterprise):
    keyNames = ['image', 'seed', 'prompt', 'negative']
    if isEnterprise:
        comList = []
        names = []
        otherParamsStr=''
        index = 0
        for key in command['params']:
            if key in keyNames:
                continue

            requiredText='（必填）' if command['params'][key]['isRequired'] else '（选填）'
            if 'options' in command['params'][key]:
                names.append(command['params'][key]['zhName']+requiredText)
                for option in command['params'][key]['options']:
                    comList.append({"id": index, "content": key+':'+option})
                    index += 1
            else:
                otherParamsStr+='\n参数“'+command['params'][key]['zhName']+requiredText+'”指令=》'+key+':'+str(command['params'][key]['default'])


        if len(names) > 0 and len(comList) > 0:
            return '您可以选择以下指令来选择('+','.join(names)+')'+otherParamsStr, comList
        else:
            if len(otherParamsStr)>0:
                return '您可以输入以下指令：'+otherParamsStr+'\n'+command['replyText'], None
            return command['replyText'], None
    else:
        names = []
        comList = []
        otherParamsStr=''
        for key in command['params']:
            if key in keyNames:
                continue

            requiredText='（必填）' if command['params'][key]['isRequired'] else '（选填）'
            if 'options' in command['params'][key]:
                names.append(command['params'][key]['zhName']+requiredText)
                for option in command['params'][key]['options']:
                    comList.append(key+':'+option)
            else:
                otherParamsStr+='\n参数“'+command['params'][key]['zhName']+requiredText+'”命令=》'+key+':'+str(command['params'][key]['default'])
        return '您可以执行以下命令:\n'+'\n'.join(comList)+'\n,选择》'+','.join(names)+otherParamsStr+'\n'+command['replyText'], None


def receive_msg(msg, isPrepare=False, isWaiting=False,userId=''):
    # 这是一个将疑问改成成熟句子的函数，例如：你好吗 公众号回复：你好
    commands = Config().wechat['commands']
    isEnterprise = Config().wechat['isEnterprise']
    query_commands = Config().wechat['query_commands']
    if msg == u'帮助':
        comList = []
        index = 0
        for key in commands:
            if 'type' not in commands[key]:
                comList.append({"id": index, "content": key})
                index += 1
        for key in query_commands:
            comList.append({"id": index, "content": key})
            index += 1
        if isEnterprise == False:
            comNames = [x['content'] for x in comList]
            return '您可以执行以下操作：\n'+'\n'.join(comNames), None
        return 'menu', comList
    elif isWaiting == False and msg in commands:
        return 'command', msg
    elif msg in query_commands:
        return 'query', msg
    elif isPrepare:
        if msg.find(':') != -1:
            keyName=msg.split(':')[0]
            value=msg[len(keyName)+1:]
            return keyName,value
        elif (msg.lower().endswith(u'ok') or msg.lower() == 'ok'):
            return 'ok', msg[:-2]
        else:
            return msg, None
    elif msg.find('加') != -1 and len(msg.split('加')) == 2:
        return 'recharge', msg
    elif isWaiting and msg in commands:
        return '任务已加入队列请等待...', None
    else:
        return msg, None


def receive_event(event, key):
    # 如果是关注公众号事件
    if event == 'subscribe':
        return Config().wechat.get("subscribeMsg", "感谢关注！您可以发送“帮助”查看使用说明")
    # 如果是点击菜单拉取消息事件
    elif event == 'CLICK':
        # 接下来就是根据你点击不同的菜单拉去不同的消息啦
        # 我为了省事，不进行判断啦，如果需要判断请根据 key进行判断
        return "你点击了菜单"+key
    # 如果是点击菜单跳转Url事件，不做任何处理因为微信客户端会自行处理
    elif event == 'VIEW':
        return None


def getAccessToken():
    if Config().wechat['access_token_expires_at'] <= 0 or time.time() >= Config().wechat['access_token_expires_at']:
        APPID = Config().wechat['appid']
        SECRET = Config().wechat['secret']
        token_url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}'
        resResult = requests.get(token_url)
        data = resResult.json()
        if 'access_token' in data:
            access_token = data['access_token']
            Config().wechat['access_token'] = access_token
            Config().wechat['access_token_expires_at'] = time.time(
            )+data['expires_in']-60
            Config().save_config()
            return access_token
        else:
            logging.info(token_url)
            logging.error('获取access_token失败'+str(data))

    else:
        return Config().wechat['access_token']

def sendServiceTextMessge(content,touser):
    message={
            "touser":touser,
            "msgtype":"text",
            "text":
            {
                "content":content
            }
        }
    return sendServiceMessage(message)
def sendServiceImageMessge(media_id, touser):  # 发送图片
    message = {
        "touser": touser,
        "msgtype": 'image',
        "image": {
            "media_id": media_id,
        }
    }
    return sendServiceMessage(message)


def sendServiceVideoMessge(media_id, title, desc, touser):  # 发送视频
    message = {
        "touser": touser,
        "msgtype": "video",
        "video": {
            "media_id": media_id,
            "title": title,
            "description": desc,
        }
    }
    return sendServiceMessage(message)


# 发送菜单 menu_list = [{"id":"1","content":"菜单1"},{"id":"2","content":"菜单2"}]
def sendServiceMenuMessage(head_content, tail_content, menu_list, touser):
    message = {
        "touser": touser,
        "msgtype": "msgmenu",
        "msgmenu": {
            "head_content": head_content,
            "list": menu_list,
            "tail_content": tail_content
        }
    }
    return sendServiceMessage(message)


def sendServiceMessage(message):
    access_token = getAccessToken()
    url = f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}'
    data = json.dumps(message, ensure_ascii=False).encode('utf-8')
    resResult = requests.post(url, data=data)
    data = resResult.json()
    if data['errcode'] == 0:
        return True
    else:
        logging.error('发送消息失败'+str(data))
        return False


def sendServiceTyping(touser):  # 下发正在输入状态
    accessToken = getAccessToken()
    url = f'https://api.weixin.qq.com/cgi-bin/message/custom/typing?access_token={accessToken}'
    message = {"touser": touser, "command": "Typing"}
    data = json.dumps(message, ensure_ascii=False).encode('utf-8')
    resResult = requests.post(url, data=data)
    data = resResult.json()
    if data['errcode'] == 0:
        return True
    else:
        logging.error('正在输入状态失败'+str(data))
        return False


# 上传临时/永久素材
# 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
def getMediaId(image_path, type, isTemporary=True):
    access_token = getAccessToken()
    if(isTemporary):
        url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type={type}"
    else:
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type={type}"

    files = {'media': open(image_path, 'rb')}
    resResult = requests.post(url, files=files)
    data = resResult.json()
    if 'media_id' in data:
        return data['media_id']
    else:
        logging.error('素材上传失败'+str(data))
        return None
