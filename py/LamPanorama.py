import cv2
import numpy as np 
import math
import time
import os
import torch

def panorama_to_spherical(img):
    """
    改进的正向变换函数，使用双线性插值
    """
    rows, cols, c = img.shape
    # 优化：大幅提高中间图像分辨率
    # 原逻辑 R = cols / 2 / pi 导致垂直分辨率损失约70%
    # 新逻辑：直接使用原图高度作为半径，保证垂直细节不丢失
    R = rows
    D = R * 2
    cx = R
    cy = R
    
    # 创建目标图像的坐标网格
    j_coords, i_coords = np.mgrid[0:D, 0:D]
    
    # 计算极坐标参数
    r = np.sqrt((i_coords - cx)**2 + (j_coords - cy)**2)
    theta = np.arctan2(j_coords - cy, i_coords - cx)
    theta = np.where(theta < 0, theta + 2 * math.pi, theta)  # 调整角度到[0, 2π]
    
    # 计算源图像坐标
    xp = (theta / (2 * math.pi) * cols).astype(np.float32)
    yp = ((1 - r / R) * rows).astype(np.float32)  # 修正yp计算
    
    # 使用remap进行高质量变换
    valid_mask = r <= R
    
    # 为了避免边缘伪影，可以不强制设为-1，而是让它自然插值（或者保持-1）
    # 这里保持原逻辑，但使用更高质量插值
    xp[~valid_mask] = -1
    yp[~valid_mask] = -1
    
    # 使用 Lanczos 插值以获得更好的质量
    new_img = cv2.remap(img, xp, yp, cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    
    return new_img

# 更高质量的还原方案
def spherical_to_panorama(transformed_img, original_rows, original_cols):
    """
    使用向量化计算和Lanczos插值的高质量还原
    """
    D, D_c, c = transformed_img.shape
    # 优化：根据中间图的实际尺寸计算半径，自适应不同分辨率
    R = D // 2
    cx = R
    cy = R
    
    # 向量化生成网格
    x = np.arange(original_cols, dtype=np.float32)
    y = np.arange(original_rows, dtype=np.float32)
    X, Y = np.meshgrid(x, y)
    
    # 计算极坐标参数
    # r = (1 - y / original_rows) * R
    r = (1.0 - Y / original_rows) * R
    # theta = x / original_cols * 2 * math.pi
    theta = X / original_cols * 2 * math.pi
    
    # 极坐标转笛卡尔坐标
    # 必须转换为 float32 才能用于 cv2.remap
    map_x = (cx + r * np.cos(theta)).astype(np.float32)
    map_y = (cy + r * np.sin(theta)).astype(np.float32)
    
    # 使用 Lanczos 插值（更高质量）
    restored_img = cv2.remap(transformed_img, map_x, map_y, 
                            interpolation=cv2.INTER_LANCZOS4,
                            borderMode=cv2.BORDER_CONSTANT,
                            borderValue=0)
    
    return restored_img

class LamSpherical2Panorama:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                        "images": ("IMAGE", ),
                        "width": ("INT", {"default": 4096, "min": 64, "max": 9999999}),
                        "height": ("INT", {"default": 2048, "min": 64, "max": 9999999}),
                    },
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("图片",)
    FUNCTION = "spherical2Panorama"
    def spherical2Panorama(self, images,width,height):
        imaget_np=images.numpy()
        imgt_shape=imaget_np.shape
        prd_images=[]
        for i in range(imgt_shape[0]):
            imaget=np.uint8(imaget_np[i]*255)
            imaget = cv2.cvtColor(imaget, cv2.COLOR_BGR2RGB)
            transformed_img = spherical_to_panorama(imaget,height,width)

            fin_color = cv2.cvtColor(transformed_img, cv2.COLOR_BGR2RGB)
            prd_images.append(torch.from_numpy(np.array(fin_color).astype(np.float32) / 255.0))

        return (torch.stack(prd_images),)


class LamPanorama2Spherical:

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"images": ("IMAGE", ),
                    },
                }

    CATEGORY = "lam"

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("图片",)
    FUNCTION = "panorama2Spherical"
    def panorama2Spherical(self, images):
        imaget_np=images.numpy()
        imgt_shape=imaget_np.shape
        prd_images=[]
        for i in range(imgt_shape[0]):
            imaget=np.uint8(imaget_np[i]*255)
            imaget = cv2.cvtColor(imaget, cv2.COLOR_BGR2RGB)
            transformed_img = panorama_to_spherical(imaget)

            fin_color = cv2.cvtColor(transformed_img, cv2.COLOR_BGR2RGB)
            prd_images.append(torch.from_numpy(np.array(fin_color).astype(np.float32) / 255.0))

        return (torch.stack(prd_images),)


NODE_CLASS_MAPPINGS = {
    "LamPanorama2Spherical": LamPanorama2Spherical,
    "LamSpherical2Panorama": LamSpherical2Panorama
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamPanorama2Spherical": "全景图转球面图",
    "LamSpherical2Panorama": "球面图转全景图"
}
