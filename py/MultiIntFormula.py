
class MultiIntFormula:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "formula": ('STRING', {"forceInput": False}),

            },
            "optional": {
                "i0": ("INT", {"forceInput": True}),
                "i1": ("INT", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("INT",)
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
        for arg in kwargs:
            if type(kwargs[arg]) != str: 
                continue
            if arg.startswith('text'):
                if return_text=='':
                    return_text = kwargs[arg]
                else:
                    return_text = append_text(return_text, kwargs[arg])

        return (return_text, )
    
NODE_CLASS_MAPPINGS = {
    "MultiIntFormula": MultiIntFormula
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiIntFormula": "多整数计算"
}