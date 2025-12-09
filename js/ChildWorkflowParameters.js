import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";
import { GroupNodeConfig, GroupNodeHandler } from "/extensions/core/groupNode.js";
import { $el, ComfyDialog } from "../../../scripts/ui.js";
import { api } from "../../../scripts/api.js";
const CONVERTED_TYPE = "converted-widget";
$el("style", {
    textContent: `
.lam_child_workflow_div{
    text-align: center;
    pointer-events: none; /* 让点击穿透到按钮 */
}
.lam_child_workflow_div button{
    pointer-events: auto; /* 仅按钮可点击，实现“点击冒泡”效果 */
}
`,
    parent: document.body,
})

function addWidget(node, widget) {
    if(widget.type === "customtext"){
        node.addWidget("STRING", widget.name, widget.value,function (v, _, node) {widget.value=v},Object.assign({}, widget.options) )
    }else{
        node.addWidget(widget.type, widget.name, widget.value,function (v, _, node) {widget.value=v},Object.assign({}, widget.options) )
    }
}

//判断参数是否存在
function paramExist(paramList, widget){
    // 修正拼写错误：nadeName -> name
    let params = paramList.filter(obj =>
        obj.nodeId === widget.nodeId &&
        obj.nodeType === widget.nodeType &&
        obj.nodeName === widget.nodeName
    );
    if(params.length>0){
        return true
    }else{
        return false
    }
}
//数据处理
function data_handle(workflow, paramList){ 
    let workflow_node_list = workflow['workflow']['nodes'];
    let workflow_nodes = {}
    for(let node of workflow_node_list){
        workflow_nodes[node['id']+''] = node
    }
    let workflow_output = workflow['output'];
    let output_index = 0;
    for(let param of paramList){
        let node_id = param.nodeId;
        let node_type = param.nodeType;
        let node_name = param.nodeName;
        let name = param.name;
        if(node_type=="input"){
            workflow_output[node_id]['inputs'][node_name]=['hidden',name]
        }else{
            if('outputs' in workflow_nodes[node_id]){
                workflow_output[node_id]['outputs']=[]
            }
            const index=workflow_nodes[node_id]['outputs'].findIndex(function(item){return item.name==node_name})
            workflow_output[node_id]['outputs'].push([index,output_index++])
        }
    }
    return workflow_output
}

function get_position_style(ctx, widget_width, y, node_height) {  
    const MARGIN = 4;  // the margin around the html element  
  
/* Create a transform that deals with all the scrolling and zooming */  
    const elRect = ctx.canvas.getBoundingClientRect();  
    const transform = new DOMMatrix()  
        .scaleSelf(elRect.width / ctx.canvas.width, elRect.height / ctx.canvas.height)  
        .multiplySelf(ctx.getTransform())  
        .translateSelf(MARGIN, MARGIN + y);  
  
    return {  
        transformOrigin: '0 0',  
        transform: transform,  
        left: `50px`,  
        top: `35px`,  
        position: "absolute",  
        maxWidth: `${widget_width - MARGIN*2}px`,  
        maxHeight: `${node_height - MARGIN*2}px`,    // we're assuming we have the whole height of the node  
        width: `auto`,  
        height: `auto`,  
    }  
}  

app.registerExtension({ 
    name: "ChildWorkflowParameters",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        var names = ["ChildWorkflowParameters"]
        if (names.indexOf(nodeData.name) >= 0) {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated?.apply(this, arguments);
                this.setProperty("paramList", [])
                this.setProperty("workflow", {})
                let thisNode = this
                const widget = {  
                    type: "HTML",   // whatever  
                    name: "childWork", // whatever  
                    draw(ctx, node, widget_width, y, widget_height) {  
                        Object.assign(this.inputEl.style, get_position_style(ctx, widget_width, y, node.size[1])); // assign the required style when we are drawn  
                    },  
                };
                widget.inputEl=$el('div.lam_child_workflow_div', [$el('button', {
                        textContent: '清空参数',
                        style: {},
                        onclick: () => {
                            thisNode.properties['paramList']=[]
                            thisNode.properties['workflow']={}
                            thisNode.inputs=[]
                            thisNode.outputs=[]
                            thisNode.widgets= thisNode.widgets.filter(w=>w.name==='childWork')
                            thisNode.widgets_values=[]
                        }
                    }),$el('button', {
                    textContent: '应用设置',
                    style: {},
                    onclick: async () => {
                        let workflow =await app.graphToPrompt();
                        const output = data_handle(workflow,thisNode.properties['paramList'])
                        console.log(output)
                        thisNode.properties['workflow'] = output;
                        alert('设置成功');
                    }
                })])
                document.body.appendChild(widget.inputEl);  
                this.addCustomWidget(widget);  
                this.onRemoved = function () { widget.inputEl.remove(); };  
                this.serialize_widgets = false;  
                return r;
            };
        }
    },
    loadedGraphNode(node, _) {
        if (node.type === "ChildWorkflowParameters") {
            // 渲染参数列表
             node.properties['paramList'].forEach(widget => {
                if(widget.value&&widget.nodeType==='input'){
                    addWidget(node, widget)
                }
            });
        }
    },
});




async function addConvertToGroupOptions() {
    // Add to nodes
    const getNodeMenuOptions = LGraphCanvas.prototype.getNodeMenuOptions;
    LGraphCanvas.prototype.getNodeMenuOptions = function (node) {
        const options = getNodeMenuOptions.apply(this, arguments);
        if (!GroupNodeHandler.isGroupNode(node) && node.type != 'ChildWorkflowParameters' && node.widgets) {
            let toInput = [];
            for (const w of node.inputs) {
                if (w.type !== CONVERTED_TYPE) {
                    toInput.push({
                        content: `添加 ${w.name} 到入参`,
                        callback: async () => {
                            let nodes = graph.computeExecutionOrder(false)
                            let appNode = nodes[nodes.findIndex(obj => obj.type === 'ChildWorkflowParameters')]
                            if (!appNode) {
                                alert('请先添加ChildWorkflowParameters节点');
                                return;
                            }
                            if(w.widget){
                                const widget = node.widgets.find(obj => obj.name === w.name)
                                let paramData = {
                                    name: w.node.id+'_'+widget.name,
                                    type: widget.type,
                                    value: widget.value,
                                    options: widget.options,
                                    id: appNode.properties['paramList'].length+1,
                                    nodeId: w.node.id,
                                    nodeName: widget.name,
                                    nodeType: 'input'
                                }
                                if(paramExist(appNode.properties['paramList'],paramData)){
                                    alert('参数已存在');
                                    return;
                                }
                                appNode.properties['paramList'].push(paramData)
                                addWidget(appNode, paramData)
                            }else{
                                let paramData = {
                                    name: w.node.id+'_'+w.name,
                                    type: w.type,
                                    id: appNode.properties['paramList'].length+1,
                                    nodeId: w.node.id,
                                    nodeName: w.name,
                                    nodeType: 'input'
                                }
                                if(paramExist(appNode.properties['paramList'],paramData)){
                                    alert('参数已存在');
                                    return;
                                }
                                appNode.properties['paramList'].push(paramData)
                                appNode.addInput(paramData.name, w.type)
                            }
                        }
                    });
                }
            }
            const index = options.findIndex((o) => o?.content === "Outputs") + 1 || options.length - 1;
            toInput.length > 0 && options.splice(index + 1, null, {
                content: `设置子工作流入参`,
                submenu: {
                    options: toInput
                }
            });
            // 出参
            let toOutput = [];
            for (const w of node.outputs) {
                if (w.type !== CONVERTED_TYPE) {
                    toOutput.push({
                        content: `添加 ${w.name} 到出参`,
                        callback: async () => {
                            let nodes = graph.computeExecutionOrder(false)
                            let appNode = nodes[nodes.findIndex(obj => obj.type === 'ChildWorkflowParameters')]
                            if (!appNode) {
                                alert('请先添加ChildWorkflowParameters节点');
                                return;
                            }
                            let paramData = {
                                name: w.node.id+'_'+w.name,
                                type: w.type,
                                id: appNode.properties['paramList'].length+1,
                                nodeId: w.node.id,
                                nodeName: w.name,
                                nodeType: 'output'
                            }
                            if(paramExist(appNode.properties['paramList'],paramData)){
                                alert('参数已存在');
                                return;
                            }
                            appNode.properties['paramList'].push(paramData)
                            appNode.addOutput(paramData.name, w.type)
                        }
                    });
                }
            }
            const indexOutput = options.findIndex((o) => o?.content === "Outputs") + 1 || options.length - 1;
            toOutput.length > 0 && options.splice(indexOutput + 1, null, {
                content: `设置子工作流出参`,
                submenu: {
                    options: toOutput
                }
            });
        }
        return options;
    };

}

const id = "Lam.ChildWorkflowParameters";
const ext = {
    name: id,
    async setup() {
        addConvertToGroupOptions();
    },
    // async beforeConfigureGraph(graphData, missingNodeTypes) {
    //     await getGroupNode(missingNodeTypes);
    // },
    // addCustomNodeDefs(defs) {
    //     // Store this so we can mutate it later with group nodes
    //     globalDefs = defs;
    // },
    // nodeCreated(node) {
    //     if (!GroupNodeHandler.isGroupNode(node)) {
    //     }
    // },
};

app.registerExtension(ext);