# -*- coding: utf-8 -*-

import os
import shutil
import functools
import yaml
import folder_paths

def singleton(cls):
    """
    将一个类作为单例
    来自 https://wiki.python.org/moin/PythonDecoratorLibrary#Singleton
    """

    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
        it.__init_original__(*args, **kw)
        return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    return cls

@singleton
class Config(object):
    def __init__(self) -> None:
        basePath=folder_paths.folder_names_and_paths['custom_nodes'][0][0]
        self.pwd = os.path.join(basePath,'ComfyUI_Lam','config')
        self.reload()

    def _load_config(self) -> dict:
        try:
            with open(f"{self.pwd}/weChat.yaml", "rb") as fp:
                yconfig = yaml.safe_load(fp)
        except FileNotFoundError:
            shutil.copyfile(f"{self.pwd}/weChat.yaml.template", f"{self.pwd}/weChat.yaml")
            with open(f"{self.pwd}/weChat.yaml", "rb") as fp:
                yconfig = yaml.safe_load(fp)

        return yconfig
    
    def save_config(self):
        yconfig = self._load_config()
        yconfig["wechat"] = self.wechat
        with open(f"{self.pwd}/weChat.yaml", 'w', encoding='utf-8') as file:
            yaml.dump(yconfig, file,sort_keys=False,default_flow_style=False,allow_unicode=True, encoding='utf-8')

    def reload(self) -> None:
        yconfig = self._load_config()
        self.wechat = yconfig.get("wechat", {})
        self.redis = yconfig.get("redis", {})
        self.base = yconfig.get("base", {})
        #self.EMAIL= yconfig.get("email", {})
        #self.OPENAI= yconfig.get("openai", {})
        #self.GLM4= yconfig.get("glm4", {})
        #self.COMFY_UI=yconfig.get("comfyUI", {})
  
