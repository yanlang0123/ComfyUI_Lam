# ComfyUI_Lam

### Introduction
A plugin developed based on comfyUI.

#### Usage Instructions
Download and place in the plugin directory of comfyUI, as shown below:

![Alt text](解压存放路径及名称.png)

##### Special Note: For this version, execute the latest version "ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z" with cu121 inside. The version address is as follows:
https://github.com/comfyanonymous/ComfyUI/releases/download/latest/ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z

Then run the install.bat file, and if there are no errors, it's ready.

1. Model addresses and storage paths:
   - Lama model:
     https://huggingface.co/lllyasviel/Annotators/resolve/main/ControlNetLama.pth  ..\ComfyUI\models\lama\ControlNetLama.pth
   - SadTalker models:
     https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar ..\ComfyUI\models\SadTalker\mapping_00109-model.pth.tar
     https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar ..\ComfyUI\models\SadTalker\mapping_00229-model.pth.tar
     https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors ..\ComfyUI\models\SadTalker\SadTalker_V0.0.2_256.safetensors
     https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors ..\ComfyUI\models\SadTalker\SadTalker_V0.0.2_512.safetensors

2. Image-face-fusion model (Face swapping model)
   - Link: https://pan.baidu.com/s/19DOgJQ_RHNAjfNrzSr2uTQ?pwd=gf0p 
   - Extraction Code: gf0p
   - Extract to the directory ..\ComfyUI\models\image-face-fusion

3. Modify the execution.py file in the comfyUI root directory. Modify the content, search for "Return type mismatch between linked nodes," find the corresponding line, and replace
   ```python
   if r[val[1]] != type_input:
   ```
   with
   ```python
   if type_input !="*" and r[val[1]] != type_input:
   ```