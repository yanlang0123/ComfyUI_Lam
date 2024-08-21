// import { app } from "/scripts/app.js";
// function addConvertToGroupOptions() {
//     //中文搜索修改
//     const showSearchBox = LGraphCanvas.prototype.showSearchBox;
//     var funstr=showSearchBox+'';
//     var repStrs=['function(event, options) {','LiteGraph.pointerListenerAdd(dialog,"leave", function(e) {','timeout_close = setTimeout(function() {']
//     for(var i=0;i<repStrs.length;i++){ //如果对应几个字符串存在缺失，就放弃操作
//         if(funstr.indexOf(repStrs[i])==-1){
//             return;
//         }
//     }
//     funstr=funstr.replace('function(event, options) {','');
//     funstr=funstr.replace('LiteGraph.pointerListenerAdd(dialog,"leave", function(e) {', `let isComposing=false;
//             LiteGraph.pointerListenerAdd(dialog,"compositionstart", function(e) {
//                 isComposing=true;
//             });
//             LiteGraph.pointerListenerAdd(dialog,"compositionend", function(e) {
//                 isComposing=false;
//             });
//             LiteGraph.pointerListenerAdd(dialog,"leave", function(e) {`);
//     funstr=funstr.replace('timeout_close = setTimeout(function() {', `if (isComposing){
//                     return;
//                 }
//                 timeout_close = setTimeout(function() {`);
//     funstr=funstr.substring(0,funstr.length-2);
//     LGraphCanvas.prototype.showSearchBox = new Function('event','options',funstr);
// }
// const id = "Lam.LitegraphCore";
// let globalDefs;
// const ext = {
// 	name: id,
// 	setup() {
// 		addConvertToGroupOptions();
// 	},
// 	// async beforeConfigureGraph(graphData, missingNodeTypes) {
//     //     await getGroupNode(missingNodeTypes);
// 	// },
// 	// addCustomNodeDefs(defs) {
// 	// 	// Store this so we can mutate it later with group nodes
// 	// 	globalDefs = defs;
// 	// },
// 	// nodeCreated(node) {
		
// 	// },
// };

// app.registerExtension(ext);