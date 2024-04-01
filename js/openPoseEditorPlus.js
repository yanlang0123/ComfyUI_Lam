import { app } from "../../../scripts/app.js";
import { fabric } from "./fabric.js";
import { api } from "../../../scripts/api.js";

fabric.Object.prototype.transparentCorners = false;
fabric.Object.prototype.cornerColor = "#108ce6";
fabric.Object.prototype.borderColor = "#108ce6";
fabric.Object.prototype.cornerSize = 10;

let connect_keypoints = [
  [0, 1],
  [1, 2],
  [2, 3],
  [3, 4],
  [1, 5],
  [5, 6],
  [6, 7],
  [1, 8],
  [8, 9],
  [9, 10],
  [1, 11],
  [11, 12],
  [12, 13],
  [0, 14],
  [14, 16],
  [0, 15],
  [15, 17],
];
let connect_color = [
  [0, 0, 255],
  [255, 0, 0],
  [255, 170, 0],
  [255, 255, 0],
  [255, 85, 0],
  [170, 255, 0],
  [85, 255, 0],
  [0, 255, 0],
  [0, 255, 85],
  [0, 255, 170],
  [0, 255, 255],
  [0, 170, 255],
  [0, 85, 255],
  [85, 0, 255],
  [170, 0, 255],
  [255, 0, 255],
  [255, 0, 170],
  [255, 0, 85],
];

const default_keypoints = [
  [241, 57],
  [241, 120],
  [191, 118],
  [177, 183],
  [163, 252],
  [298, 118],
  [317, 182],
  [332, 245],
  [225, 241],
  [213, 359],
  [215, 454],
  [270, 240],
  [282, 360],
  [286, 456],
  [230, 48],
  [255, 48],
  [215, 52],
  [270, 52],
];
const default_subset=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
const asyncLoadImg = (imgURL) => {
  return new Promise((resolve,reject) => {
      // 2.6.0 版本没有对图片加载异常的处理，需要自己处理
      fabric.Image.fromURL(imgURL, img => {
          // 加载出错提示，否则会造成渲染出错
          if(img._originalElement === null){
            reject('图片加载出错啦~~~')  
          }else {
            resolve(img)
          }
      })
      // 4.2.0版本有错误处理 
      // fabric.Image.fromURL(imgURL, (img,isError) => {})
  })
}
class OpenPose {
  constructor(node, canvasElement) {
    this.lockMode = false;
    this.visibleEyes = true;
    this.flipped = false;
    this.node = node;
    this.undo_history = LS_Poses[node.name].undo_history || [];
    this.redo_history = LS_Poses[node.name].redo_history || [];
    this.groups = [];
    this.subsets = [];
    this.hands = [];
    this.index = 0
    this.history_index = 0;
    this.history_change = false;
    this.canvas = this.initCanvas(canvasElement);
        // 创建用于选择图片的input元素
    this.addPoseDemoInput = document.createElement("input");
    this.addPoseDemoInput.type = "file";
    this.addPoseDemoInput.accept = "image/*";
    this.addPoseDemoInput.style.display = "none";
    this.addPoseDemoInput.addEventListener("change", this.addPoseDemo.bind(this));
    document.body.appendChild(this.addPoseDemoInput);

    }

	// 处理背景图片的加载
  addPoseDemo(e) {
    const file = this.addPoseDemoInput.files[0];
    if(file){
      this.getImageOpse(file)
    }
  }

    // 设置背景图片
  setBackgroundImage(url) {
        fabric.Image.fromURL(url, (img) => {
            img.set({
                originX: 'left',
                originY: 'top',
                opacity: 0.5
            });
            
			this.canvas.setWidth(img.width);
			this.canvas.setHeight(img.height);
			
            this.canvas.setBackgroundImage(img, this.canvas.renderAll.bind(this.canvas));
        });
    }
  
  //左右翻转
  fliplf() {
    let aobj=this.canvas.getActiveObject()
    if(!aobj){
      alert("请选择一只需要翻转的手")
    }
    if(aobj&&aobj['itype']&&aobj['itype']=='hand'){
      this.canvas.getActiveObject().set('flipX', !this.canvas.getActiveObject().flipX);
      this.canvas.renderAll();
    }else{
      alert("只有手能翻转")
    }
  }
  //上下翻转
  fliptd() {
    let aobj=this.canvas.getActiveObject()
    if(!aobj){
      alert("请选择一只需要翻转的手")
    }
    if(aobj&&aobj['itype']&&aobj['itype']=='hand'){
      this.canvas.getActiveObject().set('flipX', !this.canvas.getActiveObject().flipX);
      this.canvas.renderAll();
    }else{
      alert("只有手能翻转")
    }
  }
  // 异步加载图片

  async addHand(obj,isEdit=true,group=undefined){
    // 引入fabric.js库
    let thi=this
    let x=obj['l'],y=obj['t'];
    let img = await asyncLoadImg(`/lam/getImage?type=hands&&name=${obj.name}`)
    let left=x?x-img.width*0.1/2:0,top=y?y-img.height*0.1/2:0;
    let nobj=Object.assign({
      left: left, // 图片的初始水平位置
      top: top, // 图片的初始垂直位置
      angle: 0, // 图片的初始旋转角度
      opacity: 0.95, // 图片透明度
      // 这里可以通过scaleX和scaleY来设置图片绘制后的大小，这里为原来大小的一半
      scaleX: 0.1, 
      scaleY: 0.1,
      flipX:false,
      flipY:false,
      selectable: isEdit,
      evented: isEdit,
    }, obj);
    img.set(nobj);
    img['itype']='hand'
    if(group){
      group.addWithUpdate(img);
    }else{
      thi.canvas.add(img); // 将图片添加到画布上
    }
    if(x && y){
      thi.canvas.setActiveObject(img); //选中
      thi.hands[thi.history_index].push({
        left: left, // 图片的初始水平位置
        top: top, // 图片的初始垂直位置
        angle: 0, // 图片的初始旋转角度
        name:obj.name,
        scaleX: 0.1, 
        scaleY: 0.1,
        flipX:false,
        flipY:false,
        x:x,
        y:y
      })
      thi.canvas.requestRenderAll();
    }
    return img
  }

  setCanvasWidth(width){
    this.canvas.setWidth(width)
  }
  setCanvasHeight(height){
    this.canvas.setHeight(height)
  }
  delIndexPose(){
    let delIndex=this.history_index
    this.groups.splice(delIndex,1)
    this.subsets.splice(delIndex,1)
    this.hands.splice(delIndex,1)
    this.node.widgets[this.index].value =0;
    this.node.widgets[this.index].options['max']=this.groups.length-1;
    this.node.setDirtyCanvas(true);
    this.setIndexPose(0,false)
  }
  setIndexPose(v,isChangIndex=true){
    this.lockMode=true
    if(isChangIndex){
      this.changeIndexPose()
    }
    this.history_index=v
    let groups=this.groups
    let hands=this.hands
    let vgroups=[]
    for (let i = 0; i < groups.length; i++) {
      if(i==v){
        continue;
      }
      vgroups.push(groups[i])
    }
    this.setPose([],vgroups,false)
    for (let i = 0; i < hands.length; i++) {
      if(i==v){
        continue;
      }
      for(let j = 0; j < hands[i].length; j++){
        this.addHand(hands[i][j],false)
      }
    }
    this.addPose(groups[v],true,hands[v])
    this.lockMode=false
  }

   changeIndexPose(index=undefined){
    if(index===undefined){
      index=this.history_index
    }
    this.canvas.discardActiveObject();
    let json=this.getJSON();
    if (json["keypoints"].length>0&&json["keypoints"].length >1) {
      let keypoints=json["keypoints"]
      let group=[]
      let subset=this.subsets[index]
      for(let i = 0; i < subset.length; i ++){
        if(subset[i]<0){
          group.push([-1,-1])
        }else{
          group.push(keypoints[subset[i]])
        }
      }

      this.groups[index]=group
    }
    if(json['hands'].length>0){
      this.hands[index]=json['hands']
    }else{
      this.hands[index]=[]
    }
  }

  setPose(keypoints,groups=[],isEdit=true) {
    this.canvas.clear();

    this.canvas.backgroundColor = "#000";

    let res = [];
    if(groups.length>0){
      res=groups;
    }
    for (let i = 0; i < keypoints.length; i += 18) {
      const chunk = keypoints.slice(i, i + 18);
      res.push(chunk);
    }

    for (let item of res) {
      this.addPose(item,isEdit);
      this.canvas.discardActiveObject();
    }
  }

  async addPose(keypoints = undefined,isEdit=true,hands=[]) {
    if (keypoints === undefined) {
      keypoints = default_keypoints;
      this.changeIndexPose()
      this.setPose([],this.groups,false)
      this.groups.push(keypoints);
      this.subsets.push(default_subset);
      this.hands.push(hands);
      this.node.widgets[this.index].value = this.groups.length-1;
      this.node.widgets[this.index].options['max']=this.groups.length-1;
      this.history_index=this.node.widgets[this.index].value
    }

    const group = new fabric.Group();

    const makeCircle = (
      color,
      left,
      top,
      line1,
      line2,
      line3,
      line4,
      line5
    ) => {
      let c = new fabric.Circle({
        left: left,
        top: top,
        strokeWidth: 1,
        radius: 5,
        fill: color,
        stroke: color,
      });

      c.hasControls = c.hasBorders = false;
      c.line1 = line1;
      c.line2 = line2;
      c.line3 = line3;
      c.line4 = line4;
      c.line5 = line5;

      return c;
    };

    const makeLine = (coords, color) => { 
      return new fabric.Line(coords, {
        fill: color,
        stroke: color,
        strokeWidth: 10,
        selectable: false,
        evented: false,
      });
    };

    const lines = {};
    const circles = [];
    for (let i = 0; i < connect_keypoints.length; i++) {
      // 连线
      const item = connect_keypoints[i];
      if(keypoints[item[0]][0]<0||keypoints[item[0]][1]<0||keypoints[item[1]][0]<0||keypoints[item[1]][1]<0){
          continue;
      }
      const line = makeLine(
        keypoints[item[0]].concat(keypoints[item[1]]),
        `rgba(${connect_color[i].join(", ")}, 0.7)`
      );
      lines[i]=line;
      this.canvas.add(line);
    }

    for (let i = 0; i < keypoints.length; i++) {
      if(keypoints[i][0]<0||keypoints[i][1]<0){
          continue;
      }
      let list = [];

      connect_keypoints.filter((item, idx) => {
        if (item.includes(i)) {
          list.push(lines[idx]);
          return idx;
        }
      });
      const circle = makeCircle(
        `rgb(${connect_color[i].join(", ")})`,
        keypoints[i][0],
        keypoints[i][1],
        ...list
      );
      circle["id"] = i;
      circles.push(circle);
      group.addWithUpdate(circle);
    }
    for(let i = 0; i < hands.length; i++){
      await this.addHand(hands[i],true,group)
    }
    this.canvas.discardActiveObject();
    //不可编辑
    if(isEdit){
        this.canvas.setActiveObject(group);
        this.canvas.add(group);  
        group.toActiveSelection(); 
    }
    this.canvas.requestRenderAll();
  }

  initCanvas() {
    this.canvas = new fabric.Canvas(this.canvas, {
      backgroundColor: "#000",
      preserveObjectStacking: true,
    });

    const updateLines = (target) => {
      if ("_objects" in target) {
        const flipX = target.flipX ? -1 : 1;
        const flipY = target.flipY ? -1 : 1;
        this.flipped = flipX * flipY === -1;
        const showEyes = this.flipped ? !this.visibleEyes : this.visibleEyes;

        if (target.angle === 0) {
          const rtop = target.top;
          const rleft = target.left;
          for (const item of target._objects) {
            let p = item;
            if(p['itype']&&p['itype']=='hand'){
              continue
            }
            p.scaleX = 1;
            p.scaleY = 1;
            const top =
              rtop +
              p.top * target.scaleY * flipY +
              (target.height * target.scaleY) / 2;
            const left =
              rleft +
              p.left * target.scaleX * flipX +
              (target.width * target.scaleX) / 2;
            p["_top"] = top;
            p["_left"] = left;
            if (p["id"] === 0) {
              p.line1 && p.line1.set({ x1: left, y1: top });
            } else {
              p.line1 && p.line1.set({ x2: left, y2: top });
            }
            if (p["id"] === 14 || p["id"] === 15) {
              p.radius = showEyes ? 5 : 0;
              if (p.line1) p.line1.strokeWidth = showEyes ? 10 : 0;
              if (p.line2) p.line2.strokeWidth = showEyes ? 10 : 0;
            }
            p.line2 && p.line2.set({ x1: left, y1: top });
            p.line3 && p.line3.set({ x1: left, y1: top });
            p.line4 && p.line4.set({ x1: left, y1: top });
            p.line5 && p.line5.set({ x1: left, y1: top });
          }
        } else {
          const aCoords = target.aCoords;
          const center = {
            x: (aCoords.tl.x + aCoords.br.x) / 2,
            y: (aCoords.tl.y + aCoords.br.y) / 2,
          };
          const rad = (target.angle * Math.PI) / 180;
          const sin = Math.sin(rad);
          const cos = Math.cos(rad);

          for (const item of target._objects) {
            let p = item;
            const p_top = p.top * target.scaleY * flipY;
            const p_left = p.left * target.scaleX * flipX;
            const left = center.x + p_left * cos - p_top * sin;
            const top = center.y + p_left * sin + p_top * cos;
            p["_top"] = top;
            p["_left"] = left;
            if (p["id"] === 0) {
              p.line1 && p.line1.set({ x1: left, y1: top });
            } else {
              p.line1 && p.line1.set({ x2: left, y2: top });
            }
            if (p["id"] === 14 || p["id"] === 15) {
              p.radius = showEyes ? 5 : 0.3;
              if (p.line1) p.line1.strokeWidth = showEyes ? 10 : 0;
              if (p.line2) p.line2.strokeWidth = showEyes ? 10 : 0;
            }
            p.line2 && p.line2.set({ x1: left, y1: top });
            p.line3 && p.line3.set({ x1: left, y1: top });
            p.line4 && p.line4.set({ x1: left, y1: top });
            p.line5 && p.line5.set({ x1: left, y1: top });
          }
        }
      } else {
        var p = target;
        if (p["id"] === 0) {
          p.line1 && p.line1.set({ x1: p.left, y1: p.top });
        } else {
          p.line1 && p.line1.set({ x2: p.left, y2: p.top });
        }
        p.line2 && p.line2.set({ x1: p.left, y1: p.top });
        p.line3 && p.line3.set({ x1: p.left, y1: p.top });
        p.line4 && p.line4.set({ x1: p.left, y1: p.top });
        p.line5 && p.line5.set({ x1: p.left, y1: p.top });
      }
      this.canvas.renderAll();
    };

    this.canvas.on("object:moving", (e) => {
      updateLines(e.target);
    });

    this.canvas.on("object:scaling", (e) => {
      updateLines(e.target);
      this.canvas.renderAll();
    });

    this.canvas.on("object:rotating", (e) => {
      updateLines(e.target);
      this.canvas.renderAll();
    });

    this.canvas.on("object:modified", () => {
      console.log('object:modified取消的事件')
      if (
        this.lockMode ||
        (this.canvas.getActiveObject()&&this.canvas.getActiveObject().type == "activeSelection")
      )
        return;
      
      this.changeIndexPose()
      this.undo_history.push({'groups':JSON.parse(JSON.stringify(this.groups)),
            'hands':JSON.parse(JSON.stringify(this.hands)),'index':this.history_index});
      this.redo_history.length = 0;
      this.history_change = true;
    });

    this.canvas.on("selection:cleared", (e) => {
      if (this.lockMode)
          return;
      
      if(e?.deselected?.length>1||(e?.deselected?.length==1&&e?.deselected[0].itype=="hand")){
        let json=this.getJSON();
        if (json["keypoints"].length>0&&json["keypoints"].length >1) {
            this.changeIndexPose()
            this.undo_history.push({'groups':JSON.parse(JSON.stringify(this.groups)),
            'hands':JSON.parse(JSON.stringify(this.hands)),'index':this.history_index});
            this.redo_history.length = 0;
            this.history_change = true;
        }
        
      }
      console.log('selection:cleared取消的事件')
    });

    if (!LS_Poses[this.node.name].undo_history.length) {
      this.groups=[]
      this.hands=[]
      this.addPose();
      this.undo_history.push({'groups':JSON.parse(JSON.stringify(this.groups)),
      'hands':JSON.parse(JSON.stringify(this.hands)),
      'index':this.history_index});
    }
    return this.canvas;
  }

  undo() {
    if (this.undo_history.length > 0) {
      this.lockMode = true;
      if (this.undo_history.length > 1)
        this.redo_history.push(this.undo_history.pop());

      const content = this.undo_history[this.undo_history.length - 1];
      this.loadPreset(JSON.parse(JSON.stringify(content)));
      this.canvas.renderAll();
      this.lockMode = false;
      this.history_change = true;
    }
  }

  redo() {
    if (this.redo_history.length > 0) {
      this.lockMode = true;
      const content = this.redo_history.pop();
      this.undo_history.push(JSON.parse(JSON.stringify(content)));
      this.loadPreset(content);
      this.canvas.renderAll();
      this.lockMode = false;
      this.history_change = true;
    }
  }

  resetCanvas() {
    this.canvas.clear();
    this.canvas.backgroundColor = "#000";
    this.groups=[]
    this.addPose();
    this.undo_history.push({'groups':JSON.parse(JSON.stringify(this.groups)),
    'hands':JSON.parse(JSON.stringify(this.hands)),
    'index':this.history_index});
  }

  updateHistoryData() {
    if (this.history_change) {
      LS_Poses[this.node.name].undo_history = this.undo_history;
      LS_Poses[this.node.name].redo_history = this.redo_history;
      LS_Save();
      this.history_change = false;
    }
  }

  getHands(){ //获取手势
    let thi=this;
    const addHandsBtn = async () => {
      try {
        const resp = await api.fetchApi(`/lam/getHeads`);
        if (resp.status === 200) {
          const data = await resp.json();
          console.log(data)
          let rightButtons = document.createElement("div");
          rightButtons.className = "panelRightButtons comfy-menu-btns";
          for(let i=0;i<data.length;i++){
            var img = document.createElement('img');
            img.src = `/lam/getImage?type=hands&&name=${data[i]}`;
            img.alt = data[i];
            img.style.width = "40px";
            img.style.height = "40px";
            img.addEventListener("dragend", (e) =>  {
              let name=e.target.alt;
              let x=e.x;
              let y=e.y;
              let width=thi.canvas.width;
              let height=thi.canvas.height;
              let oWidth=thi.canvas.upperCanvasEl.parentElement.offsetWidth
              let oHeight=thi.canvas.upperCanvasEl.parentElement.offsetHeight
              let left=thi.canvas.upperCanvasEl.parentElement.offsetLeft
              let top=thi.canvas.upperCanvasEl.parentElement.offsetTop
              x=(x-left)/oWidth*width
              y=(y-top)/oHeight*height
              thi.addHand({name:name,l:x,t:y})
            });
            rightButtons.appendChild(img);
          }
          thi.canvas.wrapperEl.appendChild(rightButtons);
        } else {
          alert(resp.status + " - " + resp.statusText);
        }
      } catch (error) {
        console.error(error);
      }
    };
    addHandsBtn();
  }

  getImageOpse(image){ //上传图片识别骨骼姿态
    let thi=this;
    // 创建一个自定义的Loading控件
    var loading = (function() {
      if(!thi.canvas.wrapperEl.loadingDiv){
        var loadingDiv = document.createElement('div');
        loadingDiv.style.position = 'absolute';
        loadingDiv.style.left = '0';
        loadingDiv.style.top = '0';
        loadingDiv.style.right = '0';
        loadingDiv.style.bottom = '0';
        loadingDiv.style.background = 'rgba(255, 255, 255, 0.5)';
        loadingDiv.style.display = 'flex';
        loadingDiv.style.justifyContent = 'center';
        loadingDiv.style.alignItems = 'center';
        loadingDiv.style.zIndex = '100';
        loadingDiv.style.textAlign = 'center';
        loadingDiv.style.paddingTop = thi.canvas.height/2+'px';
        var loadingText = document.createElement('p');
        loadingText.textContent = '图片识别中...';
        loadingDiv.appendChild(loadingText);
      
        thi.canvas.wrapperEl.appendChild(loadingDiv);
        thi.canvas.wrapperEl.loadingDiv = loadingDiv;
      }
      return {
        show: function() {
          thi.canvas.wrapperEl.loadingDiv.style.display = 'block';
        },
        hide: function() {
          thi.canvas.wrapperEl.loadingDiv.style.display = 'none';
        }
      };
    })();
    // 在执行某些异步操作前显示Loading
    loading.show();
    
    const uploadFile = async (blobFile) => {
      try {
        const resp = await fetch("/lam/getImagePose", {
          method: "POST",
          body: blobFile,
        });
        if (resp.status === 200) {
          const data = await resp.json();
          console.log(data)
          if(data.groups.length<=0){
            alert('未识别到姿态骨骼');
            // 操作完成后隐藏Loading
            loading.hide();
            return ;
          }
          for(let i = 0; i < data.groups.length; i++){
            this.groups.push(data.groups[i]);
            this.subsets.push(data.subsets[i]);
            this.hands.push([]);
          }

          this.node.widgets[this.index].value = this.groups.length-1;
          this.node.widgets[this.index].options['max']=this.groups.length-1;
          this.node.setDirtyCanvas(true);
          this.setIndexPose(this.groups.length-1,false)
          this.updateHistoryData();
          // 操作完成后隐藏Loading
          loading.hide();
        } else {
          alert(resp.status + " - " + resp.statusText);
          loading.hide();
        }
      } catch (error) {
        console.error(error);
        loading.hide();
      }
    };
    let formData = new FormData();
    formData.append("image", image, image.name);
    uploadFile(formData);
  }

  

  getJSON() {
    const json = {
      keypoints: this.canvas
        .getObjects()
        .filter((item) => {
          if (item.type === "circle") return item;
        })
        .map((item) => {
          return [Math.round(item.left), Math.round(item.top)];
        }),
      hands:this.canvas
      .getObjects()
      .filter((item) => {
        if (item.type === "image" && item.itype === "hand" && item.selectable ) return item;
      })
      .map((item) => {
        let obj=item.getCenterPoint();
        return Object.assign(obj,{left:item.left,top:item.top,
            scaleX:item.scaleX,scaleY:item.scaleY,
            flipX:item.flipX,flipY:item.flipY,
            name:item.name,angle:item.angle
        });
      }),

    };

    return json;
  }

  loadPreset(obj) {
    this.groups=obj['groups']
    let index=obj['index']
    this.node.widgets[this.index].value=index;
    this.node.widgets[this.index].options['max']=this.groups.length;
    this.node.setDirtyCanvas(true);
    this.setIndexPose(index,false)
  }
}

// Create OpenPose widget
function createOpenPose(node, inputName, inputData, app) {
  node.name = inputName;
  const widget = {
    type: "openpose",
    name: `w${inputName}`,
    value:[],

    draw: function (ctx, _, widgetWidth, y, widgetHeight) {
      const margin = 10,
        visible = app.canvas.ds.scale > 0.5 && this.type === "openpose",
        clientRectBound = ctx.canvas.getBoundingClientRect(),
        transform = new DOMMatrix()
          .scaleSelf(
            clientRectBound.width / ctx.canvas.width,
            clientRectBound.height / ctx.canvas.height
          )
          .multiplySelf(ctx.getTransform())
          .translateSelf(margin, margin + y),
        w = (widgetWidth - margin * 2 - 3) * transform.a;

      Object.assign(this.openpose.style, {
        left: `${transform.a * margin + transform.e}px`,
        top: `${transform.d + transform.f}px`,
        width: w + "px",
        height: w + "px",
        position: "absolute",
        zIndex: app.graph._nodes.indexOf(node),
      });

      Object.assign(this.openpose.children[0].style, {
        width: w + "px",
        height: w + "px",
      });

      Object.assign(this.openpose.children[1].style, {
        width: w + "px",
        height: w + "px",
      });

      Array.from(this.openpose.children[2].children).forEach((element) => {
        Object.assign(element.style, {
          width: `${28.0 * transform.a}px`,
          height: `${22.0 * transform.d}px`,
          fontSize: `${transform.d * 10.0}px`,
        });
        element.hidden = !visible;
      });
    },
  };

  // Fabric canvas
  let canvasOpenPose = document.createElement("canvas");
  node.openPose = new OpenPose(node, canvasOpenPose);
  node.openPose.canvas.setWidth(512);
  node.openPose.canvas.setHeight(512);
  
  let index = node.widgets[node.widgets.findIndex(obj => obj.name === 'index')];
  let width = node.widgets[node.widgets.findIndex(obj => obj.name === 'width')];
  let height = node.widgets[node.widgets.findIndex(obj => obj.name === 'height')];
  index.callback = function (v) {
    node.openPose.setIndexPose(v)
  }
  width.callback = function (v) {
    node.openPose.canvas.setWidth(v);
  }
  height.callback = function (v) {
    node.openPose.canvas.setHeight(v);
  }

  widget.openpose = node.openPose.canvas.wrapperEl;
  widget.parent = node;
  Object.defineProperty(widget, "value", {
    set: (x) => {
        node.openPose.canvas.setWidth(width.value);
        node.openPose.canvas.setHeight(height.value);
        let data=JSON.parse(x)
        node.openPose.groups=data.groups;
        node.openPose.hands=data.hands;
        node.openPose.subsets=data.subsets;
        index.value =0;
        index.options['max']=this.openPose.groups.length-1;
        node.openPose.setIndexPose(0,false)
    },
    get: () => {
      return JSON.stringify({
        groups: this.openPose.groups,
        subsets: this.openPose.subsets,
        hands: this.openPose.hands,
      });
    }
  });

  // Create elements undo, redo, clear history
  let panelButtons = document.createElement("div"),
    addButton = document.createElement("button"),
    delButton = document.createElement("button"),
    resButton = document.createElement("button"),
    refButton = document.createElement("button"),
    undoButton = document.createElement("button"),
    redoButton = document.createElement("button"),
    fliplfButton = document.createElement("button"),
    fliptdButton = document.createElement("button"),
    historyClearButton = document.createElement("button");

  panelButtons.className = "panelButtons comfy-menu-btns";
  addButton.textContent = "+";
  delButton.textContent = "-";
  resButton.textContent = "⟲";
  refButton.textContent = "img";
  undoButton.textContent = "<-";
  redoButton.textContent = "->";
  fliplfButton.textContent = "↔";
  fliptdButton.textContent = "↕";
  historyClearButton.textContent = "✖";
  addButton.title = "添加骨骼";
  delButton.title = "删除骨骼";
  resButton.title = "重置";
  refButton.title = "添加人物示例";
  undoButton.title = "上一步";
  redoButton.title = "下一步";
  fliplfButton.title = "左右翻转";
  fliptdButton.title = "上下翻转";
  historyClearButton.title = "清除历史";

  addButton.addEventListener("click", () => node.openPose.addPose());
  delButton.addEventListener("click", () => node.openPose.delIndexPose());
  resButton.addEventListener("click", () => node.openPose.resetCanvas());
  refButton.addEventListener("click", () => node.openPose.addPoseDemoInput.click());
  undoButton.addEventListener("click", () => node.openPose.undo());
  redoButton.addEventListener("click", () => node.openPose.redo());
  fliplfButton.addEventListener("click", () => node.openPose.fliplf());
  fliptdButton.addEventListener("click", () => node.openPose.fliptd());
  historyClearButton.addEventListener("click", () => {
    if (confirm(`删除节点"${node.name}"的所有姿势历史记录 ?`)) {
      node.openPose.undo_history = [];
      node.openPose.redo_history = [];
      if(node.openPose.groups.length>0){
        node.openPose.undo_history.push({'groups':JSON.parse(JSON.stringify(node.openPose.groups)),
        'hands':JSON.parse(JSON.stringify(node.openPose.hands)),
        'index':node.openPose.history_index});
      }
      node.openPose.groups=[]
      node.openPose.addPose();
      node.openPose.history_change = true;
      node.openPose.updateHistoryData();
    }
  });
  panelButtons.appendChild(addButton);
  panelButtons.appendChild(delButton);
  panelButtons.appendChild(resButton);
  panelButtons.appendChild(refButton);
  panelButtons.appendChild(undoButton);
  panelButtons.appendChild(redoButton);
  panelButtons.appendChild(fliplfButton);
  panelButtons.appendChild(fliptdButton);
  panelButtons.appendChild(historyClearButton);
  node.openPose.canvas.wrapperEl.appendChild(panelButtons);

  document.body.appendChild(widget.openpose);
  document.addEventListener('keydown', function(event) {
      // console.log('按下了键:', event.key);
      // console.log('键的码值:', event.keyCode);
      // console.log('事件详情:', event);
      if(event.key=='Delete'||event.key=='Backspace'){
        let activeObject=node.openPose.canvas.getActiveObject()
        if (activeObject) {
          node.openPose.canvas.remove(activeObject);
        }
        node.openPose.setIndexPose(node.openPose.history_index,true)
      }
  });
  
  node.openPose.getHands()
  node.addWidget("button", "Test", "Test", () => {
    //node.openPose.addHand()
    debugger;
  });
  
  // Add customWidget to node
  node.addCustomWidget(widget);

  node.onRemoved = () => {
    if (Object.hasOwn(LS_Poses, node.name)) {
      delete LS_Poses[node.name];
      LS_Save();
    }

    // When removing this node we need to remove the input from the DOM
    for (let y in node.widgets) {
      if (node.widgets[y].openpose) {
        node.widgets[y].openpose.remove();
      }
    }
  };

  widget.onRemove = () => {
    widget.openpose?.remove();
  };

  app.canvas.onDrawBackground = function () {
    // Draw node isnt fired once the node is off the screen
    // if it goes off screen quickly, the input may not be removed
    // this shifts it off screen so it can be moved back if the node is visible.
    for (let n in app.graph._nodes) {
      n = graph._nodes[n];
      for (let w in n.widgets) {
        let wid = n.widgets[w];
        if (Object.hasOwn(wid, "openpose")) {
          wid.openpose.style.left = -8000 + "px";
          wid.openpose.style.position = "absolute";
        }
      }
    }
  };
  return { widget: widget };
}

window.LS_Poses = {};
function LS_Save() {
  ///console.log("Save:", LS_Poses);
  localStorage.setItem("ComfyUI_Poses", JSON.stringify(LS_Poses));
}

app.registerExtension({
  name: "LAM.OpenPoseEditorPlus",
  async init(app) {
    // Any initial setup to run as soon as the page loads
    let style = document.createElement("style");
    style.innerText = `
    .panelButtons{
      position: absolute;
      padding: 4px;
      display: flex;
      gap: 4px;
      flex-direction: column;
      width: fit-content;
    }
    .panelButtons button:last-child{
      border-color: var(--error-text);
      color: var(--error-text) !important;
    }
    .panelRightButtons{
      right: 0px;
      overflow: auto;
      height: 95%;
      position: absolute;
      padding: 4px;
      display: flex;
      gap: 4px;
      flex-direction: column;
      width: fit-content;
    }
    .panelRightButtons button:last-child{
      border-color: var(--error-text);
      color: var(--error-text) !important;
    }
    
    `;
    document.head.appendChild(style);
  },
  async setup(app) {
    let openPoseNode = app.graph._nodes.filter((wi) => wi.type == "LAM.OpenPoseEditorPlus");

    if (openPoseNode.length) {
      openPoseNode.map((n) => {
        console.log(`Setup PoseNode: ${n.name}`);
        let widgetImage = n.widgets.find((w) => w.name == "image");
        if (widgetImage && Object.hasOwn(LS_Poses, n.name)) {
          let pose_ls = LS_Poses[n.name].undo_history;
          if(pose_ls.length>0){
            n.openPose.loadPreset(pose_ls[pose_ls.length - 1]);
          }else{
            n.openPose.groups=[]
            n.openPose.addPose();
            n.openPose.undo_history.push({'groups':JSON.parse(JSON.stringify(n.openPose.groups)),
            'hands':JSON.parse(JSON.stringify(n.openPose.hands)),
            'index':n.openPose.history_index});
          }
        }
      });
    }
  },
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "LAM.OpenPoseEditorPlus") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const r = onNodeCreated
          ? onNodeCreated.apply(this, arguments)
          : undefined;
        let openPoseNode = app.graph._nodes.filter((wi) => wi.type == "LAM.OpenPoseEditorPlus");
        let nodeName = `Pose_${openPoseNode.length}`;
        let nodeNamePNG = `${nodeName}`;

        console.log(`Create PoseNode: ${nodeName}`);
        LS_Poses =
          localStorage.getItem("ComfyUI_Poses") &&
          JSON.parse(localStorage.getItem("ComfyUI_Poses"));
        if (!LS_Poses) {
          localStorage.setItem("ComfyUI_Poses", JSON.stringify({}));
          LS_Poses = JSON.parse(localStorage.getItem("ComfyUI_Poses"));
        }

        if (!Object.hasOwn(LS_Poses, nodeNamePNG)) {
          LS_Poses[nodeNamePNG] = {
            undo_history: [],
            redo_history: [],
          };
          LS_Save();
        }

        createOpenPose.apply(this, [this, nodeNamePNG, {}, app]);
        

        this.setSize([750, 900]);

        return r;
      };
    }
  },
});
