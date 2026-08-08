# -*- coding: utf-8 -*-
"""图片/视频组节点。"""


class JyMultiMediaGroup:
    """图片/视频组"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "meida0": ("MEIDA",),
            },
            "optional": {
                "meida1": ("MEIDA",),
            }
        }

    RETURN_TYPES = ("MEIDA_GROUP",)
    FUNCTION = "media_group"
    OUTPUT_NODE = False
    CATEGORY = "lam"

    def media_group(self, **kwargs):
        mediaList = []
        for arg in kwargs:
            if arg.startswith('meida'):
                if type(kwargs[arg]) == list:
                    mediaList.extend(kwargs[arg])
                else:
                    mediaList.append(kwargs[arg])
        return (mediaList,)


NODE_CLASS_MAPPINGS = {"JyMultiMediaGroup": JyMultiMediaGroup}
NODE_DISPLAY_NAME_MAPPINGS = {"JyMultiMediaGroup": "图片/视频组"}


global_var=globals()
newInputs={}
index=0
while True:
    nData=global_var.get("p"+str(index))
    if nData is not None:
        newInputs['meida'+str(index)]=nData
        index+=1
    else:
        break

jmmg=JyMultiMediaGroup()
rdata=jmmg.media_group(**newInputs)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]