
class LongTextToList:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
             "required": {
                "text": ("STRING", {"multiline": True,"default":""}),
                "i": ("INT", {"default": 0, "min": 0, "max": 99999}),
                "delimiter": ('STRING', {"forceInput": False}),
            }
        }

    RETURN_TYPES = ("STRING","LIST",'INT',)
    RETURN_NAMES = ('下标i文本', "数组", "数组长度",)
    FUNCTION = "text_to_list"

    CATEGORY = "lam"

    def text_to_list(self,text,i,delimiter):
        delimiter=delimiter.replace("\\n","\n")
        strList=text.split(delimiter)

        return (strList[i],strList,len(strList) )
    
NODE_CLASS_MAPPINGS = {
    "LongTextToList": LongTextToList
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LongTextToList": "文本分割转列表"
}