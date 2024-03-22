from PIL import Image
import os
import folder_paths
import hashlib
import torch
import numpy as np
import json
from .src.openPose.pose_body import Body
from .src.openPose.util import draw_bodypose
import server
from aiohttp import web
import os
import json
import cv2
from tools import annotator_ckpts_path,load_file_from_url


body_estimation = None
body_model_path = "https://hf-mirror.com/lllyasviel/Annotators/resolve/main/body_pose_model.pth"

@server.PromptServer.instance.routes.post("/lam/getImagePose")
async def getImagePose(request):
    global body_estimation # 声明 body_estimation 是全局变量
    post = await request.post()
    image = post.get("image")
    if image and image.file:
        # 将文件转换为 OpenCV 可以处理的格式
        nparr = np.frombuffer(image.file.read(), np.uint8)
        oriImg = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if body_estimation==None:
          body_modelpath = os.path.join(annotator_ckpts_path, "body_pose_model.pth")
          if not os.path.exists(body_modelpath):
            load_file_from_url(body_model_path, model_dir=annotator_ckpts_path)
          body_estimation=Body(body_modelpath)
        H, W, C = oriImg.shape
        YW=512*(1 if W>H else W/H)
        YH=512*(1 if W<H else H/W)
        candidate, subset = body_estimation(oriImg)
        if candidate.ndim == 2 and candidate.shape[1] == 4:
          candidate = candidate[:, :2]
          candidate[:, 0] /= float(W)
          candidate[:, 1] /= float(H)
        groups=[]
        subsets=[]
        for n in range(len(subset)):
          groups.append([[-1,-1]  if i<0 else [int(candidate[int(i)][0]*YW),int(candidate[int(i)][1]*YH)] for i in subset[n][:18]])
          sub=[]
          index=0
          for s in subset[n][:18]:
             if s>=0:
                sub.append(index)
                index+=1
             else:
                sub.append(s)
          subsets.append(sub)
        
        return web.json_response({'groups':groups,'subsets': subsets})

    return web.Response(status=404)

def get_bounding_box(coords,yWidth,yHeight,xReund=0,YReund=0):
    coords=[ x for x in coords if x[0]>=0 and x[1]>=0]
    if len(coords)==0:
      return None
    coords=np.array(coords).flatten().tolist()
    min_x = min(coords[0::2])  # 获取x坐标的最小值
    min_y = min(coords[1::2])  # 获取y坐标的最小值
    max_x = max(coords[0::2])  # 获取x坐标的最大值
    max_y = max(coords[1::2])  # 获取y坐标的最大值
    
    width = max_x - min_x  # 宽度
    height = max_y - min_y  # 高度
    wd=width*xReund
    hd=height*YReund
    min_x=int(min_x-wd/2)
    min_y=int(min_y-hd/2)
    width=int(width+wd)
    height=int(height+hd)
    min_x= min_x if min_x>0 else 0
    min_y= min_y if min_y>0 else 0
    width=width if width<yWidth else yWidth
    height=height if height<yHeight else yHeight

    return (min_x,min_y,width,height)

def solid_mask(value, width, height):
  out = torch.full((1, height, width), value, dtype=torch.float32, device="cpu")
  return out

def mask_combine(destination, source, x, y, operation="add"):
  output = destination.reshape((-1, destination.shape[-2], destination.shape[-1])).clone()
  source = source.reshape((-1, source.shape[-2], source.shape[-1]))

  left, top = (x, y,)
  right, bottom = (min(left + source.shape[-1], destination.shape[-1]), min(top + source.shape[-2], destination.shape[-2]))
  visible_width, visible_height = (right - left, bottom - top,)

  source_portion = source[:, :visible_height, :visible_width]
  destination_portion = destination[:, top:bottom, left:right]

  if operation == "multiply":
      output[:, top:bottom, left:right] = destination_portion * source_portion
  elif operation == "add":
      output[:, top:bottom, left:right] = destination_portion + source_portion
  elif operation == "subtract":
      output[:, top:bottom, left:right] = destination_portion - source_portion
  elif operation == "and":
      output[:, top:bottom, left:right] = torch.bitwise_and(destination_portion.round().bool(), source_portion.round().bool()).float()
  elif operation == "or":
      output[:, top:bottom, left:right] = torch.bitwise_or(destination_portion.round().bool(), source_portion.round().bool()).float()
  elif operation == "xor":
      output[:, top:bottom, left:right] = torch.bitwise_xor(destination_portion.round().bool(), source_portion.round().bool()).float()

  output = torch.clamp(output, 0.0, 1.0)
  return output

def create_mask(data,width,height):
   destination=solid_mask(0.0,width,height)
   source=solid_mask(1.0,data[-2],data[-1])
   return mask_combine(destination, source,data[0],data[1], operation="add")


class openPoseEditorPlus:
  @classmethod
  def INPUT_TYPES(self):
    temp_dir = folder_paths.get_temp_directory()

    if not os.path.isdir(temp_dir):
      os.makedirs(temp_dir)

    temp_dir = folder_paths.get_temp_directory()

    return {"required":
              {
                "index": ("INT", {"default": 0, "min": 0, "max": 99999}),
                "width": ("INT", {"default": 512, "min": 0, "max": 99999}),
                "height": ("INT", {"default": 512, "min": 0, "max": 99999}),
              },
              "hidden": {"unique_id": "UNIQUE_ID","wprompt":"PROMPT"},
              
            }

  RETURN_TYPES = ("IMAGE","INT","INT","MASKS",)
  RETURN_NAMES = ("image","width","height","masks",)
  FUNCTION = "output_pose"

  CATEGORY = "image"

  def output_pose(self, width,height,unique_id,wprompt,**kwargs):
    groups=[]
    if unique_id in wprompt:
        if wprompt[unique_id]["inputs"]:
            for arg in wprompt[unique_id]["inputs"]:
              if arg.startswith("wPose_"):
                groups=json.loads('{"groups":' + wprompt[unique_id]["inputs"][arg]+ '}')["groups"]
                break
    masks=[]
    candidate=[]
    subsets=[] 
    index=0
    for g in groups:
      head=get_bounding_box(g[-4:]+g[:2],width,height,1,1)
      if head:
        masks.append(create_mask(head,width,height))
      whole=get_bounding_box(g,width,height,0.5,0.2)
      if whole:
        masks.append(create_mask(whole,width,height)) 
      subset=[]
      for i in range(len(g)):
         if g[i][0]<0 or g[i][1]<0:
            subset.append(-1)
         else:
            candidate.append(g[i])
            subset.append(index)
            index+=1
            
      subsets.append(subset)

    candidate=[[i[0]/float(width),i[1]/float(height)] for i in candidate ]

    canvas = np.zeros(shape=(width, height, 3), dtype=np.uint8)
    image = draw_bodypose(canvas, candidate, subsets)
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image)[None,]

    return (image,width,height,masks,)

  @classmethod
  def IS_CHANGED(self, image):
    image_path = os.path.join(
      folder_paths.get_temp_directory(), image)
    # print(f'Change: {image_path}')

    m = hashlib.sha256()
    with open(image_path, 'rb') as f:
      m.update(f.read())
    return m.digest().hex()


NODE_CLASS_MAPPINGS = {
    "LAM.OpenPoseEditorPlus": openPoseEditorPlus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LAM.OpenPoseEditorPlus": "姿态编辑器",
}
