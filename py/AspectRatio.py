
class AspectRatio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (['704×1408 ∣ 1:2','704×1344 ∣ 11:21','768×1344 ∣ 4:7','768×1280 ∣ 3:5'
                                  ,'832×1216 ∣ 13:19','832×1152 ∣ 13:18','896×1152 ∣ 7:9','896×1088 ∣ 14:17'
                                  ,'960×1088 ∣ 15:17','960×1024 ∣ 15:16','1024×1024 ∣ 1:1','1024×960 ∣ 16:15'
                                  ,'1088×960 ∣ 17:15','1088×896 ∣ 17:14','1152×896 ∣ 9:7','1152×832 ∣ 18:13'
                                  ,'1216×832 ∣ 19:13','1280×768 ∣ 5:3','1344×768 ∣ 7:4','1344×704 ∣ 21:11'
                                  ,'1408×704 ∣ 2:1','1472×704 ∣ 23:11','1536×640 ∣ 12:5','1600×640 ∣ 5:2'
                                  ,'1664×576 ∣ 26:9','1728×576 ∣ 3:1','928×1664 ∣ 9:16','1664×928 ∣ 16:9'
                                  ,'1472×1140 ∣ 4:3','1140×1472 ∣ 3:4'], {"default": "1152×896 ∣ 9:7"}),
                "width": ("INT", {"default": 0, "min": 0, "max": 99999}),
                "height": ("INT", {"default": 0, "min": 0, "max": 99999}),
            }
        }
    RETURN_TYPES = ("INT","INT",)
    RETURN_NAMES = ("宽","高",)
    FUNCTION = "aspect_ratio"

    CATEGORY = "lam"

    def aspect_ratio(self,aspect_ratio,width,height):
        #判断不为自定义，提前宽高
        if width==0 and height==0:
            aspect_ratio = aspect_ratio.split("∣")
            width = int(aspect_ratio[0].split("×")[0])
            height = int(aspect_ratio[0].split("×")[1])
        return (width,height,)

NODE_CLASS_MAPPINGS = {
    "AspectRatio": AspectRatio
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "AspectRatio": "宽高比"
}
