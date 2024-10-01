from PIL import Image
import numpy as np
import requests
import json
import comfy.utils
import torch
from .src.utils.uitls import AlwaysEqualProxy
from comfy_execution.graph_utils import GraphBuilder, is_link
NUM_FLOW_SOCKETS=5
class DoWhileEnd:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "start": ("DOWHILE", {"rawLink": True}),
                "ANY": (AlwaysEqualProxy("*"), ),
                "obj": (AlwaysEqualProxy("*"), ),
            },
            "hidden": {
                "stop": ("INT", {}),
                "dynprompt": "DYNPROMPT",
                "unique_id": "UNIQUE_ID",
                 **{f"initial_value{i}": ("*",{"rawLink": True}) for i in range(1, NUM_FLOW_SOCKETS)}
            }
        }
    RETURN_TYPES = ("INT",AlwaysEqualProxy("*"))
    RETURN_NAMES = ("i",'endObj')
    FUNCTION = "for_end_fun"

    CATEGORY = "lam"

    def getTaskOvers(self,nodeId):
        if nodeId.find("Recurse")!= -1:
            recId=nodeId.split('Recurse')[0]
            teskSize=nodeId.count(recId)+1
            return 'DOWHILE'+','.join([str(i+1) for i in range(max(0,teskSize-10),teskSize)])
        elif nodeId.find(".")!= -1:
            return 'DOWHILE'+'1,2'
        else:
            return 'DOWHILE'+'1'

    def for_end_fun(self,start,ANY,obj,stop=1,dynprompt=None, unique_id=None, **kwargs):
        assert dynprompt is not None
        graph = GraphBuilder()
        open_node = start[0]
        overIds=self.getTaskOvers(open_node)
        if not ANY:
            values = [[open_node,1],obj]
            for i in range(NUM_FLOW_SOCKETS):
                values.append(kwargs.get(f"initial_value{i}", None))
            return {
                'ui':{'value':[overIds]},
                "result": tuple(values),
                "expand": graph.finalize(),
            }
        
        # We want to loop
        upstream = {}
        # Get the list of all nodes between the open and close nodes
        self.explore_dependencies(unique_id, dynprompt, upstream)

        contained = {}
        self.collect_contained(open_node, upstream, contained)
        contained[unique_id] = True
        contained[open_node] = True

        # We'll use the default prefix, but to avoid having node names grow exponentially in size,
        # we'll use "Recurse" for the name of the recursively-generated copy of this node.
        for node_id in contained:
            original_node = dynprompt.get_node(node_id)
            node = graph.node(original_node["class_type"], "Recurse" if node_id == unique_id else node_id)
            node.set_override_display_id(node_id)
        for node_id in contained:
            original_node = dynprompt.get_node(node_id)
            node = graph.lookup_node("Recurse" if node_id == unique_id else node_id)
            assert node is not None
            for k, v in original_node["inputs"].items():
                if is_link(v) and v[0] in contained:
                    parent = graph.lookup_node(v[0])
                    assert parent is not None
                    node.set_input(k, parent.out(v[1]))
                else:
                    node.set_input(k, v)
        new_open = graph.lookup_node(open_node)
        assert new_open is not None
        inode = graph.node("MultiParamFormula", advanced="disable",expression="p0+p1", p0=[open_node,1], p1=stop)
        new_open.set_input('i', inode.out(0))
        new_open.set_input('obj', obj)
        for i in range(NUM_FLOW_SOCKETS):
            key = f"initial_value{i}"
            new_open.set_input(key, kwargs.get(key, None))
        my_clone = graph.lookup_node("Recurse")
        assert my_clone is not None
        result = map(lambda x: my_clone.out(x), range(NUM_FLOW_SOCKETS+2))
        return {
            'ui':{'value':[overIds]},
            "result": tuple(result),
            "expand": graph.finalize(),
        }
    
    def explore_dependencies(self, node_id, dynprompt, upstream):
        node_info = dynprompt.get_node(node_id)
        if "inputs" not in node_info:
            return
        for k, v in node_info["inputs"].items():
            if is_link(v):
                parent_id = v[0]
                if parent_id not in upstream:
                    upstream[parent_id] = []
                    self.explore_dependencies(parent_id, dynprompt, upstream)
                upstream[parent_id].append(node_id)

    def collect_contained(self, node_id, upstream, contained):
        if node_id not in upstream:
            return
        for child_id in upstream[node_id]:
            if child_id not in contained:
                contained[child_id] = True
                self.collect_contained(child_id, upstream, contained)

NODE_CLASS_MAPPINGS = {
    "DoWhileEnd": DoWhileEnd
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DoWhileEnd": "判断循环尾"
}
