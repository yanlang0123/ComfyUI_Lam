class MultiIntFormula:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "expression": ("STRING",{"multiline": True}),
            },
            "optional": {
                "n0": ("INT,FLOAT", ),
                "n1": ("INT,FLOAT", ),
            }
        }

    RETURN_TYPES = ("INT","FLOAT",)
    FUNCTION = "evaluate"
    CATEGORY = "lam"
    OUTPUT_NODE = True

    def evaluate(self, expression, **kwargs):
        lookup = {}
        for arg in kwargs:
            if type(kwargs[arg]) == int or type(kwargs[arg])== float:
                lookup[arg] = kwargs[arg]
        msg=None
        r=0
        try:
            r = eval(expression, lookup)
            msg=[r]
        except Exception as e:
            msg=["表达式错误"]
        return {"ui": {"value": msg}, "result": (int(r), float(r),)}
    
NODE_CLASS_MAPPINGS = {
    "MultiIntFormula": MultiIntFormula
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiIntFormula": "多参数学表达式"
}