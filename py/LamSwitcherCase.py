from .src.utils.uitls import AlwaysEqualProxy,AlwaysTupleZero
class LamSwitcherCase:
    """
    内判断选择
    """
    DESCRIPTION = """
    根据switcher值选择执行那个case流 switcher=0-19
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

    RETURN_TYPES = AlwaysTupleZero(AlwaysEqualProxy("*"),)

    RETURN_NAMES = ('?',)

    FUNCTION = "return_based_on_bool"

    CATEGORY = "lam"
    OUTPUT_NODE = False

    def check_lazy_status(self, switcher, case0, case1, **kwargs):
        needed = []
        caseNames=['case0','case1']
        for key in kwargs.keys():
            caseNames.append(key)
        if isinstance(switcher, int) or isinstance(switcher, str):
            if ('case'+str(switcher)) in caseNames:
                needed.append('case'+str(switcher))
        elif isinstance(switcher, list):
            for i in switcher:
                if ('case'+str(i)) in caseNames:
                    needed.append('case'+str(i))
        else:
            raise Exception("Invalid input type for 'switcher'")

        return needed


    def return_based_on_bool(self,switcher, case0, case1, **kwargs):
        cases={'case0':case0,'case1':case1}
        for key in kwargs.keys():
            cases[key]=kwargs[key]
        result=None
        if isinstance(switcher, int) or isinstance(switcher, str):
            if ('case'+str(switcher)) in cases:
                result=cases['case'+str(switcher)]
            return {"ui": {"value": [switcher]}, "result": (result,)}
        elif isinstance(switcher, list):
            result=[]
            for i in switcher:
                if ('case'+str(i)) in cases:
                    result.append(cases['case'+str(i)])
            return {"ui": {"value": [switcher]}, "result": tuple(result)}
        else:
            raise Exception("Invalid input type for 'switcher'")
    
NODE_CLASS_MAPPINGS = {
    "LamSwitcherCase": LamSwitcherCase
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamSwitcherCase": "条件选择器"
}