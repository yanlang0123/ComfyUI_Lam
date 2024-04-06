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

dir = os.path.abspath(os.path.join(__file__, "../../docs"))
if not os.path.exists(dir):
    os.mkdir(dir)

@server.PromptServer.instance.routes.get("/lam/getImage")
async def get_groupNode(request):
    if "name" in request.rel_url.query:
        type = request.rel_url.query["type"]
        name = request.rel_url.query["name"]
        file = os.path.join(dir,type, name)
        if os.path.isfile(file):
            return web.FileResponse(file)
    return web.Response(status=404)

@server.PromptServer.instance.routes.get("/lam/getHeads")
def getStyles(request):
    filePath = os.path.join(dir,'hands')
    names=[]
    for root, dirs, files in os.walk(filePath):
      for file in files:
        if file.endswith(".png") or file.endswith(".jpg"):
            names.append(file)
    return web.json_response(names)
  

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

def get_bounding_box(coords,yWidth,yHeight,xReund=(0,0),YReund=(0,0)):
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
    wd=np.array(xReund) * width
    hd=np.array(YReund) * height
    min_x=int(min_x-wd[0])
    min_y=int(min_y-hd[0])
    width=int(width+wd[0]+wd[1])
    height=int(height+hd[0]+hd[1])
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

# 在大图片上添加小图片的函数
def add_image_to_background(background_image, small_image, location, size, angle, flipX=False,flipY=False):
    # 将小图片重新缩放
    resized_image = cv2.resize(small_image, size)
    
    # 如果需要翻转小图片，则进行翻转
    if flipX:
        resized_image = cv2.flip(resized_image, 1)  # 1 表示水平翻转
    if flipY:
        resized_image = cv2.flip(resized_image, 0)  # 0 表示垂直翻转
    
    # 将小图片旋转指定角度
    (h, w) = resized_image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle*-1, 1.0)
    rotated_image = cv2.warpAffine(resized_image, M, (w, h))
    
    # 计算小图片的放置位置
    (bx, by, bn) = background_image.shape
    (sx, sy, sn) = rotated_image.shape
    start_x = location[0]
    start_y = location[1]
    end_x = start_x + sx
    end_y = start_y + sy
    
    # 确保小图片不会超出大图片的边界
    if start_x < 0:
        dstart_x = -start_x
        start_x = 0
        end_x -= dstart_x
    if start_y < 0:
        dstart_y = -start_y
        start_y = 0
        end_y -= dstart_y
    if end_x > bx:
        dend_x = end_x - bx
        end_x = bx
        start_x -= dend_x
    if end_y > by:
        dend_y = end_y - by
        end_y = by
        start_y -= dend_y
    
    background_image[start_y:end_y, start_x:end_x] = rotated_image[0:end_y-start_y, 0:end_x-start_x]
    
    return background_image


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

  RETURN_TYPES = ("IMAGE","IMAGE","INT","INT","MASKS","MASKS",)
  RETURN_NAMES = ("image","handImg","width","height","head_masks","body_masks",)
  FUNCTION = "output_pose"

  CATEGORY = "lam"

  def output_pose(self, width,height,unique_id,wprompt,**kwargs):
    groups=[]
    hands=[]
    if unique_id in wprompt:
        if wprompt[unique_id]["inputs"]:
            for arg in wprompt[unique_id]["inputs"]:
              if arg.startswith("wPose_"):
                data=json.loads(wprompt[unique_id]["inputs"][arg])
                groups=data["groups"]
                hands=data["hands"]
                break
    head_masks=[]
    body_masks=[]
    candidate=[]
    subsets=[] 
    index=0
    for g in groups:
      head=get_bounding_box(g[-4:]+g[:2],width,height,(0.5,0.5),(1,0))
      if head:
        head_masks.append(create_mask(head,width,height))
      whole=get_bounding_box(g,width,height,(0.2,0.2),(0.2,0.2))
      if whole:
        body_masks.append(create_mask(whole,width,height)) 
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

    canvas = np.zeros(shape=(height,width, 3), dtype=np.uint8)
    canvasHands = np.zeros(shape=(height,width, 3), dtype=np.uint8)
    for i in range(len(hands)):
        zhand=hands[i]
        for hand in zhand:
          imgPath=os.path.join(dir,'hands',hand['name'])
          small = cv2.imread(imgPath)  # 小图片路径
          (h, w) = small.shape[:2]
          size = (int(w*abs(float(hand['scaleX']))),int(h*abs(float(hand['scaleY']))))  # 小图片的新尺寸
          location = (int(hand['x']-size[0]/2),int(hand['y']-size[1]/2))  # 小图片的左上角位置
          flipX = hand['flipX']
          flipY = hand['flipY']
          angle = float(hand['angle'])
          add_image_to_background(canvasHands,small,location,size,angle,flipX,flipY)
    image = draw_bodypose(canvas, candidate, subsets)
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image)[None,]

    handImage = np.array(canvasHands).astype(np.float32) / 255.0
    handImage = torch.from_numpy(handImage)[None,]

    return (image,handImage,width,height,head_masks,body_masks,)

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
