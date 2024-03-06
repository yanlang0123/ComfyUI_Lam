
class TextListSelelct:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
             "required": {
                 "i": ("INT", {"default": 0, "min": 0, "max": 99999}),
                "text_list": ("LIST", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "text_list_select"

    CATEGORY = "lam"

    def text_list_select(self, i,text_list):
        return (text_list[i], )
    
NODE_CLASS_MAPPINGS = {
    "TextListSelelct": TextListSelelct
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextListSelelct": "文本列表选择"
}