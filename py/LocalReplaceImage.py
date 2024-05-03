import math
import torch
import comfy.utils
import numpy as np
import cv2

class LoadReplaceImage:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"image_t": ("IMAGE", ),
                    "mask": ("MASK",),
                    "image_bt": ("IMAGE", ),
                    "x": ("INT", {"default": 0, "min": 0, "max": 99999, "step": 1}),
                    "y": ("INT", {"default": 0, "min": 0, "max": 99999, "step": 1}),
                    },
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("图片",)
    FUNCTION = "load_replace_image"
    def load_replace_image(self, image_t,mask,image_bt,x,y):
        mask_erosion = mask
        # if image_t.shape != image_bt.shape:
        #     image_bt = image_bt.permute(0, 3, 1, 2)
        #     image_bt = comfy.utils.common_upscale(image_bt, image_t.shape[2], image_t.shape[1], upscale_method='bicubic', crop='center')
        #     image_bt = image_bt.permute(0, 2, 3, 1)
        
        replace_image = self.blend_mode(image_t, image_bt, mask_erosion,x,y)
        return (replace_image,)

    def blend_mode(self, img1, img2, mask,y,x):
        mask_np=mask.numpy()
        if mask_np.ndim==2:
            mask_np=np.expand_dims(mask_np, axis=0)

        mask_shape=mask_np.shape
        img1_shape=img1.size()
        img2_shape=img2.size()

        if tuple(mask_shape)!=tuple(img1_shape):
            maskList=[]
            for i in range(mask_shape[0]):
                maskList.append(cv2.resize(mask_np[i],(img1_shape[2],img1_shape[1])))
            mask_np=np.array(maskList)
            mask_shape=mask_np.shape
        mask_np_rgb = np.zeros((mask_shape[0],mask_shape[1],mask_shape[2],3))
        mask_np_rgb[:,:,:,0] = mask_np
        mask_np_rgb[:,:,:,1] = mask_np
        mask_np_rgb[:,:,:,2] = mask_np
        
        mask=torch.from_numpy(mask_np_rgb)
        #取最少图片数量
        min_size=img2_shape[0]  if img1_shape[0]>img2_shape[0] else img1_shape[0]
        #图片大小不一致时，返回被替换内容
        if tuple(mask.size()[1:])!=tuple(img1_shape[1:]) or x+img1_shape[1]>img2_shape[1] or y+img1_shape[2]>img2_shape[2]:
            return img2

        img1[:min_size]=img1[:min_size]*mask[:min_size]
        img2[:min_size,x:x+img1_shape[1],y:y+img1_shape[2]]=img2[:min_size,x:x+img1_shape[1],y:y+img1_shape[2]]*(1-mask[:min_size])
        img2[:min_size,x:x+img1_shape[1],y:y+img1_shape[2]]=img1[:min_size]+img2[:min_size,x:x+img1_shape[1],y:y+img1_shape[2]]
        return img2


NODE_CLASS_MAPPINGS = {
    "LoadReplaceImage": LoadReplaceImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadReplaceImage": "图片局部替换"
}
