import json
import logging
import execution
import uuid
from comfy.cli_args import args
import threading
from typing import List, Literal, NamedTuple, Optional
import copy
import asyncio
import execution

class CustomPromptQueue(execution.PromptQueue):
    def __init__(self, server):
        super().__init__(server)
        self.put_handlers=[]

    def add_put_handler(self, handler):
        self.put_handlers.append(handler)

    def put(self, item):
        data = None
        for handler in self.put_handlers:
            try:
                data = handler(item)
            except Exception:
                logging.warning("[ERROR] An error occurred during the on_prompt_handler processing")
        if data is not None:
            return 
        super().put(item)
    
    def task_done(self, item_id, history_result,status: Optional['PromptQueue.ExecutionStatus'],**kwargs):
        print("结束拦截测试:",item_id)
        return super().task_done(item_id, history_result,status,**kwargs)
    
def get_route_keys(endKey, prompt,uniqueIds):
    keys=[]
    for k1,v1 in prompt[endKey]['inputs'].items():
        if type(v1)==list:
            if v1[0] == uniqueIds:
                continue
            keys.append(v1[0])
            keys.extend(get_route_keys(v1[0],prompt,uniqueIds))
    return keys
def section_handle(json_data):
    if 'prompt' not in json_data:
        return json_data
    prompt=json_data['prompt']
    sectionNodeKeys=[x for x in prompt.keys() if 'class_type' in prompt[x] and prompt[x]['class_type']=='SectionEnd']
    for endNum in sectionNodeKeys:
        startNum=prompt[endNum]['inputs']['section'][0]
        server=prompt[startNum]['inputs']['server']
        if server=='default':
            continue
        if 'sectype' in prompt[startNum]['inputs'] and prompt[startNum]['inputs']['sectype']==1:
            continue

        childPrompt={}
        selAllNum=get_route_keys(endNum,prompt,startNum)
        if len(selAllNum)==0:
            prompt[startNum]['inputs']['server']='default'
            continue
        selAllNum=list(set(selAllNum))
        for selNum in selAllNum:
            childPrompt[selNum]=prompt[selNum]
            prompt.pop(selNum, None)
        childPrompt[startNum]=copy.deepcopy(prompt[startNum])
        childPrompt[endNum]=copy.deepcopy(prompt[endNum])
        prompt[startNum]['inputs']['data']=json.dumps({'prompt':childPrompt,'client_id':json_data['client_id']})
        prompt[endNum]['inputs']['images']=[startNum,1]
    return json_data

def run_async_in_thread(coro):
    """在新线程中运行异步代码"""
    result = None
    event = threading.Event()

    def run():
        nonlocal result
        try:
            result = asyncio.run(coro)
        except Exception as e:
            result = {"error": str(e)}
        finally:
            event.set()

    thread = threading.Thread(target=run)
    thread.start()
    event.wait()
    return result
def prompt(self,json_data):
    json_data=section_handle(json_data)
    try:
        json_data = self.trigger_on_prompt(json_data)
        if "number" in json_data:
            number = float(json_data['number'])
        else:
            number = self.number
            if "front" in json_data:
                if json_data['front']:
                    number = -number

            self.number += 1
        if "prompt" in json_data:
            prompt = json_data["prompt"]
            prompt_id = str(json_data.get("prompt_id", uuid.uuid4()))

            partial_execution_targets = None
            if "partial_execution_targets" in json_data:
                partial_execution_targets = json_data["partial_execution_targets"]

            valid = run_async_in_thread(execution.validate_prompt(prompt_id, prompt, partial_execution_targets))
            extra_data = {}
            if "extra_data" in json_data:
                extra_data = json_data["extra_data"]

            if "client_id" in json_data:
                extra_data["client_id"] = json_data["client_id"]
            if valid[0]:
                outputs_to_execute = valid[2]
                sensitive = {}
                for sensitive_val in execution.SENSITIVE_EXTRA_DATA_KEYS:
                    if sensitive_val in extra_data:
                        sensitive[sensitive_val] = extra_data.pop(sensitive_val)
                self.prompt_queue.put((number, prompt_id, prompt, extra_data, outputs_to_execute,sensitive))
                response = {"prompt_id": prompt_id, "number": number, "node_errors": valid[3]}
                return response
            else:
                logging.warning("invalid prompt: {}".format(valid[1]))
                return {"error": valid[1], "node_errors": valid[3]}
        else:
            error = {
                "type": "no_prompt",
                "message": "No prompt provided",
                "details": "No prompt provided",
                "extra_info": {}
            }
            return {"error": error, "node_errors": []}
    except Exception as e:
        print('prompt处理异常',e)
        return {"error": "prompt处理异常",'node_errors':[]}