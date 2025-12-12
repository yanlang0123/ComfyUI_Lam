from huggingface_hub import snapshot_download
import sys
import os

models={
    "nllb-200-distilled-1.3B":{
        "model_id":"facebook/nllb-200-distilled-1.3B",
        "local_dir":"models/nllb-200-distilled-1.3B",
        "endpoint":"https://hf-mirror.com",
    },
    "nllb-200-distilled-600M":{
        "model_id":"facebook/nllb-200-distilled-600M",
        "local_dir":"models/nllb-200-distilled-600M",
        "endpoint":"https://hf-mirror.com",
    }
}
# repo_id 模型id
# local_dir 下载地址
# endpoint 镜像地址
# resume_download (中断后)继续下载
args = sys.argv
for model_id,model in models.items():
    if len(args)>1 and model_id not in args: 
        continue
    print(f"Downloading {model_id}...")
    local_dir = os.path.join(os.path.dirname(__file__), model['local_dir'])
    snapshot_download(repo_id=model['model_id'], local_dir=local_dir,
                    local_dir_use_symlinks=False, revision="main",
                    endpoint='https://hf-mirror.com',
                    resume_download=True)
    
