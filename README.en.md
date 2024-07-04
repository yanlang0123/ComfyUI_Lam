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

2. Image-face-fusion model (Face swapping model)
   - Link: https://pan.baidu.com/s/19DOgJQ_RHNAjfNrzSr2uTQ?pwd=gf0p 
   - Extraction Code: gf0p
   - Extract to the directory ..\ComfyUI\models\image-face-fusion

3. Modify the execution.py file in the comfyUI root directory.
windows  执行“修改文件.bat”文件，未报错后就可以了
linux  执行“修改文件.sh”文件，未报错后就可以了