# -*- coding: utf-8 -*-
"""特效组节点。"""


class JyMultiEffectGroup:
    """特效组"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "effect0": ("JY_EFFECT",),
            },
            "optional": {
                "effect1": ("JY_EFFECT",),
            }
        }

    RETURN_TYPES = ("EFFECT_GROUP",)
    FUNCTION = "effect_group"
    OUTPUT_NODE = False
    CATEGORY = "lam"

    def effect_group(self, **kwargs):
        mediaList = []
        for arg in kwargs:
            if arg.startswith('effect'):
                mediaList.append(kwargs[arg])
        return (mediaList,)


NODE_CLASS_MAPPINGS = {"JyMultiEffectGroup": JyMultiEffectGroup}
NODE_DISPLAY_NAME_MAPPINGS = {"JyMultiEffectGroup": "特效组"}


global_var=globals()
newInputs={}
index=0
while True:
    nData=global_var.get("p"+str(index))
    if nData is not None:
        newInputs['effect'+str(index)]=nData
        index+=1
    else:
        break

jmeg=JyMultiEffectGroup()
rdata=jmeg.effect_group(**newInputs)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]