from huggingface_hub import snapshot_download

models=[{
    "model_id":"Helsinki-NLP/opus-mt-zh-en",
    "local_dir":"models/opus-mt-zh-en",
    "endpoint":"https://hf-mirror.com",
}]

# repo_id 模型id
# local_dir 下载地址
# endpoint 镜像地址
# resume_download (中断后)继续下载
for model in models:
    snapshot_download(repo_id=model['model_id'], local_dir=model['local_dir'],
                    local_dir_use_symlinks=False, revision="main",
                    endpoint='https://hf-mirror.com',
                    resume_download=True)
