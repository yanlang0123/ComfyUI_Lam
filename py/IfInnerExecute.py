from .src.utils.uitls import AlwaysEqualProxy
class IfInnerExecute:
    """
    内判断选择
    """
    DESCRIPTION = """
    入参：ANY 输入任意类型，用于判断是否，主要是条件，比如 p0>p1 或整数型0 或者 1
    IF_TRUE 任意类型 ：ANY 判断为True时出参参数为此参数
    IF_TRUE 任意类型 ：ANY 判断为False时出参参数为此参数
    输出参数：类型根据IF_TRUE或者IF_TRUE一致
    实例：
    ANY = 1      IF_TRUE = 2  IF_FALSE = 3  输出：2
    ANY = 0      IF_TRUE = 2  IF_FALSE = 3  输出：3
    ANY = True   IF_TRUE = 2  IF_FALSE = 3  输出：2
    ANY = False  IF_TRUE = 2  IF_FALSE = 3  输出：3
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ANY": (AlwaysEqualProxy("*"),),
                "IF_TRUE": (AlwaysEqualProxy("*"),{"lazy":True}),
                "IF_FALSE": (AlwaysEqualProxy("*"),{"lazy":True}),
            }
        }

    RETURN_TYPES = (AlwaysEqualProxy("*"),)

    RETURN_NAMES = ('?',)

    FUNCTION = "return_based_on_bool"

    CATEGORY = "lam"
    OUTPUT_NODE = True

    def check_lazy_status(self, ANY, IF_TRUE, IF_FALSE):
        print("测试：check_lazy_status", ANY)
        needed = []
        if ANY:
            needed.append('IF_TRUE')
        else:
            needed.append('IF_FALSE')
        return needed


    def return_based_on_bool(self, ANY, IF_TRUE, IF_FALSE):
        return {"ui": {"value": [True if ANY else False]}, "result": (IF_TRUE if ANY else IF_FALSE,)}
    
NODE_CLASS_MAPPINGS = {
    "IfInnerExecute": IfInnerExecute
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IfInnerExecute": "判断选择"
}