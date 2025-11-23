import { app } from "/scripts/app.js";
import { $el } from "../../../scripts/ui.js";

const nodeName = "LamCommonHidden";

app.registerExtension({
    name: "Comfy.lam."+nodeName,
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        var names=[nodeName]
        if (names.indexOf(nodeData.name)>=0) {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                this.setProperty("hidden", '')
                let that=this
				this.addDOMWidget('hidden',"list",$el('span.hidden',{style:{"word-wrap": "break-word"}}),{
                    getValue(){
                        return that.properties['hidden']
                    }
                });
                return r;
            }
            
        }
    },
});