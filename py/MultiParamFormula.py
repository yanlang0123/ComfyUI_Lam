from .src.utils.uitls import AlwaysEqualProxy,AlwaysTupleZero
class MultiParamFormula:

    DESCRIPTION = """
    输入参数：p0,p1,p2... 支持任意类型，可根据需要输入和选择输入参数
    输出参数：p0,p1,p2... 支持任意类型，可根据需要输出
    表达式：python的正确代码语法，多个参数输出需如下形式：tuple([p0,p1,p2,p3]) 对应出参：p0,p1,p2,p3
    示例：
    入参：p0,p1 表达式：p0>p1  出参：p0 比较大小返回bool类型用于判断选节点
    入参：p0,p1 (p0类型IMAGE,p1类型INT) 表达式：p0[p1:p1+1]  出参：p0 返回指定下标的图片
    入参：p0  (p0数组)  表达式：len(p0)  出参：p0 数组长度
    入参：p0,p1 (p0类型LIST,p1类型INT) 表达式：p0[p1]  出参：p0 返回指定下标的元素
    入参：p0 (p0类型字符串数组) 表达式：','.join(p0)  出参：p0 返回字符串数组‘,’分割合并的字符串
    入参：p0 表达式：print('调试输出',p0)  出参：无 用于调试输出，查看数据结构
    """
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