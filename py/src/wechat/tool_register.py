import inspect
import traceback
from copy import deepcopy
from pprint import pformat
from types import GenericAlias
from typing import get_origin, Annotated
import json
import requests
import random
import time
import asyncio
import os
import re

_TOOL_HOOKS = {}
_TOOL_DESCRIPTIONS = {}
_TOOL_QW_DESCRIPTIONS = []
_TOOL_OP_DESCRIPTIONS = []
_TOOL_LM4_DESCRIPTIONS = []


def nested_object_to_dict(obj):
    if isinstance(obj, list):
        return [nested_object_to_dict(x) for x in obj]
    if isinstance(obj, dict):
        return {k: nested_object_to_dict(v) for k, v in obj.items()}
    if obj and type(obj) not in (int, float, str):
        return nested_object_to_dict(vars(obj))
    else:
        return obj


def register_tool(func: callable):
    tool_name = func.__name__
    tool_description = inspect.getdoc(func).strip()
    python_params = inspect.signature(func).parameters
    tool_params = []
    opai_params = {}
    params_required = []
    otye = {"str": 'string', "int": 'number', "dict": 'object',
            "list": 'array', "bool": 'boolean', "None": 'null'}

    for name, param in python_params.items():
        annotation = param.annotation
        if annotation is inspect.Parameter.empty:
            # raise TypeError(f"Parameter `{name}` missing type annotation")
            continue
        if get_origin(annotation) != Annotated:
            raise TypeError(
                f"Annotation type for `{name}` must be typing.Annotated")

        typ, (description, required) = annotation.__origin__, annotation.__metadata__
        typ: str = str(typ) if isinstance(typ, GenericAlias) else typ.__name__
        if not isinstance(description, str):
            raise TypeError(f"Description for `{name}` must be a string")
        if not isinstance(required, bool):
            raise TypeError(f"Required for `{name}` must be a bool")

        tool_params.append({
            "name": name,
            "description": description,
            "type": typ,
            "required": required
        })
        ntype = otye[str(typ)] if typ in otye else typ
        opai_params[name] = {
            "type": ntype,
            "description": description,
        }
        if required:
            params_required.append(name)
    tool_def = {
        "name": tool_name,
        "description": tool_description,
        "name_for_human": tool_description,
        "description_for_model": tool_description + " Format the arguments as a JSON object.",
        "params": tool_params,
        "parameters": tool_params
    }
    opai_tool_def = {
        "name": tool_name,
        "description": tool_description,
        "params": tool_params,
        "parameters": {"type": 'object', "properties": opai_params}
    }

    glm4_tool_def = {
        "type": "function",
        "function": {
            "name": tool_name,
            "description": tool_description,
            "params": tool_params,
            "parameters": {"type": 'object', "properties": opai_params,"required":params_required}
        }
    }

    # print("[registered tool] " + pformat(tool_def))
    _TOOL_HOOKS[tool_name] = func
    _TOOL_DESCRIPTIONS[tool_name] = tool_def
    _TOOL_QW_DESCRIPTIONS.append(tool_def)
    _TOOL_OP_DESCRIPTIONS.append(opai_tool_def)
    _TOOL_LM4_DESCRIPTIONS.append(glm4_tool_def)

    return func


def dispatch_tool(tool_name: str, tool_params: dict) -> str:
    if tool_name not in _TOOL_HOOKS:
        return f"Tool `{tool_name}` not found. Please use a provided tool."
    tool_call = _TOOL_HOOKS[tool_name]
    try:
        if len(tool_params) > 0:
            ret = tool_call(**tool_params)
        else:
            ret = tool_call()

    except:
        ret = traceback.format_exc()
    return ret


def get_lm4_tools() -> list:
    return deepcopy(_TOOL_LM4_DESCRIPTIONS)


# Tool Definitions

# @register_tool
# def random_number_generator(
#         seed: Annotated[int, 'The random seed used by the generator', True],
#         range: Annotated[tuple[int, int], 'The range of the generated numbers', True],
# ) -> int:
#     """
#     Generates a random number x, s.t. range[0] <= x < range[1]
#     """
#     if not isinstance(seed, int):
#         raise TypeError("Seed must be an integer")
#     if not isinstance(range, tuple) and not isinstance(range, list):
#         raise TypeError("Range must be a tuple")
#     if not isinstance(range[0], int) or not isinstance(range[1], int):
#         raise TypeError("Range must be a tuple of integers")

#     import random
#     return random.Random(seed).randint(*range)


@register_tool
def resetting_chat_record() -> dict:
    '''重置聊对话'''
    answer = {"success": True, "res": "重置成功", "res_type": "text"}
    return answer


@register_tool
def generate_image(prompt: Annotated[str, '要生成图片的英文提示词', True]) -> dict:
    '''
    生成图片`prompt`英文提示词
    '''
    answer = {"success": True, "res": "[Image]", "res_type": "image"}
    return answer
