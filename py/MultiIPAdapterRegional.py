
class MultiIPAdapterRegional:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "body_masks": ("MASKS",),
                "image0": ("IMAGE",),
                "image1": ("IMAGE",),
            },
            "hidden": {"extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("IPADAPTER_PARAMS",)
    RETURN_NAMES = ("IPADAPTER_PARAMS",)
    FUNCTION = "ipadapter_params"
    CATEGORY = "lam"

    def ipadapter_params(self, body_masks, extra_pnginfo, unique_id, **kwargs):
        values = []
        for node in extra_pnginfo["workflow"]["nodes"]:
            if node["id"] == int(unique_id):
                values = node["properties"]["values"]
                break

        imageList = []
        for arg in kwargs:
            if arg.startswith('image'):
                imageList.append(kwargs[arg])
          
        minSize=min([len(imageList)])
        ipadapter_params=None
        for i in range(minSize):
            mask=body_masks[i] if len(body_masks)>i else None
            if ipadapter_params==None:
                ipadapter_params = {
                    "image": [imageList[i]],
                    "attn_mask": [mask],
                    "weight": [values[i][0]],
                    "weight_type": [values[i][1]],
                    "start_at": [values[i][2]],
                    "end_at": [values[i][3]],
                }
            else:
                ipadapter_params["image"] +=  [imageList[i]]
                ipadapter_params["attn_mask"] += [mask]
                ipadapter_params["weight"] += [values[i][0]]
                ipadapter_params["weight_type"] += [values[i][1]]
                ipadapter_params["start_at"] += [values[i][2]]
                ipadapter_params["end_at"] += [values[i][3]]
        
        return (ipadapter_params,)


NODE_CLASS_MAPPINGS = {
    "MultiIPAdapterRegional": MultiIPAdapterRegional
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiIPAdapterRegional": "多IPAdapter遮罩控制"
}
