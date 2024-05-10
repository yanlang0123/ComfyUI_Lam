from server import PromptServer
from aiohttp import web
import json
import os
import yaml


class LamAllInOne:
    """
    提示词选择工具
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "negative": ("STRING", {"multiline": True, "default": ""}),
            },
            "hidden": {"unique_id": "UNIQUE_ID","wprompt":"PROMPT"},
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("提示词","反向词",)

    FUNCTION = "all_in_one_prompt"

    #OUTPUT_NODE = False

    CATEGORY = "lam"

    def all_in_one_prompt(self,prompt,negative):
        
        return (prompt,negative,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "LamAllInOne": LamAllInOne
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "LamAllInOne": "提示词工具"
}
