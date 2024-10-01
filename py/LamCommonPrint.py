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
    
class LamCommonPrintNoOutput:
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

    OUTPUT_NODE = False

    CATEGORY = "lam"

    def common_print(self,obj):
        return {"ui": {"text": str(obj)}, "result": (obj, )}

NODE_CLASS_MAPPINGS = {
    "LamCommonPrint": LamCommonPrint,
    "LamCommonPrintNoOutput":LamCommonPrintNoOutput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamCommonPrint": "通用打印输出",
    "LamCommonPrintNoOutput": "通用打印输出(非输出节点)"
}
