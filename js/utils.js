export function CUSTOM_INT(node, inputName, val, func, config = {}) {
	return {
		widget: node.addWidget(
			"number",
			inputName,
			val,
			func, 
			Object.assign({}, { min: 0, max: 4096, step: 640, precision: 0 }, config)
		),
	};
}

export function CUSTOM_COMBO(node, inputName, val, func, config = {}) {
	return {
		widget: node.addWidget(
			"combo",
			inputName,
			val,
			func, 
			Object.assign({}, config)
		),
	};
}

export function recursiveLinkUpstream(node, type, depth, index=null) {
	depth += 1
	let connections = []
	const inputList = (index !== null) ? [index] : [...Array(node.inputs.length).keys()]
	if (inputList.length === 0) { return }
	for (let i of inputList) {
		const link = node.inputs[i].link
		if (link) {
			const nodeID = node.graph.links[link].origin_id
			const slotID = node.graph.links[link].origin_slot
			const connectedNode = node.graph._nodes_by_id[nodeID]

			if (connectedNode.outputs[slotID].type === type) {

				connections.push([connectedNode.id, depth])

				if (connectedNode.inputs) {
					const index = (connectedNode.type === "LatentComposite") ? 0 : null
					connections = connections.concat(recursiveLinkUpstream(connectedNode, type, depth, index))
				} else {
					
				}
			}
		}
	}
	return connections
}

export function transformFunc(widget, value, node, index) {
	const s = widget.options.step / 10;
	widget.value = Math.round(value / s) * s;
	node.properties["values"][node.widgets[node.index].value][index] = widget.value
	if (node.widgets_values) { 
		node.widgets_values[2] = node.properties["values"].join()
	}
}

export function swapInputs(node, indexA, indexB) {
	const linkA = node.inputs[indexA].link
	let origin_slotA = null
	let node_IDA = null
	let connectedNodeA = null
	let labelA = node.inputs[indexA].label || null

	const linkB = node.inputs[indexB].link
	let origin_slotB = null
	let node_IDB = null
	let connectedNodeB = null
	let labelB = node.inputs[indexB].label || null

	if (linkA) {
		node_IDA = node.graph.links[linkA].origin_id
		origin_slotA = node.graph.links[linkA].origin_slot
		connectedNodeA = node.graph._nodes_by_id[node_IDA]

		node.disconnectInput(indexA)
	}

	if (linkB) {
		node_IDB = node.graph.links[linkB].origin_id
		origin_slotB = node.graph.links[linkB].origin_slot
		connectedNodeB = node.graph._nodes_by_id[node_IDB]

		node.disconnectInput(indexB)
	}

	if (linkA) {
		connectedNodeA.connect(origin_slotA, node, indexB)
	}

	if (linkB) {
		connectedNodeB.connect(origin_slotB, node, indexA)
	}

	node.inputs[indexA].label = labelB
	node.inputs[indexB].label = labelA
	
}

export function renameNodeInputs(node, name, offset=0) {
	for (let i=offset; i < node.inputs.length; i++) {
		node.inputs[i].name = `${name}${i-offset}`
		if(node.inputs[i].label){
			node.inputs[i].label = `${name}${i-offset}`
		}
	}
}

export function swapOutputs(node, indexA, indexB) {
	const linkAs = JSON.parse(JSON.stringify(node.outputs[indexA].links))
	let origin_slotA = null
	let node_IDA = null
	let connectedNodeA = null
	let labelA = node.outputs[indexA].label || null

	const linkBs = JSON.parse(JSON.stringify(node.outputs[indexB].links))
	let origin_slotB = null
	let node_IDB = null
	let connectedNodeB = null
	let labelB = node.outputs[indexB].label || null

	if(linkAs&&linkAs.length>0){
		for(let linkA of linkAs){
			node_IDA = node.graph.links[linkA].target_id
			origin_slotA = node.graph.links[linkA].target_slot
			connectedNodeA = node.graph._nodes_by_id[node_IDA]
			node.connect(indexB,connectedNodeA,origin_slotA)
		}
		node.disconnectOutput(indexA)
	}
	

	if(linkBs&&linkBs.length>0){
		for(let linkB of linkBs){
			node_IDB = node.graph.links[linkB].target_id
			origin_slotB = node.graph.links[linkB].target_slot
			connectedNodeB = node.graph._nodes_by_id[node_IDB]
			node.connect(indexA,connectedNodeB,origin_slotB)
		}
		node.disconnectOutput(indexB)
	}

	node.outputs[indexA].label = labelB
	node.outputs[indexB].label = labelA
	
}
export function renameNodeOutputs(node, name, offset=0) {
	for (let i=offset; i < node.outputs.length; i++) {
		node.outputs[i].name = `${name}${i-offset}`
		if(node.outputs[i].label){
			node.outputs[i].label = `${name}${i-offset}`
		}
	}
}
export function swapInputsNot01(node, indexesToRemove){
	for (let i=0;i<indexesToRemove.length;i++) {
		if(node.inputs[indexesToRemove[i]].widget){
			for(let j=0; j<node.inputs.length; j++){
				if(!indexesToRemove.includes(j)&&j>indexesToRemove[i]){
					swapInputs(node, indexesToRemove[i], j)
					indexesToRemove[i]=j
					swapInputsNot01(node, indexesToRemove)
					break;
				}
			}
		}
	}
}
export function removeNodeInputs(node, indexesToRemove, offset=0) {
	swapInputsNot01(node, indexesToRemove)
	indexesToRemove.sort((a, b) => b - a);
	for (let i of indexesToRemove) {
		if ((node.inputs.length-offset) <= 2) { console.log("too short"); continue } // if only 2 left
		node.removeInput(i)
		node.properties["values"]&&node.properties.values.splice(i-offset, 1)
	}
	if(node.properties["values"]){
		const inputLenght = node.properties["values"].length-1

		node.widgets[node.index].options.max = inputLenght
		if (node.widgets[node.index].value > inputLenght) {
			node.widgets[node.index].value = inputLenght
		}
	}
	node.onResize(node.size)
}

export function swapOutputsNot01(node, indexesToRemove){
	for (let i=0;i<indexesToRemove.length;i++) {
		if(node.outputs[indexesToRemove[i]].widget){
			for(let j=0; j<node.outputs.length; j++){
				if(!indexesToRemove.includes(j)&&j>indexesToRemove[i]){
					swapOutputs(node, indexesToRemove[i], j)
					indexesToRemove[i]=j
					swapOutputsNot01(node, indexesToRemove)
					break;
				}
			}
		}
	}
}
export function removeNodeOutputs(node, indexesToRemove, offset=0) {
	swapOutputsNot01(node, indexesToRemove)
	indexesToRemove.sort((a, b) => b - a);
	for (let i of indexesToRemove) {
		if ((node.outputs.length-offset) <= 1) { console.log("too short"); continue } // if only 2 left
		node.removeOutput(i)
	}
	node.onResize(node.size)
}

export function getDrawColor(percent, alpha) {
	let h = 360*percent
	let s = 50;
	let l = 50;
	l /= 100;
	const a = s * Math.min(l, 1 - l) / 100;
	const f = n => {
		const k = (n + h / 30) % 12;
		const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
		return Math.round(255 * color).toString(16).padStart(2, '0');   // convert to Hex and prefix "0" if needed
	};
	return `#${f(0)}${f(8)}${f(4)}${alpha}`;
}

export function hexToRgba(hex, opacity) {
	return hex && hex.replace(/\s+/g, '').length === 7 ? 'rgba(' + parseInt('0x' + hex.slice(1, 3)) + ',' +
	  parseInt('0x' + hex.slice(3, 5)) + ',' +
	  parseInt('0x' + hex.slice(5, 7)) + ',' + opacity + ')' : ''
}

export function computeCanvasSize(node, size) {
	if (node.widgets[0].last_y == null) return;

	const MIN_SIZE = 200;

	let y = LiteGraph.NODE_WIDGET_HEIGHT * Math.max(node.inputs.length, node.outputs.length) + 5;
	let freeSpace = size[1] - y;

	// Compute the height of all non customtext widgets
	let widgetHeight = 0;
	for (let i = 0; i < node.widgets.length; i++) {
		const w = node.widgets[i];
		if (w.type !== "customLamCanvas") {
			if (w.computeSize) {
				widgetHeight += w.computeSize()[1] + 4;
			} else {
				widgetHeight += LiteGraph.NODE_WIDGET_HEIGHT + 5;
			}
		}
	}

	// See how large the canvas can be
	freeSpace -= widgetHeight;

	// There isnt enough space for all the widgets, increase the size of the node
	if (freeSpace < MIN_SIZE) {
		freeSpace = MIN_SIZE;
		node.size[1] = y + widgetHeight + freeSpace;
		if(node.graph) node.graph.setDirtyCanvas(true);
	}

	// Position each of the widgets
	for (const w of node.widgets) {
		w.y = y;
		if (w.type === "customLamCanvas") {
			y += freeSpace;
		} else if (w.computeSize) {
			y += w.computeSize()[1] + 4;
		} else {
			y += LiteGraph.NODE_WIDGET_HEIGHT + 4;
		}
	}

	node.canvasHeight = freeSpace;
}