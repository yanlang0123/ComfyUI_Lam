from .src.utils.uitls import AlwaysEqualProxy,AlwaysTupleZero
import json
from comfy_execution.graph_utils import GraphBuilder
import nodes
import folder_paths
import os

def is_link(obj):
    if not isinstance(obj, list):
        return False
    if len(obj) != 2:
        return False
    if not isinstance(obj[0], str):
        return False
    if not isinstance(obj[1], int) and not isinstance(obj[1], float) and not isinstance(obj[1], str):
        return False
    return True

# 子工作流参数
class ChildWorkflowParameters:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            
        }

    RETURN_TYPES = ()

    RETURN_NAMES = ()

    OUTPUT_NODE = False

    CATEGORY = "lam"

# 子工作流节点组
class ChildWorkflowNodes:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = os.path.join(folder_paths.base_path, 'user','default','workflows')
        if not os.path.exists(input_dir):
            os .makedirs(input_dir)
        #获取全部JSON文件
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and f.endswith('.json')]
        return {
                "required":
                    {
                        "workflowFile": (files, ), 
                    },"hidden": {
                        "childJson": ("STRING", {"default": ""}),
                        "kwargsObj": ("OBJECT", {"default": {}}),
                        "unique_id": "UNIQUE_ID",           #节点编号
                        "prompt": "PROMPT",   #流程节点信息
                        "extra_pnginfo": "EXTRA_PNGINFO"    #前端流程图信息
                    }
            }

    RETURN_TYPES = AlwaysTupleZero(AlwaysEqualProxy("*"),)
    
    FUNCTION = "hidden_nodes"
    
    OUTPUT_NODE = False
    
    CATEGORY = "lam"

    def hidden_nodes(self,workflowFile,childJson='',kwargsObj={},unique_id='',prompt={},extra_pnginfo={},**kwargs):
        try: 
            if childJson=="":
                childJson=[node['properties']['childJson'] for node in extra_pnginfo['workflow']['nodes'] if int(node['id'])==int(unique_id)][0]
                
            for ikey in prompt[unique_id]['inputs'].keys():
                if not is_link(prompt[unique_id]['inputs'][ikey]):
                    kwargs[ikey]=prompt[unique_id]['inputs'][ikey]
                    
            nnoutput=json.loads(childJson)
            idDNode={}
            graph = GraphBuilder()
            def get_node_result(nodeData,id):
                inputKeys=[nodeData['inputs'][ikey][0] for ikey in  list(nodeData['inputs'].keys()) if is_link(nodeData['inputs'][ikey]) and 'hidden' != nodeData['inputs'][ikey][0] and nodeData['inputs'][ikey][0] not in idDNode]
                for ikey in inputKeys:
                    if ikey not in nnoutput:
                        continue
                    node=get_node_result(nnoutput[ikey],ikey)
                    idDNode[ikey]=node
                inputs=nodeData['inputs']
                newInputs={}
                for ikey in inputs.keys():
                    if is_link(inputs[ikey]):
                        if inputs[ikey][0]=='hidden':
                            if inputs[ikey][1] in kwargs:
                                newInputs[ikey]=kwargs[inputs[ikey][1]]
                            elif inputs[ikey][1] in kwargsObj:
                                newInputs[ikey]=kwargsObj[inputs[ikey][1]]
                        elif inputs[ikey][0] in idDNode:
                            newInputs[ikey]=idDNode[inputs[ikey][0]].out(inputs[ikey][1])
                    else:
                        newInputs[ikey]=inputs[ikey]
                if 'ChildWorkflowNodes' == nodeData['class_type']:
                    return graph.node(nodeData['class_type'],id,kwargsObj=newInputs,**newInputs)
                return graph.node(nodeData['class_type'],id,**newInputs)
            values = [value for key in nnoutput.keys() if 'outputs' in nnoutput[key] for value in nnoutput[key]['outputs']]
            for key in nnoutput.keys(): 
                nodeData=nnoutput[key]
                if 'outputs' not in nodeData: 
                    continue
                if len(nodeData['outputs'])>0:
                    node=get_node_result(nodeData,key)
                for i in nodeData['outputs']:
                    values[i[0]]=node.out(i[1])

            return {
                    "result": tuple(values),
                    "expand": graph.finalize(),
                }
        except Exception as e:
            raise SyntaxError(f"子工作流（{workflowFile}）执行异常：{e}")
        
    

NODE_CLASS_MAPPINGS = { 
    "ChildWorkflowParameters": ChildWorkflowParameters,
    "ChildWorkflowNodes": ChildWorkflowNodes,
}

NODE_DISPLAY_NAME_MAPPINGS = { 
    "ChildWorkflowParameters": "子工作流参数",
    "ChildWorkflowNodes": "子工作流节点组",
}