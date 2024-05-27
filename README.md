# ComfyUI_Lam

### 介绍
基于comfyUI开发的插件

#### 使用说明
下载放到comfyUI的插件目录，如下:

![Alt text](解压存放路径及名称.png)

##### 特别说明该版本执行最新版“ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z” 里面带cu121的版本地址如下：
https://github.com/comfyanonymous/ComfyUI/releases/download/latest/ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z

然后运行install.bat文件，未报错后就可以了，

1. 模型地址，及存放路径：
lama模型：
https://huggingface.co/lllyasviel/Annotators/resolve/main/ControlNetLama.pth  ..\ComfyUI\models\lama\ControlNetLama.pth
SadTalker模型：
https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar ..\ComfyUI\models\SadTalker\mapping_00109-model.pth.tar
https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar ..\ComfyUI\models\SadTalker\mapping_00229-model.pth.tar
https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors ..\ComfyUI\models\SadTalker\SadTalker_V0.0.2_256.safetensors
https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors ..\ComfyUI\models\SadTalker\SadTalker_V0.0.2_512.safetensors


2. image-face-fusion模型换脸模型
链接：https://pan.baidu.com/s/19DOgJQ_RHNAjfNrzSr2uTQ?pwd=gf0p 
提取码：gf0p
解压到 ..\ComfyUI\models\image-face-fusion 目录


3. 修改comfyUI根目录下的execution.py文件，修改内容，

搜索 “def recursive_execute” 
位置参考图如下：
![Alt text](修改位置.png)
新增内容：
```python
#循环添加代码----------开始----------
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
```
```python
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

    #循环添加代码-----------结束---------
```
```python
                #循环添加代码----------开始----------
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
```
```python
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
            #判断选择添加代码-----------结束---------
```
```python
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
        #循环添加代码-----------结束---------
```
搜索 “def validate_prompt
```python
'''优化输出开始'''
    inputKeys=[]
    for k,v in prompt.items():
        for k1,v1 in v['inputs'].items():
            if type(v1)==list and len(v1)==2:
                inputKeys.append(v1[0])
    for x in prompt:
        class_ = nodes.NODE_CLASS_MAPPINGS[prompt[x]['class_type']]
        if hasattr(class_, 'OUTPUT_NODE') and class_.OUTPUT_NODE == True and x not in inputKeys:
            outputs.add(x)
    '''优化输出结束'''
``` 
