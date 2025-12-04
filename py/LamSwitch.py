from .src.utils.uitls import AlwaysEqualProxy

class LamSwitchStart:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base": (AlwaysEqualProxy("*"),),
            },
            "hidden": {
                "switchs": "STRING",  #隐藏参数
            }
        }
    RETURN_TYPES = (AlwaysEqualProxy("*"),)

    RETURN_NAMES = ('base',)

    FUNCTION = "switch_start"

    OUTPUT_NODE = False

    CATEGORY = "lam"

    def switch_start(self,base,switchs=''):
        return (base,)
    
class LamSwitchMiddle:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base": (AlwaysEqualProxy("*"),),
                "new": (AlwaysEqualProxy("*"),{"lazy":True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",           #节点编号
                "prompt": "PROMPT",                 #流程节点信息
            }
        }
    RETURN_TYPES = (AlwaysEqualProxy("*"),)

    RETURN_NAMES = ('base',)

    FUNCTION = "switch_middle"

    OUTPUT_NODE = False

    CATEGORY = "lam"

    def check_lazy_status(self,base,new,unique_id,prompt):
        needed = []
        start_id = prompt[unique_id]['inputs']['base'][0]
        index = 0 
        while prompt[start_id]['class_type']!='LamSwitchStart':
            start_id=prompt[start_id]['inputs']['base'][0]
            index+=1
        switchsStr = prompt[start_id]['inputs']['switchs']
        switchs = switchsStr.split(',')
        if switchs[index]=='1':
            needed.append('new')
        return needed

    def switch_middle(self,base,new,unique_id,prompt):
        start_id = prompt[unique_id]['inputs']['base'][0]
        index = 0 
        while prompt[start_id]['class_type']!='LamSwitchStart':
            start_id=prompt[start_id]['inputs']['base'][0]
            index+=1
        switchsStr = prompt[start_id]['inputs']['switchs']
        switchs = switchsStr.split(',')
        if switchs[index]=='1':
            return (new,)
        else:
            return (base,)

NODE_CLASS_MAPPINGS = {
    "LamSwitchStart": LamSwitchStart,
    "LamSwitchMiddle":LamSwitchMiddle
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamSwitchStart": "开关控制",
    "LamSwitchMiddle": "开关分段"
}
