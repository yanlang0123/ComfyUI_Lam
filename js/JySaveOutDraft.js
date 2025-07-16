import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";
import { $el,ComfyDialog } from "../../../scripts/ui.js";

function download_file(url, filename) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.responseType = "blob";
    xhr.onload = function () {
        if (this.status == 200) {
            var blob = this.response;
            var a = document.createElement('a');
            a.style.display = 'none';
            a.href = window.URL.createObjectURL(blob);
            a.download = filename || 'downloaded_file';
            document.body.appendChild(a);
            a.click();
            setTimeout(function() {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(a.href);
            }, 100);
        }
    };
    xhr.send();
}

app.registerExtension({
    name: "JySaveOutDraft",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
		var names=["JySaveOutDraft"]
        if (names.indexOf(nodeData.name)>=0) {
            // When the node is created we want to add a readonly text widget to display the text
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated?.apply(this, arguments);

                this.addDOMWidget('downs',"list",$el('div.lam_down',[$el('button',{
                    textContent:'下载草稿',
                    style:{},
                    onclick:()=>{
                        const v = app.nodeOutputs?.[this.id + ""];
                        if (!this.flags.collapsed && v && v.down){
                            let data=v.down[0]
                            let url=`/api/view?type=${data.type}&filename=${data.filename}&subfolder=${data.subfolder}&rand=${Math.random()}`
                            download_file(url,data.filename)
                        }else{
                            alert("请先执行工作流")
                        }
                        
                    }})]
                    )
                )
                return r;
            };
        }
    },
});