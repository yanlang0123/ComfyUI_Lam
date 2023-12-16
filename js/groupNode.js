import { app } from "/scripts/app.js";
import { GroupNodeConfig,GroupNodeHandler } from "/extensions/core/groupNode.js";
import { api } from "/scripts/api.js";

const GROUP = Symbol();

const Workflow = {
	InUse: {
		Free: 0,
		Registered: 1,
		InWorkflow: 2,
	},
	isInUseGroupNode(name) {
		const id = `workflow/${name}`;
		// Check if lready registered/in use in this workflow
		if (app.graph.extra?.groupNodes?.[name]) {
			if (app.graph._nodes.find((n) => n.type === id)) {
				return Workflow.InUse.InWorkflow;
			} else {
				return Workflow.InUse.Registered;
			}
		}
		return Workflow.InUse.Free;
	},
	storeGroupNode(name, data) {
		let extra = app.graph.extra;
		if (!extra) app.graph.extra = extra = {};
		let groupNodes = extra.groupNodes;
		if (!groupNodes) extra.groupNodes = groupNodes = {};
		groupNodes[name] = data;
	},
	delGroupNode(name) {
		let extra = app.graph.extra;
		if (!extra) return;
		let groupNodes = extra.groupNodes;
		if (!groupNodes) return;
		delete groupNodes[name];
	},
};

async function getGroupNode(missingNodeTypes) {
    const resp = await api.fetchApi(`/lam/groupNode`, { cache: "no-store" });
    if (resp.status === 200) {
        let data = await resp.json();
        await GroupNodeConfig.registerFromWorkflow(data, missingNodeTypes);
    }
}

async function saveGroupNode(nodeName, nodeData) {
	try {
		const response = await api.fetchApi("/lam/groupNode", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ [nodeName]:nodeData}),
		});
		if (response.status === 201) {
			return true;
		}
		if (response.status === 409) {
			return false;
		}
		throw new Error(response.statusText);
	} catch (error) {
		console.error(error);
	}
}

async function delGroupNode(name) {
	try {
		const response = await api.fetchApi("/lam/delGroupNode", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ 'name': name}),
		});
		if (response.status === 201) {
			return true;
		}
		if (response.status === 409) {
			return false;
		}
		throw new Error(response.statusText);
	} catch (error) {
		console.error(error);
	}
}

function addConvertToGroupOptions() {
	function addOption(options, index) {
		const selected = Object.values(app.canvas.selected_nodes ?? {});
		const disabled = selected.length < 2 || selected.find((n) => GroupNodeHandler.isGroupNode(n));
		options.splice(index + 1, null, {
			content: `转换为组节点且保存`,
			disabled,
			callback: async () => {
				const groupNode=await GroupNodeHandler.fromNodes(selected);
				if(groupNode){
					const groupData=groupNode[Object.getOwnPropertySymbols(groupNode)[0]].groupData;
					await saveGroupNode(groupData.name,groupData.nodeData);
				}
				return groupNode;
			},
		});
	}

	// Add to canvas
	const getCanvasMenuOptions = LGraphCanvas.prototype.getCanvasMenuOptions;
	LGraphCanvas.prototype.getCanvasMenuOptions = function () {
		const options = getCanvasMenuOptions.apply(this, arguments);
		const index = options.findIndex((o) => o?.content === "Add Group") + 1 || options.length;
		addOption(options, index);
		return options;
	};

	// Add to nodes
	const getNodeMenuOptions = LGraphCanvas.prototype.getNodeMenuOptions;
	LGraphCanvas.prototype.getNodeMenuOptions = function (node) {
		const options = getNodeMenuOptions.apply(this, arguments);
		if (!GroupNodeHandler.isGroupNode(node)) {
			const index = options.findIndex((o) => o?.content === "Outputs") + 1 || options.length - 1;
			addOption(options, index);
		}else{
            const index = options.findIndex((o) => o?.content === "Outputs") + 1 || options.length - 1;
            options.splice(index + 1, null, {
                content: `转换为节点且删除`,
                callback: ()=> {
                    const selected = Object.values(app.canvas.selected_nodes ?? {});
					const ret=selected[0].convertToNodes();
					const nodeName=selected[0][Object.getOwnPropertySymbols(selected[0])[0]].groupData.name;
					Workflow.delGroupNode(nodeName);
					try {
						LiteGraph.unregisterNodeType("workflow/" + nodeName);
					} catch (error) {}
					delGroupNode(nodeName);
                    return ret
                },
            });
        }
		return options;
	};
	//刷新和清除的时候都刷新一下组节点
	const sendActionToCanvas = LGraph.prototype.sendActionToCanvas;
	LGraph.prototype.sendActionToCanvas = function (action, params) {
		const options = sendActionToCanvas.apply(this, arguments);
		if (action === "clear") {
			getGroupNode();
		}
	}
    
}

const id = "Lam.GroupNode";
let globalDefs;
const ext = {
	name: id,
	setup() {
		addConvertToGroupOptions();
	},
	// async beforeConfigureGraph(graphData, missingNodeTypes) {
    //     await getGroupNode(missingNodeTypes);
	// },
	addCustomNodeDefs(defs) {
		// Store this so we can mutate it later with group nodes
		globalDefs = defs;
	},
	nodeCreated(node) {
		if (GroupNodeHandler.isGroupNode(node)) {
			//保留节点存储时的选择
			const groupData=node[Object.getOwnPropertySymbols(node)[0]].groupData;
			for(var i=0;i<groupData.nodeData.nodes.length;i++){
				node.widgets[i].value=groupData.nodeData.nodes[i].widgets_values[0]
			}
			Workflow.storeGroupNode(node[Object.getOwnPropertySymbols(node)[0]].groupData.name, node[Object.getOwnPropertySymbols(node)[0]].groupData.nodeData);
		}
	},
};

app.registerExtension(ext);
