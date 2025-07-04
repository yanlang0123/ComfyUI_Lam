from pydub import AudioSegment
import os
import folder_paths

class MultiMergeAudio:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'audio')
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
    RETURN_NAMES = ("音频地址",)
    FUNCTION = "merge_audios"

    CATEGORY = "lam"

    def merge_audios(self,pathList, filename_prefix="ComfyUI"):
        """
        使用FFmpeg合并多个视频文件（需保证编码参数一致）
        :param video_files: 视频文件路径列表（按顺序排列）
        :param output_file: 输出文件名
        """
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        # 生成临时文件列表
        filename_with_batch_num = filename.replace("%batch_num%", "0")
        video_path = os.path.join(full_output_folder, filename_with_batch_num  + ".mp3")

        # 初始化空的音频段
        combined = AudioSegment.empty()

        # 逐个加载并合并文件
        for mp3_file in pathList:
            audio = AudioSegment.from_mp3(mp3_file)
            combined += audio

        # 导出合并后的文件
        combined.export(video_path, format="mp3")
        return (video_path, )

NODE_CLASS_MAPPINGS = {
    "MultiMergeAudio": MultiMergeAudio
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiMergeAudio": "多个音频合并"
}
