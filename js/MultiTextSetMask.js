import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";
import {CUSTOM_INT,CUSTOM_COMBO, recursiveLinkUpstream, transformFunc, swapInputs,swapOutputs, renameNodeInputs,renameNodeOutputs, removeNodeInputs,removeNodeOutputs, getDrawColor, computeCanvasSize} from "./utils.js"



function addMultiTextSetMaskSelectCanvas(node, app) {
const widget = {
    type: "customLamCanvas",
    name: "MultiTextSetMask-Canvas",
    get value() {
        return this.canvas.value;
    },
    set value(x) {
        this.canvas.value = x;
    },
    draw: function (ctx, node, widgetWidth, widgetY) {

        const values = node.properties["values"]
        const index = Math.round(node.widgets[node.index].value)

        const selectedColor = getDrawColor(index/values.length, "FF")
        ctx.fillStyle = selectedColor
        ctx.beginPath();

        ctx.arc(LiteGraph.NODE_SLOT_HEIGHT*0.5, LiteGraph.NODE_SLOT_HEIGHT*(index+node.originalsize + 0.5)+4, 4, 0, Math.PI * 2);
        ctx.fill();

        ctx.lineWidth = 1;
        ctx.strokeStyle = "white";
        ctx.stroke();

        if (node.selected) {
            const connectedNodes = recursiveLinkUpstream(node, node.inputs[index+node.originalsize].type, 0, index+node.originalsize)
            
            if (connectedNodes.length !== 0) {
                for (let [node_ID, depth] of connectedNodes) {
                    let connectedNode = node.graph._nodes_by_id[node_ID]
                    if (connectedNode.type != node.type) {
                        const [x, y] = connectedNode.pos
                        const [w, h] = connectedNode.size
                        const offset = 5
                        const titleHeight = LiteGraph.NODE_TITLE_HEIGHT * (connectedNode.type === "Reroute"  ? 0 : 1)

                        ctx.strokeStyle = selectedColor
                        ctx.lineWidth = 5;
                        ctx.strokeRect(x-offset-node.pos[0], y-offset-node.pos[1]-titleHeight, w+offset*2, h+offset*2+titleHeight)
                    }
                }
            }
        }
    },
};

widget.canvas = document.createElement("canvas");
widget.canvas.className = "dave-custom-canvas";

widget.parent = node;
document.body.appendChild(widget.canvas);
node.addCustomWidget(widget);

return { minWidth: 200, minHeight: 200, widget }
}
// Displays input text on a node
app.registerExtension({
    name: "Comfy.lam.MultiTextSetMask",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        
        var names=["MultiTextSetMask","MultiTextSetArea","MultiTextSetGligen","MultiIPAdapterRegional"]
        if (names.indexOf(nodeData.name)>=0) {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                this.selected=false;
                this.defaultValue=null
                this.index=2
				this.originalsize=4 
                this.inputType="STRING"
                this.inputPrefix="text"
                this.outputPrefix=""
                if('MultiTextSetGligen'==nodeData.name){
                    this.originalsize=5 
                    this.defaultValue=1.0;
                }else if('MultiTextSetArea'==nodeData.name){
                    this.defaultValue=1.0;
                }else if('MultiTextSetMask'==nodeData.name){
                    this.defaultValue=[1.0,"default"];
                }else if('MultiIPAdapterRegional'==nodeData.name){
                    this.index=0
                    this.originalsize=1
                    this.inputType="IMAGE"
                    this.inputPrefix="image"
                    this.defaultValue=[1.0,"linear",0.0,1.0]
                }
                if(this.defaultValue){
                    this.setProperty("values", [this.defaultValue,this.defaultValue])
                }
                
                
                CUSTOM_INT(
					this,
					"index",
					0,
					function (v, _, node) {
						let values = node.properties["values"]
                        if(Array.isArray(values[v])){
                            for(let i=0;i<values[v].length;i++){
                                node.widgets[node.index+i+1].value =values[v][i]
                            }
                        }else{
                            node.widgets[node.index+1].value =values[v]
                        }
					},
					{ step: 10, max: 1 }

				)
                if('MultiTextSetMask'==nodeData.name || 'MultiTextSetArea'==nodeData.name){
                    CUSTOM_INT(this, "strength", 1.0,function (v, _, node) {node.properties["values"][node.widgets[node.index].value][0] = this.value},{"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01,precision: 2 })
                }
                if('MultiTextSetMask'==nodeData.name){
                    CUSTOM_COMBO(this, "set_cond_area", "default",function (v, _, node) {node.properties["values"][node.widgets[node.index].value][1] = this.value},{values:["default", "mask bounds"]}).widget;
                }
                if('MultiIPAdapterRegional'==nodeData.name){
                    var WEIGHT_TYPES = ["linear", "ease in", "ease out", 'ease in-out', 'reverse in-out', 'weak input', 'weak output', 'weak middle', 'strong middle', 'style transfer', 'composition', 'strong style transfer']
                    CUSTOM_INT(this, "image_weight", 1.0,function (v, _, node) {node.properties["values"][node.widgets[node.index].value][0] = this.value},{"default": 1.0, "min": -1.0, "max": 3.0, "step": 0.05,precision: 2 })
                    CUSTOM_COMBO(this, "weight_type", WEIGHT_TYPES[0],function (v, _, node) {node.properties["values"][node.widgets[node.index].value][1] = this.value},{values:WEIGHT_TYPES}).widget;
                    CUSTOM_INT(this, "start_at", 1.0,function (v, _, node) {node.properties["values"][node.widgets[node.index].value][2] = this.value},{"default": 1.0, "min": -1.0, "max": 3.0, "step": 0.05,precision: 2 })
                    CUSTOM_INT(this, "end_at", 1.0,function (v, _, node) {node.properties["values"][node.widgets[node.index].value][3] = this.value},{"default": 1.0, "min": -1.0, "max": 3.0, "step": 0.05,precision: 2 })
                }
                addMultiTextSetMaskSelectCanvas(this, app)
                
                this.getExtraMenuOptions = function(_, options) {
                    options.unshift(
                        {
                            content: `最前插入参 /\\`,
                            callback: () => {
                                this.addInput(this.inputPrefix, this.inputType)

                                const inputLenth = this.inputs.length-1-this.originalsize
                                const index = 0+this.originalsize

                                for (let i = inputLenth; i > index; i--) {
                                    swapInputs(this, i, i-1)
                                }
                                renameNodeInputs(this, this.inputPrefix,this.originalsize)
                                this.properties["values"].splice(index, 0, this.defaultValue)
								this.widgets[this.index].options.max = inputLenth
                                this.setDirtyCanvas(true);
                            },
                        },
                        {
                            content: `最后插入参 \\/`,
                            callback: () => {
                                this.addInput(this.inputPrefix, this.inputType)

                                const inputLenth = this.inputs.length-1-this.originalsize
                                const index = this.widgets[this.index].value+this.originalsize

                                renameNodeInputs(this, this.inputPrefix,this.originalsize)
                                this.properties["values"].splice(index, 0, this.defaultValue)
								this.widgets[this.index].options.max = inputLenth
                                this.setDirtyCanvas(true);
                            },
                        },
                        {
                            content: "删除全部未连接的入参框",
                            callback: () => {
                                let indexesToRemove = []

                                for (let i = 0; i < this.inputs.length; i++) {
                                    if (!this.inputs[i].link&&i>=this.originalsize) {
                                        indexesToRemove.push(i)
                                    }
                                }
                                
                                removeNodeInputs(this, indexesToRemove,this.originalsize)
                                renameNodeInputs(this, this.inputPrefix,this.originalsize)
                            },
                        }
                    );
                }

            
                this.onSelected = function () {
                    this.selected = true
                }
                this.onDeselected = function () {
                    this.selected = false
                }

                return r;
            }
            
        }
    },
    loadedGraphNode(node, _) {
        var names=["MultiTextSetMask","MultiTextSetArea","MultiTextSetGligen","MultiIPAdapterRegional"]
		if (names.indexOf(node.type)>=0) {
			node.widgets[node.index].options["max"] = node.properties["values"].length-1
		}
	},
});