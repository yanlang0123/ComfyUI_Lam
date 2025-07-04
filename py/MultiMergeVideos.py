import subprocess
import random
import os
import folder_paths

class MultiMergeVideos:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'video')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pathList": ("LIST",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("视频地址",)
    FUNCTION = "merge_videos_ffmpeg"

    CATEGORY = "lam"

    def merge_videos_ffmpeg(self,pathList, filename_prefix="ComfyUI"):
        """
        使用FFmpeg合并多个视频文件（需保证编码参数一致）
        :param video_files: 视频文件路径列表（按顺序排列）
        :param output_file: 输出文件名
        """
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        # 生成临时文件列表
        filename_with_batch_num = filename.replace("%batch_num%", "0")
        list_file=os.path.join(full_output_folder, filename_with_batch_num  + ".txt")
        video_path = os.path.join(full_output_folder, filename_with_batch_num  + ".mp4")
        with open(list_file, "w") as f:
            for file in pathList:
                f.write(f"file '{file}'\n")  # 注意单引号包裹路径:ml-citation{ref="4,5" data="citationList"}
        
        # 执行FFmpeg命令（无损合并）
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",  # 直接流复制，避免重新编码:ml-citation{ref="2,5" data="citationList"}
            "-map", "0",   # 包含所有流
            "-y",          # 覆盖已存在文件
            video_path
        ]
        try:
            subprocess.run(cmd, check=True)
            print(f"✓ 合并成功！输出文件: {video_path}")
        except subprocess.CalledProcessError as e:
            print(f"合并失败: {e.stderr}")
        finally:
            os.remove(list_file)  # 清理临时文件

        return (video_path, )

NODE_CLASS_MAPPINGS = {
    "MultiMergeVideos": MultiMergeVideos
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiMergeVideos": "多视频合并"
}
