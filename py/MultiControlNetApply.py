import folder_paths
import comfy.controlnet
class MultiControlNetApply:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
             "required": {
                "conditioning": ("CONDITIONING", ),
                "image0": ("IMAGE", ),
            },
            "optional": {
               "image1": ("IMAGE", {"extNetName":folder_paths.get_filename_list("controlnet")}),
                "control_net_name": (folder_paths.get_filename_list("controlnet"), )
            },
            "hidden": {"extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "multi_control_net_apply"

    CATEGORY = "lam"

    def multi_control_net_apply(self, conditioning, extra_pnginfo, unique_id,**kwargs):
        values=[]
        for node in extra_pnginfo["workflow"]["nodes"]:
            if node["id"] == int(unique_id):
                values = node["properties"]["values"]
                break
        imageList=[]
        for arg in kwargs:
            if arg.startswith('image'):
                imageList.append(kwargs[arg])

        minSize=len(imageList)
        for i in range(minSize):
            controlnet_path = folder_paths.get_full_path("controlnet", values[i][0])
            controlnet = comfy.controlnet.load_controlnet(controlnet_path)
            conditioning=self.apply_controlnet(conditioning, controlnet, imageList[i], float(values[i][1]))

        return (conditioning,)

    def apply_controlnet(self, conditioning, control_net, image, strength):
        if strength == 0:
            return conditioning

        c = []
        control_hint = image.movedim(-1,1)
        for t in conditioning:
            n = [t[0], t[1].copy()]
            c_net = control_net.copy().set_cond_hint(control_hint, strength)
            if 'control' in t[1]:
                c_net.set_previous_controlnet(t[1]['control'])
            n[1]['control'] = c_net
            n[1]['control_apply_to_uncond'] = True
            c.append(n)
        return c
    
    
NODE_CLASS_MAPPINGS = {
    "MultiControlNetApply": MultiControlNetApply
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiControlNetApply": "多ControlNet应用"
}