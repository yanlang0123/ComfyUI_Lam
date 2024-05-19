# ComfyUI_Lam

### Introduction
A plugin developed based on comfyUI.

#### Usage Instructions
Download and place in the plugin directory of comfyUI, as shown below:

![Alt text](解压存放路径及名称.png)

##### Special Note for this version, execute the latest version "ComfyUI_windows_portable_nvidia_cu118_or_cpu.7z" with cu118 inside, the address is as follows:
https://github.com/comfyanonymous/ComfyUI/releases/download/latest/ComfyUI_windows_portable_nvidia_cu118_or_cpu.7z

1. Unzip according to the image to the specified plugin directory and name. Extract insightface.rar to the directory ..\ComfyUI_windows_portable\python_embeded\Lib\site-packages. Extract venv.rar to the directory ..\ComfyUI_windows_portable\python_embeded\Lib\site-packages. Then run the install.bat file, and if there are no errors, it's ready.

2. Model addresses and storage paths:
   Lama model:
   https://huggingface.co/lllyasviel/Annotators/resolve/main/ControlNetLama.pth  ..\ComfyUI\models\lama\ControlNetLama.pth
   SadTalker models:
   https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar ..\ComfyUI\models\SadTalker\mapping_00109-model.pth.tar
   https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar ..\ComfyUI\models\SadTalker\mapping_00229-model.pth.tar
   https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors ..\ComfyUI\models\SadTalker\SadTalker_V0.0.2_256.safetensors
   https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors ..\ComfyUI\models\SadTalker\SadTalker_V0.0.2_512.safetensors

3. Gfpgan is based on the startup directory, follow the prompts accordingly.
   https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth ..\ComfyUI_windows_portable\gfpgan\weights\alignment_WFLW_4HG.pth 
   https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth ..\ComfyUI_windows_portable\gfpgan\weights\detection_Resnet50_Final.pth 
   https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth ..\ComfyUI_windows_portable\gfpgan\weights\GFPGANv1.4.pth 
   https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth ..\ComfyUI_windows_portable\gfpgan\weights\parsing_parsenet.pth 

4. Image-face-fusion model (Face swapping model)
   Link: https://pan.baidu.com/s/19DOgJQ_RHNAjfNrzSr2uTQ?pwd=gf0p 
   Extraction Code: gf0p
   Extract to the directory ..\ComfyUI\models\image-face-fusion

5. Roop-face-swap model (Face swapping model)
   Link: https://pan.baidu.com/s/1cJeRtqgdeNW21Hljwuv-tA?pwd=b4yy 
   Extraction Code: b4yy
   Extract to the directory ..\ComfyUI\models\roop-face-swap

6. Modify the execution.py file in the comfyUI root directory. 
搜索 “def recursive_execute” 
位置参考图如下：
![Alt text](修改位置.png)
新增内容：
```python
#循环添加代码----------开始----------
def get_del_keys(key, prompt):
    keys=[]
    for k,v in prompt.items():
        if v['class_type']=='ForInnerEnd' or v['class_type']=='ForInnerStart':
            continue
        for k1,v1 in v['inputs'].items():
            if type(v1)==list and v1[0]==key:
                keys.append(k)
                keys=keys+get_del_keys(k,prompt)
    return keys
#循环添加代码-----------结束---------
```
```python
    #循环添加代码----------开始----------
    startNum=None
    startData={}
    delKeys=[]
    backhaul={}
    clTypes=['ForInnerEnd','IfInnerExecute']
    oldPrompt=None
    if class_type in clTypes:
        oldPrompt=copy.deepcopy(prompt)

    if class_type=='ForInnerEnd':
        startNum=prompt[unique_id]['inputs']['total'][0]
        inputNum=prompt[unique_id]['inputs']['obj'][0]
        maxKeyStr=sorted(list(prompt.keys()), key=lambda x: int(x.split(':')[0]))[-1]
        maxKey = int(maxKeyStr.split(':')[0])
        delKeys=list(set(get_del_keys(startNum,prompt)))
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
            #判断选择添加代码-----------结束---------
            if class_type=='IfInnerExecute' and x=='ANY':
                if outputs[input_unique_id][output_index][0]:
                    inputs['IF_FALSE']=oldPrompt[unique_id]['inputs']['IF_TRUE']
                else:
                    inputs['IF_TRUE']=oldPrompt[unique_id]['inputs']['IF_FALSE']
            #判断选择添加代码-----------结束---------
```
```python
        #循环添加代码----------开始----------
        if class_type=='ForInnerEnd':
            prompt[startNum]['inputs']=oldPrompt[startNum]['inputs']
            prompt[unique_id]['inputs']=oldPrompt[unique_id]['inputs']
            result = recursive_execute(server, prompt, outputs, startNum, extra_data, executed, prompt_id, outputs_ui, object_storage)
            if result[0] is not True:
                   return result
        if class_type=='IfInnerExecute':
            prompt[unique_id]['inputs']=oldPrompt[unique_id]['inputs']
        #循环添加代码-----------结束---------
```