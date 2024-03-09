from .src.utils.uitls import AlwaysEqualProxy
class IfInnerExecute:
    """
    内判断选择
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ANY": (AlwaysEqualProxy("*"),),
                "IF_TRUE": (AlwaysEqualProxy("*"),),
                "IF_FALSE": (AlwaysEqualProxy("*"),),
            }
        }

    RETURN_TYPES = (AlwaysEqualProxy("*"),)

    RETURN_NAMES = "?"

    FUNCTION = "return_based_on_bool"

    CATEGORY = "lam"
    OUTPUT_NODE = True

    def return_based_on_bool(self, ANY, IF_TRUE, IF_FALSE):
        return {"ui": {"value": [True if ANY else False]}, "result": (IF_TRUE if ANY else IF_FALSE,)}
    
NODE_CLASS_MAPPINGS = {
    "IfInnerExecute": IfInnerExecute
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IfInnerExecute": "判断选择"
}