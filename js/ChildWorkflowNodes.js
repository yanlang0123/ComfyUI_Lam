import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";
import { GroupNodeConfig, GroupNodeHandler } from "/extensions/core/groupNode.js";
import { $el, ComfyDialog } from "../../../scripts/ui.js";
import { api } from "../../../scripts/api.js";

async function getWorkflow(workflowName) {
    try {
        const resp = await api.fetchApi(`/userdata/workflows%2F${workflowName}`);
        if (resp.status === 200) {
            let data = await resp.json();
            const nodes= data.nodes;
            const node = nodes.find(n => n.type === "ChildWorkflowParameters");
            if (!node) {
                alert("工作流未配置参数节点")
                return null;
            }
            return node.properties;
        }
        throw new Error(resp.data.msg);
    } catch (error) {
        console.error(error);
    }
}

function addWidget(node, widget) {
    if(widget.type === "customtext"){
        node.addWidget("STRING", widget.name, widget.value,function (v, _, node) {widget.value=v},Object.assign({}, widget.options) )
    }else{
        node.addWidget(widget.type, widget.name, widget.value,function (v, _, node) {widget.value=v},Object.assign({}, widget.options) )
    }
}

app.registerExtension({
    name: "ChildWorkflowNodes",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        var names = ["ChildWorkflowNodes"]
        if (names.indexOf(nodeData.name) >= 0) {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated?.apply(this, arguments);
                this.setProperty("paramList", [])
                this.setProperty("workflow", {})
                let thisNode = this
                const widget = this.widgets.find(w => w.name === "workflowFile");
                const widget1 = {  
                    type: "HTML",   // whatever  
                    name: "childJson"
                };
                widget1.getValue = function () {
                    return JSON.stringify(thisNode.properties['workflow'])  
                }
                this.addCustomWidget(widget1);  
                // this.addDOMWidget('childJson',"list",$el('span.hidden',{style:{"word-wrap": "break-word"}}),{
                //     getValue(){
                //         return JSON.stringify(thisNode.properties['workflow'])  
                //     }
                // });
                widget.callback = async (value) => {
                    if (value) {
                        let props = await getWorkflow(value);
                        if(props) {
                            thisNode.properties['paramList']=props.paramList
                            thisNode.properties['workflow']=props.workflow
                            thisNode.inputs = thisNode.inputs.filter(w=>w.name==='workflowFile')
                            thisNode.widgets=  thisNode.widgets.filter(w=>w.name==='workflowFile')
                            thisNode.widgets_values=[]
                            thisNode.outputs=[]
                            // 渲染参数列表
                            props.paramList.forEach(widget => {
                                if(widget.nodeType==='input'){
                                    if(widget.value){
                                        addWidget(thisNode, widget)
                                    }else{
                                        thisNode.addInput(widget.name, widget.type)
                                    }
                                }else{
                                    thisNode.addOutput(widget.name, widget.type)
                                }
                                
                            });
                        }else{
                            thisNode.properties['paramList']=[]
                            thisNode.properties['workflow']={}
                            thisNode.inputs = thisNode.inputs.filter(w=>w.name==='workflowFile')
                            thisNode.widgets=  thisNode.widgets.filter(w=>w.name==='workflowFile')
                            thisNode.widgets_values=[]
                            thisNode.outputs=[]
                        }
                    }
                }
                return r;
            };
        }
    },
    loadedGraphNode(node, _) {
        if (node.type === "ChildWorkflowNodes") {
            // 渲染参数列表
             node.properties['paramList'].forEach(widget => {
                if(widget.value||widget.nodeType==='input'){
                    addWidget(node, widget)
                }
            });
        }
    },
});