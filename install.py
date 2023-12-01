import os
from time import sleep
from importlib.util import spec_from_file_location, module_from_spec
import sys
import argparse
import subprocess

this_module_name = "ComfyUI_Lam"
EXT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(EXT_PATH, "../../")))

parser = argparse.ArgumentParser()
parser.add_argument('--no_download_ckpts', action="store_true", help="Don't download any model")

args = parser.parse_args()

def add_global_shortcut_module(module_name, module_path):
    #Naming things is hard
    module_spec = spec_from_file_location(module_name, module_path)
    module = module_from_spec(module_spec)
    sys.modules[module_name] = module
    module_spec.loader.exec_module(module)

def download_models():
    #from git.repo import Repo
	#import folder_paths
    #download_path = os.path.join(folder_paths.models_dir,'image-face-fusion')
    #Repo.clone_from('https://www.modelscope.cn/damo/cv_unet_face_fusion_torch.git',to_path=download_path,branch='master')
    pass


# command1 = [sys.executable]
# if "python_embeded" in sys.executable: command1 += ['-s']
# command1 += ['-m','pip', 'install','-U', 'pip']
# print("upgrade pip...")
# sleep(2)
# proc = subprocess.Popen(command1, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
# for line in iter(proc.stdout.readline, ''):
#     print(line, end='')
# proc.wait()
# print("upgrade pip done")

command = [sys.executable]
if "python_embeded" in sys.executable: command += ['-s']
command += ['-m','pip', 'install','--use-pep517', '-r' , f'{EXT_PATH}/requirements.txt', 
    '--index-url' , 'https://mirrors.aliyun.com/pypi/simple',
    '--extra-index-url', 'https://download.pytorch.org/whl/cu117', '--no-warn-script-location']
print("Installing requirements...")
sleep(2)
proc = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
for line in iter(proc.stdout.readline, ''):
    print(line, end='')
proc.wait()
print("Installing requirements done")

if args.no_download_ckpts: exit()
print("Download models...")
download_models()
print("Download done")

# add_global_shortcut_module("cli_args", os.path.join(EXT_PATH, "../../comfy/cli_args.py"))
# add_global_shortcut_module("model_management", os.path.join(EXT_PATH, "../../comfy/model_management.py"))
# add_global_shortcut_module(this_module_name, os.path.join(EXT_PATH, "__init__.py"))


sleep(2)
download_models()
print("Done!")
