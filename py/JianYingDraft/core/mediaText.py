"""
 * @file   : materialVideo.py
 * @time   : 15:23
 * @date   : 2024/3/23
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""
from . import template
from .media import Media
from ..utils import tools
from .otherSettings import Text_style
import json


class MediaText(Media):
    def __init__(self,**kwargs):
        kwargs.setdefault("media_type", "text")
        super().__init__(**kwargs)
        
        

    pass

    def _set_material_data_for_content(self):
        ma_id = tools.generate_id()

        self.material_data_for_content['material_animations'] = template.get_speed(ma_id)
        subtitle = self.kwargs.get("text", "")
        color = self.kwargs.get("color", "#000000")
        size = self.kwargs.get("size", 8.0)
        texts=self.__generate_text()
        texts["content"] = self.getContent(subtitle,size,color)
        self.material_data_for_content["texts"] = texts
        # 将素材的各种业务信息，暂时保存起来，后续供track下的segment使用
        self.material_data_for_content["X.extra_material_refs"] = [ma_id, ]

    def __generate_text(self):
        _self = self
        entity = template.get_text(self.id)
        return entity

    def getContent(self,subtitle,size, color):
        r = round(int(color[1:3], 16)/ 255, 6)
        g = round(int(color[3:5], 16)/ 255, 6)
        b = round(int(color[5:7], 16)/ 255, 6)
        
        style=Text_style(size=size,color=(r, g, b))
        content_json = {
            "styles": [
                {
                    "fill": {
                        "alpha": 1.0,
                        "content": {
                            "render_type": "solid",
                            "solid": {
                                "alpha": style.alpha,
                                "color": list(style.color)
                            }
                        }
                    },
                    "range": [0, len(subtitle)],
                    "size": style.size,
                    "bold": style.bold,
                    "italic": style.italic,
                    "underline": style.underline,
                    "strokes": []
                }
            ],
            "text": subtitle
        }
        return json.dumps(content_json, ensure_ascii=False)

