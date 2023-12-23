import { app } from "/scripts/app.js";
import { $el } from "../../../scripts/ui.js";
$el("style", {
	textContent: `
    .node-zh-cn-name {
        background-color: rgb(128, 213, 247);
        color: #000;
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 2px 5px;
        cursor: pointer;
    }
    
    .node-zh-cn-name:hover {
        outline: 2px solid dodgerblue;
    }
    .node-zh-cn-name p {
        margin: 0;
    }
    .node-zh-cn-name span {
        text-align: center;
        border-radius: 5px;
        background-color: dodgerblue;
        color: #fff;
        padding: 2px;
        position: relative;
        min-width: 20px;
        overflow: hidden;
    }
`});
function addConvertToGroupOptions() {
    //中文搜索修改
    const showSearchBox = LGraphCanvas.prototype.showSearchBox;
    var funstr=showSearchBox+'';
    var repStrs=['function(event, options) {','var filtered = keys.filter( inner_test_filter );'
    ,'if ((!options.show_all_if_empty || str) && type.toLowerCase().indexOf(str) === -1)','help.dataset["type"] = escape(type);']
    for(var i=0;i<repStrs.length;i++){ //如果对应几个字符串存在缺失，就放弃操作
        if(funstr.indexOf(repStrs[i])==-1){
            return;
        }
    }
    funstr=funstr.replace('function(event, options) {','');
    funstr=funstr.replace('var filtered = keys.filter( inner_test_filter );', `var filtered = keys.filter( inner_test_filter );
    filtered=filtered.map(function(e){ 
        if(/.*[\u4e00-\u9fa5]+.*$/.test(LiteGraph.registered_node_types[e]['title'])) {
            return [e,LiteGraph.registered_node_types[e]['title']];
        }else{
            return e;
        }
    });`);
    funstr=funstr.replace('if ((!options.show_all_if_empty || str) && type.toLowerCase().indexOf(str) === -1)', `if ((!options.show_all_if_empty || str) && (type.toLowerCase().indexOf(str) === -1 && ctor.title.indexOf(str) === -1 ))`);
    //funstr=funstr.replace('help.innerText = type;', `help.innerHTML = type instanceof Array?'<div class="node-zh-cn-name"><p>'+type[0]+'</p><span>'+type[1]+'</span></div>':'<div class="node-zh-cn-name"><p>'+type+'</p></div>'`);
    funstr=funstr.replace('help.dataset["type"] = escape(type);',`help.dataset["type"]=type instanceof Array?escape(type[0]):escape(type);`);
    funstr=funstr.substring(0,funstr.length-2);
    LGraphCanvas.prototype.showSearchBox = new Function('event','options',funstr);
}
const id = "Lam.LitegraphCore";
let globalDefs;
const ext = {
	name: id,
	setup() {
		addConvertToGroupOptions();
	},
	// async beforeConfigureGraph(graphData, missingNodeTypes) {
    //     await getGroupNode(missingNodeTypes);
	// },
	// addCustomNodeDefs(defs) {
	// 	// Store this so we can mutate it later with group nodes
	// 	globalDefs = defs;
	// },
	// nodeCreated(node) {
		
	// },
};

app.registerExtension(ext);