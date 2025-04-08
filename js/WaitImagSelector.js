import { app } from "../../../../scripts/app.js";
import { api } from "../../../../scripts/api.js";
import { ComfyDialog, $el } from "../../../../scripts/ui.js";

import { restart_from_here } from "./image_chooser/prompt.js";
import { hud, FlowState } from "./image_chooser/state.js";
import { send_cancel, send_message, send_onstart, skip_next_restart_message } from "./image_chooser/messaging.js";
import { display_preview_images, additionalDrawBackground, click_is_in_image } from "./image_chooser/preview.js";


class chooserImageDialog extends ComfyDialog {

    constructor() {
		super();
        this.node = null
        this.select_index = []
        this.dialog_div = null
	}

    show(image,node){
        this.select_index = []
        this.node = node

        const images_div = image.map((img, index) => {
            const imgEl = $el('img', {
                src: img.src,
                onclick: _ => {
                    if(this.select_index.includes(index)){
                        this.select_index = this.select_index.filter(i => i !== index)
                        imgEl.classList.remove('selected')
                    } else {
                        this.select_index.push(index)
                        imgEl.classList.add('selected')
                    }
                    if (node.selecteds.has(index)) node.selecteds.delete(index);
                    else node.selecteds.add(index);
                }
            })
            return imgEl
        })
        super.show($el('div.easyuse-chooser-dialog',[
            $el('h5.easyuse-chooser-dialog-title', '选择图像继续'),
            $el('div.easyuse-chooser-dialog-images',images_div)
        ]))
    }
    createButtons() {
        const btns = super.createButtons();
        btns[0].onclick = _ => {
            if (FlowState.running()) { send_cancel();}
            super.close()
        }
        btns.unshift($el('button', {
            type: 'button',
            textContent: "选择已选图像",
            onclick: _ => {
                if (FlowState.paused()) {
                    send_message(this.node.id, [...this.node.selected, -1, ...this.node.anti_selected]);
                }
                if (FlowState.idle()) {
                    skip_next_restart_message();
                    restart_from_here(this.node.id).then(() => { send_message(this.node.id, [...this.node.selected, -1, ...this.node.anti_selected]); });
                }
                super.close()
            }
        }))
        return btns
    }

}

function progressButtonPressed() {
    const node = app.graph._nodes_by_id[this.node_id];
    if (node) {
        const selecteds = [...node.selecteds]
        if(selecteds?.length>0){
            node.setProperty('values',selecteds)
        }
        if (FlowState.paused()) {
            send_message(node.id, [...node.selecteds, -1, ...node.anti_selected]);
        }
        if (FlowState.idle()) {
            skip_next_restart_message();
            restart_from_here(node.id).then(() => { send_message(node.id, [...node.selecteds, -1, ...node.anti_selected]); });
        }
    }
}

function cancelButtonPressed() {

    if (FlowState.running()) { send_cancel();}
}

function enable_disabling(button) {
    Object.defineProperty(button, 'clicked', {
        get : function() { return this._clicked; },
        set : function(v) { this._clicked = (v && this.name!=''); }
    })
}

function disable_serialize(widget) {
    if (!widget.options) widget.options = {  };
    widget.options.serialize = false;
}

app.registerExtension({
    name:'comfy.WaitImagSelector',
    init() {
        window.addEventListener("beforeunload", send_cancel, true);
    },
    setup(app) {

        const draw = LGraphCanvas.prototype.draw;
        LGraphCanvas.prototype.draw = function(ctx, node, widgetWidth, widgetY) {
            if (hud.update()) {
                app.graph._nodes.forEach((node)=> { if (node.update) { node.update(); } })
            }
            draw.apply(this,arguments);
        }


        function easyuseImageChooser(event) {
            const {node,image,isKSampler} = display_preview_images(event);
            if(isKSampler) {
                const dialog = new chooserImageDialog();
                dialog.show(image,node)
            }
        }
        api.addEventListener("lam-wait-image-select", easyuseImageChooser);
        /*
        If a run is interrupted, send a cancel message (unless we're doing the cancelling, to avoid infinite loop)
        */
        const original_api_interrupt = api.interrupt;
        api.interrupt = function () {
            if (FlowState.paused() && !FlowState.cancelling) send_cancel();
            original_api_interrupt.apply(this, arguments);
        }

        /*
        At the start of execution
        */
        function on_execution_start(event) {
            if (send_onstart()) {
                app.graph._nodes.forEach((node)=> {
                    if (node.selecteds || node.anti_selected) {
                        node.selecteds.clear();
                        node.anti_selected.clear();
                        node.update();
                    }
                })
            }
        }
        api.addEventListener("execution_start", on_execution_start);
    },

    async nodeCreated(node, app) {

        if(node.comfyClass == 'WaitImagSelector'){
            node.setProperty('values',[])

            // node.selecteds=new Set()
            // node.anti_selected=new Set()

            /* A property defining the top of the image when there is just one */
            if(node?.imageIndex === undefined){
              Object.defineProperty(node, 'imageIndex', {
                    get : function() { return null; },
                    set: function (v) {
                        node.overIndex= v;
                        if(v!=null){
                            this.imageClicked(v);
                        }
                    },
                })
            }
            if(node?.imagey === undefined){
                Object.defineProperty(node, 'imagey', {
                    get : function() { return null; },
                    set: function (v) {return node.widgets[node.widgets.length-1].last_y+LiteGraph.NODE_WIDGET_HEIGHT;},
                })
            }
           

            node.send_button_widget = node.addWidget("button", "换一批", "", progressButtonPressed);
            enable_disabling(node.send_button_widget);
            disable_serialize(node.send_button_widget);

            let addCustomWidget= node.addCustomWidget;
            node.addCustomWidget = function(widget) {
                addCustomWidget.apply(this, arguments);
                const draw = widget.draw;
                widget.draw = function (ctx,parentNode, widgetWidth, y, widgetHeight) {
                    draw?.apply(this, arguments);
                    if(node?.imgs?.length>0){
                        additionalDrawBackground(node, ctx);
                    }
                }
            }
        }
    },

    beforeRegisterNodeDef(nodeType, nodeData, app) {
        if(nodeData?.name == 'WaitImagSelector'){

            // const onDrawBackground = nodeType.prototype.onDrawBackground;
            // nodeType.prototype.onDrawBackground = function(ctx) {
            //     onDrawBackground.apply(this, arguments);
            //     additionalDrawBackground(this, ctx);
            // }

            nodeType.prototype.imageClicked = function (imageIndex) {
                if (nodeType?.comfyClass==="WaitImagSelector") {
                    if (this.selecteds.has(imageIndex)){
                        this.selecteds.delete(imageIndex);
                    }else{
                        this.selecteds.add(imageIndex);
                    }
                    this.update();
                }
            }

            const update = nodeType.prototype.update;
            nodeType.prototype.update = function() {
                if (update) update.apply(this,arguments);
                if (this.send_button_widget) {
                    this.send_button_widget.node_id = this.id;
                    const selection = ( this.selecteds ? this.selecteds.size : 0 ) + ( this.anti_selected ? this.anti_selected.size : 0 )
                    const maxlength = this.imgs?.length || 0;
                    if (FlowState.paused_here(this.id) && selection>0) {
                        this.send_button_widget.label = (selection>0) ? "确认选择 (" + selection + '/' + maxlength  +")" : "确认选择";
                    }else{
                        this.send_button_widget.label = "换一批";
                    }
                }
                this.setDirtyCanvas(true,true);
            }
		}
    }
})