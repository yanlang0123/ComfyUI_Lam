import os
import shutil
import requests

from comfy_api.latest import io, ui
from comfy_api.input import VideoInput
from comfy_api.util import VideoContainer, VideoCodec

import folder_paths


def _save_video_to_output(video_path: str, filename_prefix: str):
    """Copy a local file or download an http(s) URL into the ComfyUI output directory.

    Returns the final saved path and a list of SavedResult entries for the frontend preview.
    """
    full_output_folder, filename, counter, subfolder, _ = folder_paths.get_save_image_path(
        filename_prefix, folder_paths.get_output_directory()
    )
    fmt = video_path.rsplit(".", 1)[-1]
    file = f"{filename}_{counter:05}_.{VideoContainer.get_extension(fmt)}"
    file_path = os.path.join(full_output_folder, file)
    if video_path.startswith("http"):
        response = requests.get(video_path)
        with open(file_path, "wb") as f:
            f.write(response.content)
    else:
        shutil.copyfile(video_path, file_path)
    saved = ui.SavedResult(file, subfolder, io.FolderType.output)
    return file_path, [saved]


class LamSaveVideo(io.ComfyNode):
    """Save a VideoInput to the output directory and return its on-disk path."""

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="LamSaveVideo",
            display_name="保存视频输出",
            category="lam",
            search_aliases=["save video", "export video"],
            inputs=[
                io.Video.Input("video", tooltip="The video to save."),
                io.String.Input(
                    "filename_prefix",
                    default="video/ComfyUI",
                    tooltip="The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes.",
                ),
                io.Combo.Input(
                    "format",
                    options=VideoContainer.as_input(),
                    default="auto",
                    tooltip="The format to save the video as.",
                ),
                io.Combo.Input(
                    "codec",
                    options=VideoCodec.as_input(),
                    default="auto",
                    tooltip="The codec to use for the video.",
                ),
            ],
            hidden=[io.Hidden.prompt, io.Hidden.extra_pnginfo],
            outputs=[io.String.Output("video_path")],
            is_output_node=True,
        )

    @classmethod
    def execute(cls, video: VideoInput, filename_prefix: str, format: str, codec: str) -> io.NodeOutput:
        full_output_folder, filename, counter, subfolder, _ = folder_paths.get_save_image_path(
            filename_prefix,
            folder_paths.get_output_directory(),
            video.get_dimensions()[0],
            video.get_dimensions()[1],
        )
        file = f"{filename}_{counter:05}_.{VideoContainer.get_extension(format)}"
        file_path = os.path.join(full_output_folder, file)

        metadata = None
        if cls.hidden.extra_pnginfo is not None:
            metadata = dict(cls.hidden.extra_pnginfo)
        if cls.hidden.prompt is not None:
            metadata = metadata or {}
            metadata["prompt"] = cls.hidden.prompt

        video.save_to(file_path, format=VideoContainer(format), codec=codec, metadata=metadata)

        saved = ui.SavedResult(file, subfolder, io.FolderType.output)
        return io.NodeOutput(file_path, ui=ui.PreviewVideo([saved]))


class LamViewVideoOut(io.ComfyNode):
    """Copy a local video file (or download an http(s) URL) into the output directory and return the saved path."""

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="LamViewVideoOut",
            display_name="视频转存预览输出",
            category="lam",
            search_aliases=["save video path", "copy video", "video to output"],
            inputs=[
                io.String.Input(
                    "video_path",
                    default="",
                    tooltip="The path to the video to save.",
                ),
                io.String.Input(
                    "filename_prefix",
                    default="video/ComfyUI",
                    tooltip="The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes.",
                ),
            ],
            hidden=[io.Hidden.prompt, io.Hidden.extra_pnginfo],
            outputs=[io.String.Output("video_path")],
        )

    @classmethod
    def execute(cls, video_path: str, filename_prefix: str) -> io.NodeOutput:
        file_path, saved = _save_video_to_output(video_path, filename_prefix)
        return io.NodeOutput(file_path, ui=ui.PreviewVideo(saved))


class LamViewVideo(io.ComfyNode):
    """Copy a local video file (or download an http(s) URL) into the output directory and preview it."""

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="LamViewVideo",
            display_name="视频转存预览",
            category="lam",
            search_aliases=["save video path", "copy video", "video to output"],
            inputs=[
                io.String.Input(
                    "video_path",
                    default="",
                    tooltip="The path to the video to save.",
                ),
                io.String.Input(
                    "filename_prefix",
                    default="video/ComfyUI",
                    tooltip="The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes.",
                ),
            ],
            hidden=[io.Hidden.prompt, io.Hidden.extra_pnginfo],
            is_output_node=True,
        )

    @classmethod
    def execute(cls, video_path: str, filename_prefix: str) -> io.NodeOutput:
        _, saved = _save_video_to_output(video_path, filename_prefix)
        return io.NodeOutput(ui=ui.PreviewVideo(saved))


class LamSaveVideoNoOutput(io.ComfyNode):
    """Save a VideoInput to the output directory and expose the saved file path."""

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="LamSaveVideoNoOutput",
            display_name="保存视频输出（非输出节点）",
            category="lam",
            search_aliases=["save video", "export video", "no output"],
            inputs=[
                io.Video.Input("video", tooltip="The video to save."),
                io.String.Input(
                    "filename_prefix",
                    default="video/ComfyUI",
                    tooltip="The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes.",
                ),
                io.Combo.Input(
                    "format",
                    options=VideoContainer.as_input(),
                    default="auto",
                    tooltip="The format to save the video as.",
                ),
                io.Combo.Input(
                    "codec",
                    options=VideoCodec.as_input(),
                    default="auto",
                    tooltip="The codec to use for the video.",
                ),
            ],
            outputs=[
                io.String.Output(
                    "video_path",
                    tooltip="The full path of the saved video file.",
                ),
            ],
            hidden=[io.Hidden.prompt, io.Hidden.extra_pnginfo],
            is_output_node=False,
        )

    @classmethod
    def execute(cls, video: VideoInput, filename_prefix: str, format: str, codec: str) -> io.NodeOutput:
        full_output_folder, filename, counter, subfolder, _ = folder_paths.get_save_image_path(
            filename_prefix,
            folder_paths.get_output_directory(),
            video.get_dimensions()[0],
            video.get_dimensions()[1],
        )
        file = f"{filename}_{counter:05}_.{VideoContainer.get_extension(format)}"
        file_path = os.path.join(full_output_folder, file)

        metadata = None
        if cls.hidden.extra_pnginfo is not None:
            metadata = dict(cls.hidden.extra_pnginfo)
        if cls.hidden.prompt is not None:
            metadata = metadata or {}
            metadata["prompt"] = cls.hidden.prompt

        video.save_to(file_path, format=VideoContainer(format), codec=codec, metadata=metadata)
        saved = ui.SavedResult(file, subfolder, io.FolderType.output)

        return io.NodeOutput(file_path, ui=ui.PreviewVideo([saved]))


NODE_CLASS_MAPPINGS = {
    "LamSaveVideo": LamSaveVideo,
    "LamViewVideo": LamViewVideo,
    "LamViewVideoOut": LamViewVideoOut,
    "LamSaveVideoNoOutput": LamSaveVideoNoOutput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamSaveVideo": "保存视频输出",
    "LamViewVideo": "视频转存预览",
    "LamViewVideoOut": "视频转存预览输出",
    "LamSaveVideoNoOutput": "保存视频输出（非输出节点）",
}