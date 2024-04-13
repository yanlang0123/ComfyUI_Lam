import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";
import {CUSTOM_INT,CUSTOM_COMBO, recursiveLinkUpstream, transformFunc, swapInputs,swapOutputs, renameNodeInputs,renameNodeOutputs, removeNodeInputs,removeNodeOutputs, getDrawColor, computeCanvasSize} from "./utils.js"



function addMultiControlNetApplySelectCanvas(node, app) {
const widget = {
    type: "customLamCanvas",
    name: "MultiControlNetApply-Canvas",
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
    name: "Comfy.lam.MultiControlNetApply",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        
        var names=["MultiControlNetApply"]
        if (names.indexOf(nodeData.name)>=0) {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                let control_net_name = this.widgets[this.widgets.findIndex(obj => obj.name === 'control_net_name')];
                let netNames=control_net_name.options.values;
                this.setProperty("values", [[netNames[0],1.0],[netNames[0],1.0]])
                this.index=2
				this.originalsize=1 
                this.inputType="IMAGE"
                this.inputPrefix="image"
                this.outputPrefix=""
                this.selected=false;
                
                control_net_name.callback = function (v,_, node) {
                    node.properties["values"][node.widgets[node.index].value][0] = this.value
                }
                CUSTOM_INT(this, "strength", 1.0,function (v, _, node) {node.properties["values"][node.widgets[node.index].value][1] = this.value},{"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01,precision: 2 })
                CUSTOM_INT(
					this,
					"index",
					0,
					function (v, _, node) {
						let values = node.properties["values"]
						node.widgets[node.index-2].value = values[v][0]
						node.widgets[node.index-1].value = values[v][1]
					},
					{ step: 10, max: 1 }

				)
				//CUSTOM_COMBO(this, "control_net_name", netNames[0],function (v, _, node) {node.properties["values"][node.widgets[node.index].value][0] = this.value},{values:netNames}).widget;
                //this.widgets.reverse();
                addMultiControlNetApplySelectCanvas(this, app)
                
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
                                this.properties["values"].splice(index, 0, [netNames[0],1.0])
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
                                this.properties["values"].splice(index, 0, [netNames[0],1.0])
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
		if (node.type === "MultiControlNetApply") {
			node.widgets[node.index].options["max"] = node.properties["values"].length-1
		}
	},
});