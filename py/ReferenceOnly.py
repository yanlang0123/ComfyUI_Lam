import torch
#说明
#1、 T2i 为原版的reference only 只能用于文生图，如果要图生图使用 使用Latent 复合的话 会有相互污染出现
#2、个人改写了代码，增加的了三个节点，主要是下面三个：
#   ①、用于图生图的 ReferenceOnlySimple_Img2Img
#   ②、用于文生图的使用遮罩：ReferenceOnlySimple_Masks
#   ③、用于图生图的 双reference only 参考的  ReferenceOnly_TwoReference_Img2Img  Ps:大概率是个玩具
#使用方法：从网盘下载python 文件，放到Comfyui的 custom_nodes 目录下即可，
# 示列：“E:\ComfyUI\ComfyUI\custom_nodes”
#PS:本插件主要用于对于人物一致性的探索，代码为个人改写的，仅仅只是尝试探索，个人B站账号：zhairy ,QQ：366310700 
#本插件开源，请勿用于倒卖，也勿用于其他违规用途！
#ReferenceOnly文生图节点
class ReferenceOnlySimple_T2i:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                              "reference": ("LATENT",),
                              "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
                              }}

    RETURN_TYPES = ("MODEL", "LATENT")
    FUNCTION = "reference_only_T2i"
    CATEGORY = "custom_node_experiments"

    def reference_only_T2i(self, model, reference, batch_size):
        model_reference = model.clone()
        size_latent = list(reference["samples"].shape)
        size_latent[0] = batch_size
        latent = {}
        latent["samples"] = torch.zeros(size_latent)
  
        batch = latent["samples"].shape[0] + reference["samples"].shape[0]
        # batch = reference["samples"].shape[0]
        def reference_apply(q, k, v, extra_options):
            k = k.clone().repeat(1, 2, 1)
            offset = 0
            if q.shape[0] > batch:
                offset = batch

            for o in range(0, q.shape[0], batch):
                for x in range(1, batch):
                    k[x + o, q.shape[1]:] = q[o,:]

            return q, k, k

        model_reference.set_model_attn1_patch(reference_apply)
        out_latent = torch.cat((reference["samples"], latent["samples"]))
        if "noise_mask" in latent:
            mask = latent["noise_mask"]
        else:
            mask = torch.ones((64,64), dtype=torch.float32, device="cpu")

        if len(mask.shape) < 3:
            mask = mask.unsqueeze(0)
        if mask.shape[0] < latent["samples"].shape[0]:
            print(latent["samples"].shape, mask.shape)
            mask = mask.repeat(latent["samples"].shape[0], 1, 1)

        out_mask = torch.zeros((1,mask.shape[1],mask.shape[2]), dtype=torch.float32, device="cpu")
        return (model_reference, {"samples": out_latent, "noise_mask": torch.cat((out_mask, mask))})
    
#ReferenceOnly图生图节点
class ReferenceOnlySimple_Img2Img:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                              "reference": ("LATENT",),
                              "latent": ("LATENT",),
                              "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
                              }}

    RETURN_TYPES = ("MODEL", "LATENT")
    FUNCTION = "reference_only_img2img"
    CATEGORY = "custom_node_experiments"

    def reference_only_img2img(self, model, reference, latent, batch_size):
        model_reference = model.clone()
        size_latent = list(reference["samples"].shape)
        size_latent[0] = batch_size

        batch = latent["samples"].shape[0] + reference["samples"].shape[0]
        def reference_apply(q, k, v, extra_options):
            k = k.clone().repeat(1, 2, 1)
            offset = 0
            if q.shape[0] > batch:
                offset = batch

            for o in range(0, q.shape[0], batch):
                for x in range(1, batch):
                    k[x + o, q.shape[1]:] = q[o,:]

            return q, k, k

        model_reference.set_model_attn1_patch(reference_apply)
        out_latent = torch.cat((reference["samples"], latent["samples"]))
        if "noise_mask" in latent:
            mask = latent["noise_mask"]
        else:
            mask = torch.ones((64,64), dtype=torch.float32, device="cpu")

        if len(mask.shape) < 3:
            mask = mask.unsqueeze(0)
        if mask.shape[0] < latent["samples"].shape[0]:
            print(latent["samples"].shape, mask.shape)
            mask = mask.repeat(latent["samples"].shape[0], 1, 1)

        out_mask = torch.zeros((1,mask.shape[1],mask.shape[2]), dtype=torch.float32, device="cpu")
        return (model_reference, {"samples": out_latent, "noise_mask": torch.cat((out_mask, mask))})


#ReferenceOnly遮罩节点
class ReferenceOnlySimple_Masks:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                              "reference": ("LATENT",),
                              "Mask_latent": ("LATENT",),
                              "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
                              }}

    RETURN_TYPES = ("MODEL", "LATENT")
    FUNCTION = "reference_only_mask"
    CATEGORY = "custom_node_experiments"

    def reference_only_mask(self, model, reference, Mask_latent, batch_size):
        model_reference = model.clone()
        size_latent = list(reference["samples"].shape)
        size_latent[0] = batch_size

        batch = Mask_latent["samples"].shape[0] + reference["samples"].shape[0]
        def reference_apply(q, k, v, extra_options):
            k = k.clone().repeat(1, 2, 1)
            offset = 0
            if q.shape[0] > batch:
                offset = batch
            for o in range(0, q.shape[0], batch):
                for x in range(1, batch):
                    k[x + o, q.shape[1]:] = q[o,:]
            return q, k, k

        model_reference.set_model_attn1_patch(reference_apply)
        out_latent = torch.cat((reference["samples"], Mask_latent["samples"]))
        if "noise_mask" in Mask_latent:
            mask = Mask_latent["noise_mask"]
        else:
            mask = torch.ones((64,64), dtype=torch.float32, device="cpu")

        if len(mask.shape) < 3:
            mask = mask.unsqueeze(0)
        if mask.shape[0] < Mask_latent["samples"].shape[0]:
            print(Mask_latent["samples"].shape, mask.shape)
            mask = mask.repeat(Mask_latent["samples"].shape[0], 1, 1)

        if len(mask.shape) < 4:
            out_mask = torch.zeros((1,mask.shape[1],mask.shape[2]), dtype=torch.float32, device="cpu")
        else:
            out_mask = torch.zeros((1,1,mask.shape[2],mask.shape[3]), dtype=torch.float32, device="cpu")

        return (model_reference, {"samples": out_latent, "noise_mask": torch.cat((out_mask, mask))})  

#ReferenceOnly_双参考图
class ReferenceOnly_TwoReference_Img2Img:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                              "reference": ("LATENT",),
                              "reference2": ("LATENT",),
                              "latent": ("LATENT",),
                              "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
                              }}

    RETURN_TYPES = ("MODEL", "LATENT")
    FUNCTION = "reference_only_tworeference_img2img"
    CATEGORY = "custom_node_experiments"

    def reference_only_tworeference_img2img(self, model, reference, reference2,latent,batch_size):
        model_reference = model.clone()
        size_latent = list(reference["samples"].shape)
        size_latent[0] = batch_size

        batch = latent["samples"].shape[0] + reference["samples"].shape[0] + reference2["samples"].shape[0]

        def reference_apply(q, k, v, extra_options):
            k = k.clone().repeat(1, 2, 1)
            offset = 0
            if q.shape[0] > batch:
                offset = batch

            re = extra_options["transformer_index"] % 2
            for o in range(0, q.shape[0], batch):
                for x in range(1, batch):
                    k[x + o, q.shape[1]:] = q[o + re,:]

            return q, k, k

        model_reference.set_model_attn1_patch(reference_apply)
        out_latent = torch.cat((reference["samples"], reference2["samples"], latent["samples"]))
        if "noise_mask" in latent:
            mask = latent["noise_mask"]
        else:
            mask = torch.ones((64,64), dtype=torch.float32, device="cpu")

        if len(mask.shape) < 3:
            mask = mask.unsqueeze(0)
        if mask.shape[0] < latent["samples"].shape[0]:
            print(latent["samples"].shape, mask.shape)
            mask = mask.repeat(latent["samples"].shape[0], 1, 1)

        out_mask = torch.zeros((1,mask.shape[1],mask.shape[2]), dtype=torch.float32, device="cpu")
        return (model_reference, {"samples": out_latent, "noise_mask": torch.cat((out_mask,out_mask, mask))})

NODE_CLASS_MAPPINGS = {
    "ReferenceOnlySimple_T2i": ReferenceOnlySimple_T2i,
    "ReferenceOnlySimple_Img2Img": ReferenceOnlySimple_Img2Img,
    "ReferenceOnlySimple_Masks": ReferenceOnlySimple_Masks,
    "ReferenceOnly_TwoReference_Img2Img":ReferenceOnly_TwoReference_Img2Img,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ReferenceOnlySimple_T2i": "仅参考文生图节点",
    "ReferenceOnlySimple_Img2Img": "仅参考图生图",
    "ReferenceOnlySimple_Masks": "仅参考遮罩节点",
    "ReferenceOnly_TwoReference_Img2Img": "仅参考双参考图"
}