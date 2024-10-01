import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";
import { $el } from "../../../scripts/ui.js";
import {CUSTOM_INT, recursiveLinkUpstream, transformFunc, swapInputs,swapOutputs, renameNodeInputs,renameNodeOutputs, removeNodeInputs,removeNodeOutputs, getDrawColor, computeCanvasSize} from "./utils.js"

app.registerExtension({
    name: "Comfy.lam.MultiTextConcatenate",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        var showNames=["IfInnerExecute",'MultiIntFormula','MultiParamFormula','ForInnerEnd','DoWhileEnd',"LamSwitcherCase"]
        if (showNames.indexOf(nodeData.name)>=0) {
            const onDrawForeground = nodeType.prototype.onDrawForeground;
            let oldText=''
            nodeType.prototype.onDrawForeground = function (ctx) {
                try {
                    const r = onDrawForeground?.apply?.(this, arguments);
                    const v = app.nodeOutputs?.[this.id + ""];
                    if (!this.flags.collapsed && v) {
                        let text=''
                        if(['ForInnerEnd','DoWhileEnd'].indexOf(nodeData.name)>=0){
                            if(v.value[0].indexOf('DOWHILE')!=-1){
                                text=v.value[0].split('DOWHILE')[1]
                                oldText=text
                            }else{
                                text=oldText
                            }
                        }else{
                            text = v.value[0] + "";
                        }
                        ctx.save();
                        ctx.font = "bold 12px sans-serif";
                        ctx.fillStyle = "dodgerblue";
                        const sz = ctx.measureText(text);
                        ctx.fillText(text, this.size[0]/2 - (sz.width + 5)/2, LiteGraph.NODE_SLOT_HEIGHT * 1);
                        ctx.restore();
                    }
                    return r;
                } catch(e) {
                    console.log(e)
                }
                return 

            };
        }
        var names=["MultiTextConcatenate",'MultiTextSelelct',"MultiIntFormula","MultiParamFormula","LamSwitcherCase"]
        if (names.indexOf(nodeData.name)>=0) {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
				this.originalsize=0 
                this.inputType="STRING"
                this.inputPrefix="text"
                this.outputPrefix=""
                if('MultiTextSelelct'==nodeData.name){
                    this.originalsize=2
                }
                if('MultiIntFormula'==nodeData.name){
                    this.inputType="INT,FLOAT"
                    this.inputPrefix="n"
                }
                if('MultiParamFormula'==nodeData.name){
                    this.inputType="*"
                    this.inputPrefix="p"
                    this.outputPrefix="r"
                }
                if('LamSwitcherCase'==nodeData.name){
                    this.originalsize=1
                    this.inputType="*"
                    this.inputPrefix="case"
                }
                function changCustomtext(){
                    //this.setSize( this.computeSize() );
                }
                this.widgets?.forEach(function(widget) {
                    if(widget.type!="customtext"){
                        return ;
                    }
                    const draw = widget.draw;
                    widget.draw = function (ctx,parentNode, widgetWidth, y, widgetHeight) {
                        draw?.apply(this, arguments);
                        if (this.inputEl.hidden) return;
                        const  margin = 20,
                        clientRectBound = ctx.canvas.getBoundingClientRect(),
                        transform = new DOMMatrix()
                        .scaleSelf(
                            clientRectBound.width / ctx.canvas.width,
                            clientRectBound.height / ctx.canvas.height
                        )
                        .multiplySelf(ctx.getTransform())
                        .translateSelf(margin, margin + y),
                        w = (widgetWidth - (margin * 4) ) ;
                        let maxIoputSize=Math.max(...[parentNode.inputs.length,parentNode.outputs.length])
                        Object.assign(this.inputEl.style, {
                            left: `${transform.a * margin + transform.e}px`,
                            top: `${transform.d + transform.f-10}px`,
                            width: `${w}px`,
                        });
                    }
                });
                this.getExtraMenuOptions = function(_, options) {
                    if(this.outputPrefix){
                        options.unshift(
                            {
                                content: `最前插入参 /\\`,
                                callback: () => {
                                    this.addInput(this.inputPrefix, this.inputType)
                                    const inputLenth = this.inputs.length-1
                                    const index = 0+this.originalsize
    
                                    for (let i = inputLenth; i > index; i--) {
                                        swapInputs(this, i, i-1)
                                    }
                                    renameNodeInputs(this, this.inputPrefix,this.originalsize)
                                    this.setDirtyCanvas(true);
                                    changCustomtext.call(this)
                                },
                            },
                            {
                                content: `最后插入参 \\/`,
                                callback: () => {
                                    this.addInput(this.inputPrefix, this.inputType)
                                    renameNodeInputs(this, this.inputPrefix,this.originalsize)
                                    this.setDirtyCanvas(true);
                                    changCustomtext.call(this)
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
                                    changCustomtext.call(this)
                                },
                            },
                            {
                                content: `最前插出参 /\\`,
                                callback: () => {
                                    this.addOutput(this.outputPrefix, this.inputType)
                                    const inputLenth = this.outputs.length-1
                                    const index = 0+this.originalsize
    
                                    for (let i = inputLenth; i > index; i--) {
                                        swapOutputs(this, i, i-1)
                                    }
                                    renameNodeOutputs(this, this.outputPrefix,this.originalsize)
                                    this.setDirtyCanvas(true);
                                    changCustomtext.call(this)
                                },
                            },
                            {
                                content: `最后插出参 \\/`,
                                callback: () => {
                                    this.addOutput(this.outputPrefix, this.inputType)
                                    renameNodeOutputs(this, this.outputPrefix,this.originalsize)
                                    this.setDirtyCanvas(true);
                                    changCustomtext.call(this)
                                },
                            },
                            {
                                content: "删除全部未连接的出参框",
                                callback: () => {
                                    let indexesToRemove = []
                                    for (let i = 0; i < this.outputs.length; i++) {
                                        if ((!this.outputs[i].links||this.outputs[i].links.length==0)&&i>=this.originalsize) {
                                            indexesToRemove.push(i)
                                        }
                                    }
                                    removeNodeOutputs(this, indexesToRemove,this.originalsize)
                                    renameNodeOutputs(this, this.outputPrefix,this.originalsize)
                                    changCustomtext.call(this)
                                },
                            }
                        );
                    }else{
                        options.unshift(
                            {
                                content: `最前插入参 /\\`,
                                callback: () => {
                                    this.addInput(this.inputPrefix, this.inputType)
                                    const inputLenth = this.inputs.length-1
                                    const index = 0+this.originalsize
    
                                    for (let i = inputLenth; i > index; i--) {
                                        swapInputs(this, i, i-1)
                                    }
                                    renameNodeInputs(this, this.inputPrefix,this.originalsize)
                                    this.setDirtyCanvas(true);
                                    changCustomtext.call(this)
                                },
                            },
                            {
                                content: `最后插入参 \\/`,
                                callback: () => {
                                    this.addInput(this.inputPrefix, this.inputType)
                                    renameNodeInputs(this, this.inputPrefix,this.originalsize)
                                    this.setDirtyCanvas(true);
                                    changCustomtext.call(this)
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
                                    changCustomtext.call(this)
                                },
                            }
                        );
                    }
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
});