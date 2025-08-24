import torch

class AudioBeforeAfterSilence():
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "audio": ("AUDIO", ),
                            "before": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "时长（秒）"}),
                            "after": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "时长（秒）"}),
                            }
                }
    
    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)  #返回参数名称

    FUNCTION = "before_after_silence"

    OUTPUT_NODE = False

    CATEGORY = "lam"
    def before_after_silence(self, audio, before, after):
        waveform=audio['waveform']
        sample_rate = audio['sample_rate']
        # 创建前后静音张量
        batch_size, num_channels, _ = waveform.shape
        beforeSilence = torch.zeros(batch_size, num_channels, int(sample_rate * before),
                                device=waveform.device,
                                dtype=waveform.dtype)
        afterSilence = torch.zeros(batch_size, num_channels, int(sample_rate * after),
                                device=waveform.device,
                                dtype=waveform.dtype)
            
        # 在前面和后面都插入静音
        audio_with_silence = torch.cat([beforeSilence, waveform, afterSilence], dim=-1)

        return ({"waveform": audio_with_silence, "sample_rate": sample_rate},)
    
NODE_CLASS_MAPPINGS = { #节点名称与类名对应关系
    "AudioBeforeAfterSilence": AudioBeforeAfterSilence,
}

NODE_DISPLAY_NAME_MAPPINGS = { #节点名称与显示名称对应关系
    "AudioBeforeAfterSilence": "音频前后加静音",
}
