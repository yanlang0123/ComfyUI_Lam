import { app } from "/scripts/app.js";


function adaptWidgetsToConnection(node) {
    if (!node.outputs || node.outputs.length === 0) {
        return
    }
    console.log("到这里==================")
}

function setupParameterNode(nodeType) {
    const onAdded = nodeType.prototype.onAdded
    nodeType.prototype.onAdded = function () {
        onAdded?.apply(this, arguments)
        adaptWidgetsToConnection(this)
    }

    const onAfterGraphConfigured = nodeType.prototype.onAfterGraphConfigured
    nodeType.prototype.onAfterGraphConfigured = function () {
        onAfterGraphConfigured?.apply(this, arguments)
        adaptWidgetsToConnection(this)
    }

    const onConnectOutput = nodeType.prototype.onConnectOutput
    nodeType.prototype.onConnectOutput = function (slot, type, input, target_node, target_slot) {
        if (!input.widget) {
            return false
        } else if (onConnectOutput) {
            result = onConnectOutput.apply(this, arguments)
            return result
        }
        return true
    }

    const onConnectionsChange = nodeType.prototype.onConnectionsChange
    nodeType.prototype.onConnectionsChange = function (_, index, connected) {
        if (!app.configuringGraph) {
            adaptWidgetsToConnection(this)
        }
        onConnectionsChange?.apply(this, arguments)
    }
}

const id = "Lam.Switch";
const ext = {
    name: id,
    setup() {
        //addConvertToGroupOptions();
        //添加按钮可以
    },
    async beforeConfigureGraph(graphData, missingNodeTypes) {
        //加载配置
    },
    beforeRegisterNodeDef(nodeType /*typeof LGraphNode*/, nodeData /*ComfyObjectInfo*/, app) {
        if (nodeData.name === "LamSwitchStart") {
            setupParameterNode(nodeType)
        }
    },
    addCustomNodeDefs(defs) {
        // 将其存储起来，以便稍后使用组节点对其进行修改
    },
    nodeCreated(node) {
        //节点创建
    },
};

app.registerExtension(ext);