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

6. Modify the execution.py file in the comfyUI root directory. Modify the content, search for "Return type mismatch between linked nodes," find the corresponding line, and replace
   ```python
   if r[val[1]] != type_input:
   ```
   with
   ```python
   if type_input !="*" and r[val[1]] != type_input:
   ```