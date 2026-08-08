# -*- coding: utf-8 -*-
"""字幕组节点。"""


class JyMultiCaptionsGroup:
    """字幕组"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "captions0": ("JY_CAPTIONS",),
            },
            "optional": {
                "captions1": ("JY_CAPTIONS",),
            }
        }

    RETURN_TYPES = ("CAPTIONS_GROUP",)
    FUNCTION = "captions_group"
    OUTPUT_NODE = False
    CATEGORY = "lam"

    def captions_group(self, **kwargs):
        mediaList = []
        for arg in kwargs:
            if arg.startswith('captions'):
                mediaList.append(kwargs[arg])
        return (mediaList,)


NODE_CLASS_MAPPINGS = {"JyMultiCaptionsGroup": JyMultiCaptionsGroup}
NODE_DISPLAY_NAME_MAPPINGS = {"JyMultiCaptionsGroup": "字幕组"}


global_var=globals()
newInputs={}
index=0
while True:
    nData=global_var.get("p"+str(index))
    if nData is not None:
        newInputs['captions'+str(index)]=nData
        index+=1
    else:
        break

jmcg=JyMultiCaptionsGroup()
rdata=jmcg.captions_group(**newInputs)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]