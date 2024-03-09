from .src.utils.uitls import AlwaysEqualProxy
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

    RETURN_TYPES = (AlwaysEqualProxy("*"),)
    FUNCTION = "evaluate"
    CATEGORY = "lam"

    def evaluate(self, expression, **kwargs):
        lookup = {}
        for arg in kwargs:
            lookup[arg] = kwargs[arg]
        r = eval(expression, lookup)
        return (r,)
    
NODE_CLASS_MAPPINGS = {
    "MultiParamFormula": MultiParamFormula
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiParamFormula": "多参代码表达式"
}