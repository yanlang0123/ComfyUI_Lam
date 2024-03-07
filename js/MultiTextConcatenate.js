import { app } from "/scripts/app.js";
import {CUSTOM_INT, recursiveLinkUpstream, transformFunc, swapInputs, renameNodeInputs, removeNodeInputs, getDrawColor, computeCanvasSize} from "./utils.js"

// Displays input text on a node

app.registerExtension({
    name: "Comfy.lam.MultiTextConcatenate",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        var names=["MultiTextConcatenate",'MultiTextSelelct']
        if (names.indexOf(nodeData.name)>=0) {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
				this.originalsize=0 
                if('MultiTextSelelct'==nodeData.name){
                    this.originalsize=1
                }
                this.getExtraMenuOptions = function(_, options) {
                    options.unshift(
                        {
                            content: `最前插入 /\\`,
                            callback: () => {
                                this.addInput("text", "STRING")
                                
                                const inputLenth = this.inputs.length-1
                                const index = 0+this.originalsize

                                for (let i = inputLenth; i > index; i--) {
                                    swapInputs(this, i, i-1)
                                }
                                renameNodeInputs(this, "text",this.originalsize)
                                this.setDirtyCanvas(true);
                            },
                        },
                        {
                            content: `最后插入 \\/`,
                            callback: () => {
                                this.addInput("text", "STRING")
                                renameNodeInputs(this, "text",this.originalsize)
                                this.setDirtyCanvas(true);
                            },
                        },
                        {
                            content: "删除全部未连接的框",
                            callback: () => {
                                let indexesToRemove = []

                                for (let i = 0; i < this.inputs.length; i++) {
                                    if (!this.inputs[i].link&&i>=this.originalsize) {
                                        indexesToRemove.push(i)
                                    }
                                }
                                
                                removeNodeInputs(this, indexesToRemove,this.originalsize)
                                renameNodeInputs(this, "text",this.originalsize)
                            },
                        },
                    );
                }

                this.onRemoved = function () {
                    // When removing this node we need to remove the input from the DOM
                    for (let y in this.widgets) {
                        if (this.widgets[y].canvas) {
                            this.widgets[y].canvas.remove();
                        }
                    }
                };
            
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
});