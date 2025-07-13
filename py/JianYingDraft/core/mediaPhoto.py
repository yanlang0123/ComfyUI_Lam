"""
 * @file   : materialVideo.py
 * @time   : 15:23
 * @date   : 2024/3/23
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""
from ...src.wechat.config import Config

from . import template
from .mediaVideo import MediaVideo
from ..utils import tools


# TODO:xiedali@2024/03/27 功能需要实现

class MediaPhoto(MediaVideo):
    
    

    def _init_basic_info_after(self):
        """
        在初始化基础属性后加载逻辑（供派生类使用）
        """
        # duration = self.kwargs.get("duration", 0)
        if self.duration == 0:
            duration = Config().jianYing['image_duration']
            self.duration = duration
        pass

    def _set_material_data_for_content(self):
        super()._set_material_data_for_content()
        self.material_data_for_content["videos"]["type"]="photo"


pass
