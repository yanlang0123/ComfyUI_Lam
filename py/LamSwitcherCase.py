from .src.utils.uitls import AlwaysEqualProxy
class LamSwitcherCase:
    """
    内判断选择
    """
    DESCRIPTION = """
    
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "switcher": (AlwaysEqualProxy("*"),),
                "case0": (AlwaysEqualProxy("*"),{"lazy":True}),
                "case1": (AlwaysEqualProxy("*"),{"lazy":True}),
            },"hidden": {
                f"case{i}": (AlwaysEqualProxy("*"),{"lazy":True}) for i in range(2, 20)
            }
        }

    RETURN_TYPES = (AlwaysEqualProxy("*"),)

    RETURN_NAMES = ('?',)

    FUNCTION = "return_based_on_bool"

    CATEGORY = "lam"
    OUTPUT_NODE = False

    def check_lazy_status(self, switcher, case0, case1, **kwargs):
        needed = []
        caseNames=['case0','case1']
        for key in kwargs.keys():
            caseNames.append(key)
        if ('case'+str(switcher)) in caseNames:
            needed.append('case'+str(switcher))

        return needed


    def return_based_on_bool(self,switcher, case0, case1, **kwargs):
        cases={'case0':case0,'case1':case1}
        for key in kwargs.keys():
            cases[key]=kwargs[key]
        result=None
        if ('case'+str(switcher)) in cases:
            result=cases['case'+str(switcher)]
        return {"ui": {"value": [switcher]}, "result": (result,)}
    
NODE_CLASS_MAPPINGS = {
    "LamSwitcherCase": LamSwitcherCase
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamSwitcherCase": "条件选择器"
}