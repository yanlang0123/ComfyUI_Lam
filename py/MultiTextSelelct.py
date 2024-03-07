
class MultiTextSelelct:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
             "required": {
                 "i": ("INT", {"forceInput": True}),
                "text0": ("STRING", {"forceInput": True}),
                "text1": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING","LIST",)
    FUNCTION = "text_to_select"

    CATEGORY = "lam"

    def text_to_select(self, i,**kwargs):
        strList=[]
        for arg in kwargs:
            if type(kwargs[arg]) != str: 
                continue
            if arg.startswith('text'):
                strList.append(kwargs[arg])

        return (strList[i],strList)
    
NODE_CLASS_MAPPINGS = {
    "MultiTextSelelct": MultiTextSelelct
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiTextSelelct": "多文本选择"
}