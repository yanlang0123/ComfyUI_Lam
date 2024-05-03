import torch
import torchvision.transforms.functional as TF
import cv2
import numpy as np
class ImageAddMask:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "imageAddMask"

    CATEGORY = "lam"

    def imageAddMask(self, image, mask):
        image = tensor2rgba(image)
        mask_np=mask.numpy()
        mask_shape=mask_np.shape
        img_shape=image.size()
        if img_shape[1] != mask_shape[1] or img_shape[2] != mask_shape[2]:
            maskList=[]
            for i in range(mask.shape[0]):
                maskList.append(cv2.resize(mask_np[i],(img_shape[2],img_shape[1])))
            mask_np=np.array(maskList)

        mask=torch.from_numpy(mask_np)
        
        mask = 1.0 - mask
        image[:,:,:,-1] = mask

        return (image,)

def tensor2rgba(t: torch.Tensor) -> torch.Tensor:
    size = t.size()
    if (len(size) < 4):
        return t.unsqueeze(3).repeat(1, 1, 1, 4)
    elif size[3] == 1:
        return t.repeat(1, 1, 1, 4)
    elif size[3] == 3:
        alpha_tensor = torch.ones((size[0], size[1], size[2], 1))
        return torch.cat((t, alpha_tensor), dim=3)
    else:
        return t
    
def tensor2rgb(t: torch.Tensor) -> torch.Tensor:
    size = t.size()
    if (len(size) < 4):
        return t.unsqueeze(3).repeat(1, 1, 1, 3)
    if size[3] == 1:
        return t.repeat(1, 1, 1, 3)
    elif size[3] == 4:
        return t[:, :, :, :3]
    else:
        return t
def tensor2mask(t: torch.Tensor) -> torch.Tensor:
    size = t.size()
    if (len(size) < 4):
        return t
    if size[3] == 1:
        return t[:,:,:,0]
    elif size[3] == 4:
        # Not sure what the right thing to do here is. Going to try to be a little smart and use alpha unless all alpha is 1 in case we'll fallback to RGB behavior
        if torch.min(t[:, :, :, 3]).item() != 1.:
            return t[:,:,:,3]

    return TF.rgb_to_grayscale(tensor2rgb(t).permute(0,3,1,2), num_output_channels=1)[:,0,:,:]

NODE_CLASS_MAPPINGS = {
    "ImageAddMask": ImageAddMask
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageAddMask": "图片加遮罩"
}

