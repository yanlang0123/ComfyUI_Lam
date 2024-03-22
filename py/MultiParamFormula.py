from .src.utils.uitls import AlwaysEqualProxy,AlwaysTupleZero
class MultiParamFormula:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "expression": ("STRING",{"multiline": True}),
            },
            "optional": {
                "p0": (AlwaysEqualProxy("*"), ),
                "p1": (AlwaysEqualProxy("*"), ),
            }
        }

    RETURN_TYPES = AlwaysTupleZero(AlwaysEqualProxy("*"),)
    RETURN_NAMES = ('p0',)
    FUNCTION = "evaluate"
    CATEGORY = "lam"
    OUTPUT_NODE = True

    def evaluate(self, expression, **kwargs):
        lookup = {}
        for arg in kwargs:
            lookup[arg] = kwargs[arg]
        
        msg='完成'
        r=""
        try:
            r = eval(expression, lookup)
        except Exception as e:
            msg='表达式错误'

        if not isinstance(r, tuple):
            r = (r,)

        return {"ui": {"value": [msg]}, "result": r}
    
NODE_CLASS_MAPPINGS = {
    "MultiParamFormula": MultiParamFormula
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiParamFormula": "多参代码表达式"
}