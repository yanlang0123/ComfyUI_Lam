import os
import shutil
import uuid
import json
import sys
import time
# sys.path.append(r"scripts\JianyingDraft")

# from BasicLibrary.io.dirHelper import DirHelper
from .innerBizTypes import *
from .dataStruct import TransitionData, EffectData, AnimationData, AnimationTypes


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


def generate_effect_data(name_or_resource_id: str | int) -> EffectData:
    """
    生成转场数据
    :param name_or_resource_id: 动画名称或资源id
    """
    resource_id = "7012933493663470088"  # 缺省的特效资源ID表示小花花特效
    name = "小花花"

    if isinstance(name_or_resource_id, str):
        name = name_or_resource_id

        if name in effectDict:
            resource_id = effectDict[name]
        pass
    elif isinstance(name_or_resource_id, int):
        resource_id = str(name_or_resource_id)
        name = resource_id
    pass

    return EffectData(
        guid=generate_id(),
        resource_id=resource_id,
        name=name
    )


def generate_transition_data(name_or_resource_id: str | int, duration=0) -> TransitionData:
    """
    生成转场数据
    :param name_or_resource_id: 动画名称或资源id
    :param duration: 持续时间
    """
    resource_id = "6724239388189921806"  # 缺省的转场资源ID表示闪黑
    name = "闪黑"
    if isinstance(name_or_resource_id, str):
        name = name_or_resource_id

        if name in transitionDict:
            resource_id = transitionDict[name]
        pass
    elif isinstance(name_or_resource_id, int):
        resource_id = str(name_or_resource_id)
        name = resource_id
    pass

    return TransitionData(
        guid=generate_id(),
        resource_id=resource_id,
        duration=duration,
        name=name
    )


def generate_animation_data(name_or_resource_id: str | int, animation_type: AnimationTypes = "in", start=0,
                            duration=0) -> AnimationData:
    """
    生成动画数据
    :param animation_type: 动画类型 in/out/group
    :param name_or_resource_id: 动画名称或资源id
    :param start:
    :param duration: 持续时间
    """
    resource_id = ""  # 缺省的动画资源ID
    name = ""
    if isinstance(name_or_resource_id, str):
        name = name_or_resource_id

        if animation_type == "in" and name in animationInDict:
            resource_id = animationInDict[name]
        pass

        if animation_type == "out" and name in animationOutDict:
            resource_id = animationOutDict[name]
        pass

        if animation_type == "group" and name in animationGroupDict:
            resource_id = animationGroupDict[name]
        pass
    elif isinstance(name_or_resource_id, int):
        resource_id = str(name_or_resource_id)
        name = resource_id
    pass

    return AnimationData(
        guid=generate_id(),
        resource_id=resource_id,
        duration=duration,
        animation_type=animation_type,
        start=start,
        name=name
    )


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
    

# @classmethod
# def get_date_lunar(cls, solar_date=None, result_with_year=True):
#     """
#     获取给定阳历日期的阴历表示（比如）
#     :param result_with_year:结果中是否包含用干支表示的年份
#     :param solar_date:待转换的公历日期
#     :return:
#     """
#     if solar_date is None:
#         solar_date = datetime.now()
#     pass

#     if ObjectHelper.get_type(solar_date) is str:
#         solar_date = cls.convert_from_string(solar_date)
#     pass

#     lunar_date = solar2lunar(solar_date.year, solar_date.month, solar_date.day)

#     result = ""
#     if result_with_year is True:
#         lunar_year = lunar_date.getYearGZ()
#         lunar_year_string = ChineseData.TianG[lunar_year.tg] + ChineseData.DiZ[lunar_year.dz]
#         result = StringHelper.format("{0}年", lunar_year_string)
#     pass

#     if lunar_date.isLunarLeap():
#         result += "闰"
#     pass

#     result += StringHelper.format("{0}月{1}日", ChineseData.YueM[lunar_date.getLunarMonth() - 1],
#                                 ChineseData.RiM[lunar_date.getLunarDay() - 1])

#     return result

# pass


if __name__ == '__main__':
    print(get_timestamp(format=5))