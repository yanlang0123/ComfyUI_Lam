"""MiniMax H3 Reference to Video (Lam) - 图片数组/音频数组/音频数组 input variant."""

import math

import torch
import torchaudio

import comfy.model_management
import comfy.nested_tensor
import comfy.utils
import node_helpers
from comfy.comfy_types import ComfyNodeABC

CANVAS_MULTIPLE = 32
BASE_SHORT_EDGE = 768
MAX_PIXELS = 768 * 1344
REF_IMAGE_SHORT_EDGE = 2048
FPS = 24
AUDIO_LATENT_FPS = 40


def align_frame_count(n):
    while n % 17 != 5:
        n += 1
    return n


def video_latent_t(frame_count):
    return 2 if frame_count <= 5 else ((frame_count - 5) // 17) * 5 + 2


def temporal_shape(length):
    frame_count = align_frame_count(max(5, length))
    duration = frame_count / FPS
    return frame_count, video_latent_t(frame_count), round(duration * AUDIO_LATENT_FPS)


def _resize(image, width, height, crop):
    samples = image[..., :3].movedim(-1, 1)
    samples = comfy.utils.common_upscale(samples, width, height, "lanczos", crop)
    return samples.movedim(1, -1)


def _empty_av_latent(width, height, length, batch_size=1):
    frame_count, latent_t, audio_t = temporal_shape(length)
    video = torch.zeros([batch_size, 24, latent_t, height // 16, width // 16],
                        device=comfy.model_management.intermediate_device())
    audio = torch.zeros([batch_size, 32, 2, audio_t],
                        device=comfy.model_management.intermediate_device())
    return {"samples": comfy.nested_tensor.NestedTensor((video, audio))}, frame_count


class LamMiniMaxH3RefVideo(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip": ("CLIP", {}),
                "vae": ("VAE", {}),
                "audio_vae": ("VAE", {}),
                "prompt": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "width": ("INT", {"default": 1344, "min": 32, "max": 8192, "step": 32}),
                "height": ("INT", {"default": 768, "min": 32, "max": 8192, "step": 32}),
                "length": ("INT", {"default": 124, "min": 5, "max": 3600, "step": 17}),
                "ref_image_size": (["match", "max"], {"default": "match"}),
            },
            "optional": {
                "ref_images": ("IMAGE", {}),
                "ref_video_audios": ("AUDIO", {}),
                "ref_audios": ("AUDIO", {}),
            },
        }

    RETURN_TYPES = ("CONDITIONING", "LATENT")
    RETURN_NAMES = ("positive", "latent")
    FUNCTION = "execute"
    CATEGORY = "lam"
    DESCRIPTION = "MiniMax H3 图片+音频 参视频节点"

    @staticmethod
    def _encode_ref_audio(audio_vae, audio):
        waveform = audio["waveform"]  # [B, C, L]
        sr = audio["sample_rate"]
        vae_sr = getattr(audio_vae, "audio_sample_rate", 32000)
        if sr != vae_sr:
            waveform = torchaudio.functional.resample(waveform, sr, vae_sr)
        z = audio_vae.encode(waveform[:1].movedim(1, -1))  # [1, 32, 2, T]
        return z, z.shape[-1]

    def execute(self, clip, vae, audio_vae, prompt, width, height, length,
                ref_image_size="match", ref_images=None,
                ref_video_audios=None, ref_audios=None):
        latent, frame_count = _empty_av_latent(width, height, length)

        ref_items = []
        ref_blocks = []

        # 图片数组
        if ref_images is not None:
            if ref_image_size == "match":
                scale = min(1.0, math.sqrt((width * height) / (ref_images.shape[1] * ref_images.shape[2])))
            else:
                scale = min(1.0, REF_IMAGE_SHORT_EDGE / min(ref_images.shape[1], ref_images.shape[2]))
            tw = max(CANVAS_MULTIPLE, round(ref_images.shape[2] * scale / CANVAS_MULTIPLE) * CANVAS_MULTIPLE)
            th = max(CANVAS_MULTIPLE, round(ref_images.shape[1] * scale / CANVAS_MULTIPLE) * CANVAS_MULTIPLE)
            resized = _resize(ref_images, tw, th, "disabled")
            z = vae.encode(resized)
            ref_items.append({"type": "image", "data": resized})
            ref_blocks.append({"kind": "image", "latent_h": th // 16, "latent_w": tw // 16, "latent": z})

        # 音频数组 1: 视频伴音 (ref_video_audios)
        if ref_video_audios is not None:
            if not isinstance(ref_video_audios, (list, tuple)):
                ref_video_audios = [ref_video_audios]
            for audio in ref_video_audios:
                if audio is None:
                    continue
                audio_latent, ref_audio_t = self._encode_ref_audio(audio_vae, audio)
                ref_items.append({"type": "audio"})
                ref_blocks.append({"kind": "audio", "ref_audio_t": ref_audio_t, "audio_latent": audio_latent})

        # 音频数组 2: 独立音频 (ref_audios)
        if ref_audios is not None:
            if not isinstance(ref_audios, (list, tuple)):
                ref_audios = [ref_audios]
            for audio in ref_audios:
                if audio is None:
                    continue
                audio_latent, ref_audio_t = self._encode_ref_audio(audio_vae, audio)
                ref_items.append({"type": "audio"})
                ref_blocks.append({"kind": "audio", "ref_audio_t": ref_audio_t, "audio_latent": audio_latent})

        tokens = clip.tokenize(prompt, minimax_ref_items=ref_items)
        cond = clip.encode_from_tokens_scheduled(tokens)
        if ref_blocks:
            cond = node_helpers.conditioning_set_values(cond, {"minimax_refs": ref_blocks})

        return (cond, latent)


NODE_CLASS_MAPPINGS = {
    "LamMiniMaxH3RefVideo": LamMiniMaxH3RefVideo,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LamMiniMaxH3RefVideo": "Lam MiniMax H3 Reference to Video",
}
