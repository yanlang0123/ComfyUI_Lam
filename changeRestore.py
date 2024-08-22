import os,sys
#读取py文件为text字符串
editlist=[{
	"name": "server.py",
	"isEditStr":"elif 'prompt_id' in json_data:",
	"changs":[
		{
			"primit":'''else:
                return web.json_response({"error": "no prompt", "node_errors": []}, status=400)''',
			"edit":'''elif 'prompt_id' in json_data:
                return web.json_response(json_data)
            else:
                return web.json_response({"error": "no prompt", "node_errors": []}, status=400)'''
		}
	]
},{
	"name": "comfy_execution/caching.py",
	"isEditStr":"def remove_node(self, node_id):",
	"changs":[
		{
			"primit":'''class BasicCache:''',
			"edit":'''class BasicCache:
    def add_keys(self, node_ids):
        self.cache_key_set.add_keys(node_ids)

    def remove_node(self, node_id):
        cache_key = self.cache_key_set.get_data_key(node_id)
        if cache_key is None:
            return 
        if cache_key in self.cache:
            del self.cache[cache_key]
        subcache_key = self.cache_key_set.get_subcache_key(node_id)
        if subcache_key in self.subcaches:
            del self.subcaches[subcache_key]'''
		}
	]
},{
	"name": "execution.py",
	"isEditStr":"def get_del_keys(key, prompt,uniqueIds)",
	"changs":[
		{
			"primit":'''class PromptExecutor:''',
			"edit":'''#循环添加代码----------开始----------
def get_del_keys(key, prompt,uniqueIds):
    keys=[]
    for k,v in prompt.items():
        if k in uniqueIds :
            continue
        for k1,v1 in v['inputs'].items():
            if type(v1)==list and v1[0]==key:
                keys.append(k)
                keys=keys+get_del_keys(k,prompt,uniqueIds+[k])
    return keys
#循环添加代码-----------结束---------
class PromptExecutor:'''
		},{
			"primit":'''while not execution_list.is_empty():''',
			"edit":'''oldPrompt=copy.deepcopy(prompt)
            forNodes={}
            nextNodeForId={}
            oldNodeData={}
            ifAnyNodes={prompt[x]['inputs']['ANY'][0]:[x,prompt[x]['inputs']['ANY'][1]] for x in prompt.keys() if prompt[x]['class_type']=='IfInnerExecute'}
            while not execution_list.is_empty():'''
		}
		,{
			"primit":'''result, error, ex = execute''',
			"edit":'''class_type = prompt[node_id]['class_type']
                if class_type=='ForInnerEnd' and node_id not in forNodes:
                    if node_id not in oldNodeData:
                        oldNodeData[node_id]={}
                    
                    forNodes[node_id]={"backhaul":{},"newNodeIds":{},"backhaul":{},"startData":{},"delKeys":[],"startNum":None,"inputNum":None,"nextNoewId":None}
                    forNodes[node_id]['startNum']=prompt[node_id]['inputs']['total'][0]
                    forNodes[node_id]['inputNum']=prompt[node_id]['inputs']['obj'][0]
                    forNodes[node_id]['startCcacheData']=self.caches.outputs.get(forNodes[node_id]['startNum'])
                    maxKeyStr=sorted(list(prompt.keys()), key=lambda x: int(x.split(':')[0]))[-1]
                    maxKey = int(maxKeyStr.split(':')[0])
                    delKeys=list(set(get_del_keys(forNodes[node_id]['startNum'],prompt,[forNodes[node_id]['startNum'],node_id]))) 
                    delKeys.append(forNodes[node_id]['startNum'])
                    forNodes[node_id]['delKeys'] = list(filter(lambda x: x != forNodes[node_id]['inputNum'],delKeys))
                    
                    startInput=prompt[forNodes[node_id]['startNum']]['inputs']
                    for x in startInput:
                        input_data = startInput[x]
                        if isinstance(input_data, list):
                            forNodes[node_id]['startData'][x]=self.caches.outputs.get(input_data[0])[input_data[1]][0]
                        else:
                            forNodes[node_id]['startData'][x]=input_data

                    oldPi=''
                    for i in range(forNodes[node_id]['startData'] ['i']+1,forNodes[node_id]['startData'] ['total'],forNodes[node_id]['startData'] ['stop']):
                        if f'p{i}' in oldNodeData[node_id] and oldNodeData[node_id][f'p{i}'] in prompt:
                            prompt[oldNodeData[node_id][f'p{i}']]['inputs'][f'p{i}']=prompt[forNodes[node_id]['inputNum']]['inputs']['p0']
                            prompt[node_id]['inputs']['obj'+str(i)]=[oldNodeData[node_id][f'p{i}'],prompt[node_id]['inputs']['obj'][-1]]
                        else:
                            oldNodeData[node_id][f'p{i}']=str(maxKey+i)
                            prompt[str(maxKey+i)]=copy.deepcopy(prompt[forNodes[node_id]['inputNum']])
                            prompt[str(maxKey+i)]['inputs']['expression']=f'p{i}'
                            prompt[str(maxKey+i)]['inputs'][f'p{i}']=prompt[forNodes[node_id]['inputNum']]['inputs']['p0']
                            prompt[str(maxKey+i)]['inputs'].pop('p0',None)
                            prompt[node_id]['inputs']['obj'+str(i)]=[str(maxKey+i),prompt[node_id]['inputs']['obj'][-1]]

                        if i==forNodes[node_id]['startData']['i']+1:
                            forNodes[node_id]['backhaul']['obj'+oldNodeData[node_id][f'p{i}']]=prompt[node_id]['inputs']['obj']
                        else:
                            forNodes[node_id]['backhaul']['obj'+oldNodeData[node_id][f'p{i}']]=[oldNodeData[node_id][oldPi],prompt[node_id]['inputs']['obj'][-1]]
                        
                        forNodes[node_id]['newNodeIds'][oldNodeData[node_id][f'p{i}']]=(oldNodeData[node_id][f'p{i}'], prompt[node_id]['inputs']['obj'][-1], node_id)
                        nextNodeForId[oldNodeData[node_id][f'p{i}']]=node_id
                        oldPi=f'p{i}'
                    
                    if len(forNodes[node_id]['newNodeIds'].keys())>0:
                        nnfids=list(nextNodeForId.items())
                        nnfids=[x for x in nnfids if x[1]==node_id]
                        i=len(nnfids)-len(forNodes[node_id]['newNodeIds'].keys())+1
                        endSize=','.join([str(x) for x in range(max(1,i-10),i+1)]) 
                        if self.server.client_id is not None:
                            self.server.send_sync("executed", {"output":{"value": [endSize]},"node":node_id,"prompt_id":''},self.server.client_id)
                            self.server.send_sync("executing", { "node": node_id, "display_node": node_id, "prompt_id": prompt_id }, self.server.client_id)
                    
                        for cache in self.caches.all:
                            cache.add_keys(list(forNodes[node_id]['newNodeIds'].keys()))
                        from_node_id, from_socket, to_node_i=forNodes[node_id]['newNodeIds'][list(forNodes[node_id]['newNodeIds'].keys())[0]]
                        self.caches.outputs.remove_node(from_node_id)
                        for key in forNodes[node_id]['delKeys']:
                            if key not in list(forNodes[node_id]['newNodeIds'].keys()):
                                self.caches.outputs.remove_node(key)
                        
                        if isinstance(prompt[forNodes[node_id]['startNum']]['inputs']['i'],list):
                            prompt[forNodes[node_id]['startNum']]['inputs']['i']=forNodes[node_id]['startData'] ['i']+forNodes[node_id]['startData'] ['stop']
                        else:
                            prompt[forNodes[node_id]['startNum']]['inputs']['i']=prompt[forNodes[node_id]['startNum']]['inputs']['i']+forNodes[node_id]['startData'] ['stop']
                        prompt[forNodes[node_id]['startNum']]['inputs']['obj']=forNodes[node_id]['backhaul']['obj'+from_node_id]
                        execution_list.add_strong_link(from_node_id, from_socket, to_node_i)
                        forNodes[node_id]['newNodeIds'].pop(from_node_id, None)
                        forNodes[node_id]['nextNoewId']=from_node_id

                        execution_list.unstage_node_execution()
                        node_id, error, ex = execution_list.stage_node_execution()
                        if error is not None:
                            self.handle_execution_error(prompt_id, dynamic_prompt.original_prompt, current_outputs, executed, error, ex)
                            break
                        class_type = prompt[node_id]['class_type']

                elif  class_type=='DoWhileEnd':
                    startNum=prompt[node_id]['inputs']['start'][0]
                    inputNum,inputSocket=prompt[node_id]['inputs']['ANY']
                    anyVal=self.caches.outputs.get(inputNum)
                    if anyVal and anyVal[inputSocket][0]:
                        vals=self.caches.outputs.get(startNum)
                        i=0
                        if vals:
                            i=int(vals[2][0])
                        i=i+1
                        endSize=','.join([str(x) for x in range(max(1,i-10),i+1)])
                        if self.server.client_id is not None:
                            self.server.send_sync("executed", {"output":{"value": [endSize]},"node":node_id,"prompt_id":''},self.server.client_id)
                            self.server.send_sync("executing", { "node": node_id, "display_node": node_id, "prompt_id": prompt_id }, self.server.client_id)
                         
                        iNum=prompt[startNum]['inputs']['i'][0]
                        prompt[iNum]['inputs']['expression']=str(i)
                        from_node_id, from_socket=prompt[node_id]['inputs']['obj']
                        delKeys=list(set(get_del_keys(startNum,prompt,[startNum,node_id]))) 
                        delKeys.append(startNum)
                        delKeys.append(inputNum)
                        delKeys.append(from_node_id)
                        delKeys.append(iNum)
                        for key in delKeys:
                            self.caches.outputs.remove_node(key)
                        execution_list.add_strong_link(from_node_id, from_socket, node_id)
                        execution_list.unstage_node_execution()
                        node_id, error, ex = execution_list.stage_node_execution()
                        if error is not None:
                            self.handle_execution_error(prompt_id, dynamic_prompt.original_prompt, current_outputs, executed, error, ex)
                            break
                        class_type = prompt[node_id]['class_type']

                result, error, ex = execute'''
		}
		,{
			"primit":'''execution_list.complete_node_execution()''',
			"edit":'''execution_list.complete_node_execution()
                    
                    if node_id in nextNodeForId and forNodes[nextNodeForId[node_id]]['nextNoewId']==node_id and  len(forNodes[nextNodeForId[node_id]]['newNodeIds'].keys())>0:
                        forNodeId=nextNodeForId[node_id]
                        nnfids=list(nextNodeForId.items())
                        nnfids=[x for x in nnfids if x[1]==forNodeId]
                        i=len(nnfids)-len(forNodes[forNodeId]['newNodeIds'].keys())+1
                        endSize=','.join([str(x) for x in range(max(1,i-10),i+1)]) 
                        if self.server.client_id is not None:
                            self.server.send_sync("executed", {"output":{"value": [endSize]},"node":forNodeId,"prompt_id":''},self.server.client_id)
                            self.server.send_sync("executing", { "node": forNodeId, "display_node": forNodeId, "prompt_id": prompt_id }, self.server.client_id)
                    
                        from_node_id, from_socket, to_node_i=forNodes[forNodeId]['newNodeIds'][list(forNodes[forNodeId]['newNodeIds'].keys())[0]]
                        self.caches.outputs.remove_node(from_node_id)
                        for key in forNodes[forNodeId]['delKeys']:
                            if key not in list(forNodes[forNodeId]['newNodeIds'].keys()):
                                self.caches.outputs.remove_node(key)
                        if isinstance(prompt[forNodes[forNodeId]['startNum']]['inputs']['i'],list):
                            prompt[forNodes[forNodeId]['startNum']]['inputs']['i']=forNodes[forNodeId]['startData']['i']+forNodes[forNodeId]['startData']['stop']
                        else:
                            prompt[forNodes[forNodeId]['startNum']]['inputs']['i']=prompt[forNodes[forNodeId]['startNum']]['inputs']['i']+forNodes[forNodeId]['startData']['stop']
                        prompt[forNodes[forNodeId]['startNum']]['inputs']['obj']=forNodes[forNodeId]['backhaul']['obj'+from_node_id]
                        execution_list.add_strong_link(from_node_id, from_socket, to_node_i)
                        forNodes[forNodeId]['newNodeIds'].pop(from_node_id, None)
                        forNodes[forNodeId]['nextNoewId']=from_node_id
                            
                    if class_type=='ForInnerEnd':
                        nnfids=list(nextNodeForId.items())
                        nnfids=[x for x in nnfids if x[1]==node_id]
                        i=len(nnfids)+1
                        endSize=','.join([str(x) for x in range(max(1,i-10),i+1)]) 
                        if self.server.client_id is not None:
                            self.server.send_sync("executed", {"output":{"value": [endSize]},"node":node_id,"prompt_id":''},self.server.client_id)
                         
                        prompt[forNodes[node_id]['startNum']]['inputs']=copy.deepcopy(oldPrompt[forNodes[node_id]['startNum']]['inputs'])
                        prompt[node_id]['inputs']=copy.deepcopy(oldPrompt[node_id]['inputs'])
                        #self.caches.outputs.set(forNodes[node_id]['startNum'], forNodes[node_id]['startCcacheData'])
                        self.caches.outputs.remove_node(forNodes[node_id]['startNum'])
                        forNodes.pop(node_id,None)
                        del_ids=[]
                        for k,v in nextNodeForId.items():
                            if v == node_id:
                                del_ids.append(k)

                        for k in del_ids:
                            nextNodeForId.pop(k,None)
                            prompt[k]['inputs'].pop(prompt[k]['inputs']['expression'],None)
                        
                    elif class_type=='DoWhileEnd':
                        startNum=prompt[node_id]['inputs']['start'][0]
                        iNum=prompt[startNum]['inputs']['i'][0]
                        prompt[iNum]['inputs']['expression']='0'
                        vals=self.caches.outputs.get(startNum)
                        i=0
                        if vals:
                            i=int(vals[2][0])
                        i=i+1
                        endSize=','.join([str(x) for x in range(max(1,i-10),i+1)]) 
                        if self.server.client_id is not None:
                            self.server.send_sync("executed", {"output":{"value": [endSize]},"node":node_id,"prompt_id":''},self.server.client_id)
                            self.server.send_sync("executing", { "node": node_id, "display_node": node_id, "prompt_id": prompt_id }, self.server.client_id)
                        self.caches.outputs.remove_node(iNum)
                        self.caches.outputs.remove_node(startNum)
                    elif node_id in ifAnyNodes:
                        data=self.caches.outputs.get(node_id)
                        ifExNodeId=ifAnyNodes[node_id][0]
                        if data and data[ifAnyNodes[node_id][-1]][0]:
                            if prompt[ifExNodeId]['inputs']['IF_FALSE'][0] in execution_list.blocking and len(execution_list.blocking[prompt[ifExNodeId]['inputs']['IF_FALSE'][0]].keys())==1:
                                if prompt[ifExNodeId]['inputs']['IF_FALSE'][0] in execution_list.pendingNodes:
                                    execution_list.pop_node(prompt[ifExNodeId]['inputs']['IF_FALSE'][0])
                        else:
                            if prompt[ifExNodeId]['inputs']['IF_TRUE'][0] in execution_list.blocking and len(execution_list.blocking[prompt[ifExNodeId]['inputs']['IF_TRUE'][0]].keys())==1:
                                if prompt[ifExNodeId]['inputs']['IF_TRUE'][0] in execution_list.pendingNodes:
                                    execution_list.pop_node(prompt[ifExNodeId]['inputs']['IF_TRUE'][0])'''
		}
	]
}
]
filePath=os.path.dirname(os.path.abspath(__file__))
print('当前目录：',filePath)
base_path=filePath.split('custom_nodes')[0]
backupPath=os.path.join(filePath,'backup')
def read_py_file(file_path):
	with open(file_path, 'r',encoding='utf-8') as file:
		text = file.read()
	return text

def write_py_file(file_path, text):
	filePath=os.path.dirname(file_path)
	if not os.path.exists(filePath):
			os.makedirs(filePath)
	with open(file_path, 'w',encoding='utf-8') as file:
		file.write(text)


if __name__ == '__main__':
	isRestore='--res' in sys.argv
	print('-------开始还原-------' if isRestore else '--------开始修改--------')
	for i in editlist:
		file_path=os.path.join(base_path,i['name'])
		if not os.path.exists(file_path):
			print(file_path+'文件不存在')
			continue
		if not os.path.exists(backupPath):
			os.makedirs(backupPath)
		
		if isRestore:
			if not os.path.exists(os.path.join(backupPath,i['name'])):
				print('备份文件'+os.path.join(backupPath,i['name'])+'不存在无法还原')
				continue
			text=read_py_file(os.path.join(backupPath,i['name']))
			write_py_file(file_path, text)
		else:
			text=read_py_file(file_path)
			if text.find(i['isEditStr'])!=-1:
				continue
			write_py_file(os.path.join(backupPath,i['name']), text)
			textOld=text+''
			for j in i['changs']:
				if text.find(j['primit'])==-1:
					print(i['name']+'未找到修改位置，修改失败')
					text=textOld
					break
				text=text.replace(j['primit'],j['edit'])
			write_py_file(file_path, text)
	print('-------还原完成-------' if isRestore else '--------修改完成--------')

