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
	"name": "execution.py",
	"isEditStr":"def get_del_keys(key, prompt,uniqueIds)",
	"changs":[
		{
			"primit":'''def recursive_execute''',
			"edit":'''#循环添加代码----------开始----------
def get_del_keys(key, prompt,uniqueIds):
    keys=[]
    for k,v in prompt.items():
        if k in uniqueIds :
            continue
        for k1,v1 in v['inputs'].items():
            if type(v1)==list and v1[0]==key:
                keys.append(k)
                keys=keys+get_del_keys(k,prompt,uniqueIds)
    return keys
#循环添加代码-----------结束---------
def recursive_execute'''
		},{
			"primit":'''class_def = nodes.NODE_CLASS_MAPPINGS[class_type]
    if unique_id in outputs:
        return (True, None, None)''',
			"edit":'''class_def = nodes.NODE_CLASS_MAPPINGS[class_type]
    if unique_id in outputs:
        return (True, None, None)

    #循环添加代码----------开始----------
    startNum=None
    startData={}
    delKeys=[]
    backhaul={}
    clTypes=['ForInnerEnd','IfInnerExecute','DoWhileEnd']
    oldPrompt=None
    if class_type in clTypes:
        oldPrompt=copy.deepcopy(prompt)

    if class_type=='ForInnerEnd':
        startNum=prompt[unique_id]['inputs']['total'][0]
        inputNum=prompt[unique_id]['inputs']['obj'][0]
        maxKeyStr=sorted(list(prompt.keys()), key=lambda x: int(x.split(':')[0]))[-1]
        maxKey = int(maxKeyStr.split(':')[0])
        delKeys=list(set(get_del_keys(startNum,prompt,[startNum,unique_id]))) 
        delKeys.append(startNum)
        delKeys = list(filter(lambda x: x != inputNum, delKeys))
        for key in delKeys:
            outputs.pop(key, None)
        
        startInput=prompt[startNum]['inputs']
        if isinstance(startInput['total'],list) or isinstance(startInput['stop'],list) or isinstance(startInput['i'],list):
            result = recursive_execute(server, prompt, outputs, startNum, extra_data, executed, prompt_id, outputs_ui, object_storage)
            if result[0] is not True:
                    return result
            
        for x in startInput:
            input_data = startInput[x]
            if isinstance(input_data, list):
                startData[x]=outputs[input_data[0]][input_data[1]][0]
            else:
                startData[x]=input_data

        for i in range(startData['i']+1,startData['total'],startData['stop']):
            prompt[str(maxKey+i)]=prompt[inputNum]
            prompt[unique_id]['inputs']['obj'+str(i)]=[str(maxKey+i),prompt[unique_id]['inputs']['obj'][-1]]
            if i==startInput['i']+1:
                backhaul['obj'+str(i)]=prompt[unique_id]['inputs']['obj']
            else:
                backhaul['obj'+str(i)]=[str(maxKey+i-startInput['stop']),prompt[unique_id]['inputs']['obj'][-1]]
    elif class_type=='DoWhileEnd':
        startNum=prompt[unique_id]['inputs']['start'][0]
        inputNum=prompt[unique_id]['inputs']['ANY'][0]
        delKeys=list(set(get_del_keys(startNum,prompt,[startNum,unique_id]))) 
        delKeys.append(startNum)
        delKeys.append(inputNum)

    #循环添加代码-----------结束---------'''
		}
		,{
			"primit":'''result = recursive_execute(server, prompt, outputs, input_unique_id, extra_data, executed, prompt_id, outputs_ui, object_storage)
                if result[0] is not True:
                    # Another node failed further upstream
                    return result''',
			"edit":'''#循环添加代码----------开始----------
                if class_type=='ForInnerEnd' and x !='obj' and x.startswith('obj'):
                    if startNum!=None:
                        if isinstance(prompt[startNum]['inputs']['i'],list):
                            prompt[startNum]['inputs']['i']=startData['i']+startData['stop']
                        else:
                            prompt[startNum]['inputs']['i']=prompt[startNum]['inputs']['i']+startData['stop']
                        prompt[startNum]['inputs']['obj']=backhaul[x]
                        for key in delKeys:
                            outputs.pop(key, None)
                #循环添加代码-----------结束---------
                result = recursive_execute(server, prompt, outputs, input_unique_id, extra_data, executed, prompt_id, outputs_ui, object_storage)
                if result[0] is not True:
                    # Another node failed further upstream
                    return result
                
                #判断选择添加代码-----------开始---------
                if class_type=='DoWhileEnd' and x == 'ANY':
                    any=outputs[inputNum][prompt[unique_id]['inputs']['ANY'][1]][0]
                    i=0
                    while any:
                        for key in delKeys:
                            outputs.pop(key, None)
                        i=i+1
                        outputs['i']=[[i]]
                        prompt[startNum]['inputs']['i']=['i',0]
                        result = recursive_execute(server, prompt, outputs, input_unique_id, extra_data, executed, prompt_id, outputs_ui, object_storage)
                        if result[0] is not True:
                            return result
                        any=outputs[inputNum][prompt[unique_id]['inputs']['ANY'][1]][0]
            
            if class_type=='IfInnerExecute' and x=='ANY':
                if outputs[input_unique_id][output_index][0]:
                    inputs['IF_FALSE']=oldPrompt[unique_id]['inputs']['IF_TRUE']
                else:
                    inputs['IF_TRUE']=oldPrompt[unique_id]['inputs']['IF_FALSE']
            #判断选择添加代码-----------结束---------'''
		}
		,{
			"primit":'''output_data, output_ui = get_output_data(obj, input_data_all)
        outputs[unique_id] = output_data''',
			"edit":'''output_data, output_ui = get_output_data(obj, input_data_all)
        outputs[unique_id] = output_data
        #循环添加代码----------开始----------
        if class_type=='ForInnerEnd' or class_type=='DoWhileEnd':
            prompt[startNum]['inputs']=oldPrompt[startNum]['inputs']
            prompt[unique_id]['inputs']=oldPrompt[unique_id]['inputs']
            outputs.pop(startNum, None)
            result = recursive_execute(server, prompt, outputs, startNum, extra_data, executed, prompt_id, outputs_ui, object_storage)
            if result[0] is not True:
                   return result
        if class_type=='IfInnerExecute':
            prompt[unique_id]['inputs']=oldPrompt[unique_id]['inputs']
        #循环添加代码-----------结束---------'''
		}
		,{
			"primit":'''def validate_prompt(prompt):
    outputs = set()''',
			"edit":'''def validate_prompt(prompt):
    outputs = set()
    inputKeys=[]
    for k,v in prompt.items():
        for k1,v1 in v['inputs'].items():
            if type(v1)==list and len(v1)==2:
                inputKeys.append(v1[0])'''
		}
		,{
			"primit":'''if hasattr(class_, 'OUTPUT_NODE') and class_.OUTPUT_NODE is True:''',
			"edit":'''if hasattr(class_, 'OUTPUT_NODE') and class_.OUTPUT_NODE is True and x not in inputKeys: #添加and x not in inputKeys'''
		}
	]
}
]
filePath=os.path.dirname(__file__)
base_path=filePath.split('custom_nodes')[0]
backupPath=os.path.join(filePath,'backup')
def read_py_file(file_path):
	with open(file_path, 'r',encoding='utf-8') as file:
		text = file.read()
	return text

def write_py_file(file_path, text):
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

