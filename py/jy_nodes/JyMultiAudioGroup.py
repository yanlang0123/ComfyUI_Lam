# -*- coding: utf-8 -*-
"""音频组节点。"""


class JyMultiAudioGroup:
    """音频组"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio0": ("JY_AUDIO",),
            },
            "optional": {
                "audio1": ("JY_AUDIO",),
            }
        }

    RETURN_TYPES = ("AUDIO_GROUP",)
    FUNCTION = "audio_group"
    OUTPUT_NODE = False
    CATEGORY = "lam"

    def audio_group(self, **kwargs):
        mediaList = []
        for arg in kwargs:
            if arg.startswith('audio'):
                mediaList.append(kwargs[arg])
        return (mediaList,)


NODE_CLASS_MAPPINGS = {"JyMultiAudioGroup": JyMultiAudioGroup}
NODE_DISPLAY_NAME_MAPPINGS = {"JyMultiAudioGroup": "音频组"}


global_var=globals()
newInputs={}
index=0
while True:
    nData=global_var.get("p"+str(index))
    if nData is not None:
        newInputs['audio'+str(index)]=nData
        index+=1
    else:
        break

jmag=JyMultiAudioGroup()
rdata=jmag.audio_group(**newInputs)
if isinstance(rdata, tuple):
    result=rdata
elif "result" in rdata:
    result=rdata["result"]
    if "ui" in rdata:
        ui= rdata["ui"]