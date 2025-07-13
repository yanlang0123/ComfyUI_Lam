# -*- coding: utf-8 -*-

import os
import shutil
import functools
import yaml
import folder_paths
from comfy.cli_args import args

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
                fp.close()

        return yconfig
    
    def save_config(self):
        yconfig = self._load_config()
        yconfig["wechat"] = self.wechat
        yconfig["base"] = self.base
        yconfig["commands"] = self.commands
        yconfig["jian_ying"] = self.jianYing
        with open(f"{self.pwd}/weChat.yaml", 'w', encoding='utf-8') as file:
            yaml.dump(yconfig, file,sort_keys=False,default_flow_style=False,allow_unicode=True, encoding='utf-8')
            file.close()

    def reload(self) -> None:
        yconfig = self._load_config()
        self.wechat = yconfig.get("wechat", {})
        self.base = yconfig.get("base", {})
        self.ai = yconfig.get("ai", {})
        self.redis = yconfig.get("redis", {})
        self.commands= yconfig.get("commands", {})
        self.jianYing= yconfig.get("jian_ying", {})
        if "cluster" in args and args.cluster:
            self.cluster = yconfig.get("cluster", {})
            self.cluster["isSection"] = args.isSection
            if args.isSection:
                self.cluster["isMain"] = False
            else:
                self.cluster["isMain"] = args.isMain
            self.cluster["basePath"] = args.basePath+":"+str(args.port)
        else:
            self.cluster = None
        #self.EMAIL= yconfig.get("email", {})
        #self.OPENAI= yconfig.get("openai", {})
        #self.GLM4= yconfig.get("glm4", {})
        #self.COMFY_UI=yconfig.get("comfyUI", {})
  
