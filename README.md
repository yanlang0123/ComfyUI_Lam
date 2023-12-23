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


3. 修改comfyUI根目录下的execution.py文件，修改内容为,搜索“Return type mismatch between linked nodes”找到对应行，
替换
```python
if r[val[1]] != type_input:
```
为 
```python
if type_input !="*" and r[val[1]] != type_input:
```
