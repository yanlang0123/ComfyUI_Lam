import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";

// Displays input text on a node

app.registerExtension({
    name: "StatusInfo",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
		var names=["Image2Video",'Video2TalkingFace','VideoAddAudio','Image2TalkingFace','ForEnd','LoadVideo','VideoFaceFusion',
    'Text2AutioEdgeTts','VideoRoopFaceSwap','PromptTranslator']
        if (names.indexOf(nodeData.name)>=0) {
            // When the node is created we want to add a readonly text widget to display the text
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated?.apply(this, arguments);

                const w = ComfyWidgets["STRING"](this, "StatusInfo", ["STRING", { multiline: true }], app).widget;
                w.inputEl.readOnly = true;
                w.inputEl.style.opacity = 0.6;
                return r;
            };

            // When the node is executed we will be sent the input text, display this in the widget
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function(message) {
                onExecuted?.apply(this, arguments);
				for (let i = 0; i < this.widgets.length; i++) {
					if(this.widgets[i].name=='StatusInfo'){
                        if(message?.text){
                            this.widgets[i].value = message.text.join('');
                        }
						break;
					}
				}

                if (this.size[1] < 200) {
                    this.setSize([this.size[0], 200]);
                }
            };
        }
    },
});