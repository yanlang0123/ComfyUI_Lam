
class MultiTextConcatenate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "linebreak_addition": (['false', 'true'],),
                "text0": ("STRING", {"forceInput": True}),
                "text1": ("STRING", {"forceInput": True}),
            },
            "optional": {
                "delimiter": ('STRING', {"forceInput": False}),
            }
        }

    RETURN_TYPES = ("STRING","LIST",)
    FUNCTION = "text_concatenate"

    CATEGORY = "lam"

    def text_concatenate(self, linebreak_addition='false', delimiter='',**kwargs):
        # Initialize return_text with text_
        def append_text(base_text, new_text):
            if linebreak_addition == 'true':
                return base_text + delimiter + "\n" + new_text
            else:
                return base_text + delimiter + new_text
        return_text=''
        strList=[]
        for arg in kwargs:
            if type(kwargs[arg]) != str: 
                continue
            if arg.startswith('text'):
                strList.append(kwargs[arg])
                if return_text=='':
                    return_text = kwargs[arg]
                else:
                    return_text = append_text(return_text, kwargs[arg])

        return (return_text,strList, )
    
NODE_CLASS_MAPPINGS = {
    "MultiTextConcatenate": MultiTextConcatenate
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiTextConcatenate": "多文本联合"
}