# ComfyUI_Lam

### 介绍
基于comfyUI开发的插件

#### 使用说明
下载放到comfyUI的插件目录，如下:

![Alt text](解压存放路径及名称.png)

##### 特别说明该版本执行最新版“ComfyUI_windows_portable_nvidia_cu118_or_cpu.7z” 里面带cu118的版本地址如下：
https://github.com/comfyanonymous/ComfyUI/releases/download/latest/ComfyUI_windows_portable_nvidia_cu118_or_cpu.7z

1. 根据图片解压到指定插件目录及名称，
将insightface.rar解压到..\ComfyUI_windows_portable\python_embeded\Lib\site-packages目录
将venv.rar解压到..\ComfyUI_windows_portable\python_embeded\Lib\site-packages目录
然后运行install.bat文件，未报错后就可以了，

2. 模型地址，及存放路径：
lama模型：
https://huggingface.co/lllyasviel/Annotators/resolve/main/ControlNetLama.pth  ..\ComfyUI\models\lama\ControlNetLama.pth
SadTalker模型：
https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar ..\ComfyUI\models\SadTalker\mapping_00109-model.pth.tar
https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar ..\ComfyUI\models\SadTalker\mapping_00229-model.pth.tar
https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors ..\ComfyUI\models\SadTalker\SadTalker_V0.0.2_256.safetensors
https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors ..\ComfyUI\models\SadTalker\SadTalker_V0.0.2_512.safetensors

3. gfpgan是根据启动目录来的，根据提示对应
https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth ..\ComfyUI_windows_portable\gfpgan\weights\alignment_WFLW_4HG.pth 
https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth ..\ComfyUI_windows_portable\gfpgan\weights\detection_Resnet50_Final.pth 
https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth ..\ComfyUI_windows_portable\gfpgan\weights\GFPGANv1.4.pth 
https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth ..\ComfyUI_windows_portable\gfpgan\weights\parsing_parsenet.pth 

4. image-face-fusion模型换脸模型
链接：https://pan.baidu.com/s/19DOgJQ_RHNAjfNrzSr2uTQ?pwd=gf0p 
提取码：gf0p
解压到 ..\ComfyUI\models\image-face-fusion 目录

5. roop-face-swap模型换脸模型
链接：https://pan.baidu.com/s/1cJeRtqgdeNW21Hljwuv-tA?pwd=b4yy 
提取码：b4yy
解压到 ..\ComfyUI\models\roop-face-swap 目录


6. 修改comfyUI根目录下的execution.py文件，修改内容为,搜索“Return type mismatch between linked nodes”找到对应行，
替换
```python
if r[val[1]] != type_input:
```
为 
```python
if type_input !="*" and r[val[1]] != type_input:
```

搜索 “def recursive_execute” 
位置参考图如下：
![Alt text](修改位置.png)
新增内容：
```python
#循环添加代码----------开始----------
def get_del_keys(key, prompt):
    keys=[]
    for k,v in prompt.items():
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
    delKeys=[]
    if class_type=='ForInnerEnd':
        startNum=prompt[unique_id]['inputs']['total'][0]
        inputNum=prompt[unique_id]['inputs']['images'][0]
        startInput=prompt[startNum]['inputs']
        maxKey = int(sorted(list(prompt.keys()), key=lambda x: int(x))[-1])
        delKeys=list(set(get_del_keys(startNum,prompt)))
        delKeys.append(startNum)
        delKeys = list(filter(lambda x: x != inputNum, delKeys))
        for i in range(startInput['i']+1,startInput['total'],startInput['stop']):
            prompt[str(maxKey+i)]=prompt[inputNum]
            prompt[unique_id]['inputs']['images'+str(i)]=[str(maxKey+i),prompt[unique_id]['inputs']['images'][-1]]

    #循环添加代码-----------结束---------
```
```python
                #循环添加代码----------开始----------
                if class_type=='ForInnerEnd' and x !='images' and x.startswith('images'):
                    if startNum!=None:
                        prompt[startNum]['inputs']['i']=prompt[startNum]['inputs']['i']+prompt[startNum]['inputs']['stop']
                        for key in delKeys:
                            outputs.pop(key, None)
                #循环添加代码-----------结束---------
```