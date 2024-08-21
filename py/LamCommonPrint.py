from .src.utils.uitls import AlwaysEqualProxy
class LamCommonPrint:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "obj": (AlwaysEqualProxy("*"),),
            }
        }
    RETURN_TYPES = (AlwaysEqualProxy("*"),)

    RETURN_NAMES = ('obj',)

    FUNCTION = "common_print"

    OUTPUT_NODE = True

    CATEGORY = "lam"

    def common_print(self,obj):
        return {"ui": {"text": str(obj)}, "result": (obj, )}

NODE_CLASS_MAPPINGS = {
    "LamCommonPrint": LamCommonPrint
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamCommonPrint": "通用打印输出"
}
