import os
import shutil
import uuid
import json
import sys
import time

def generate_id() -> str:
    """
    生成uuid
    """
    return str(uuid.uuid4()).upper()


def read_json(path):
    """
    读取json文件
    :param path: 文件路径
    """
    with open(path, 'r',encoding="UTF-8") as file:
        return json.load(file)
    pass


def write_json(path, data):
    """
    写入json文件
    :param path: 文件路径
    :param data: 数据
    """
    with open(path, 'w') as file:
        # 给json.dump添加参数 ensure_ascii=false可以保证汉字不被编码
        json.dump(data, file)
    pass


def create_folder(folder_path):
    """
    创建文件夹
    :param folder_path: 文件夹路径
    """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
       
    pass

    # DirHelper.ensure_exist(folder_path)
    os.mkdir(folder_path)
'''
 * 获取文件名不带扩展名
 * @param filename
 * @returns {string}
'''
def get_file_name_no_ext(filename):
    basename=os.path.basename(filename)
    if basename.find(".") == -1:
        return basename
    return os.path.splitext(basename)[0]


def get_timestamp(format=16):
    """获取当前时间的Unix时间戳"""
    timestamp = time.time()*1000000
    timestamp = str(timestamp)[0:format if format <= 17 else 17]
    return int(timestamp)
    