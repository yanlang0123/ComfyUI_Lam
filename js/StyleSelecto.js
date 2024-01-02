import { app } from "/scripts/app.js";
import { $el } from "../../../scripts/ui.js";
import { ComfyWidgets } from "/scripts/widgets.js";
import { api } from "../../../scripts/api.js";

$el("style", {
	textContent: `
    .lam_style-model-info {
        color: white;
        font-family: sans-serif;
        max-width: 90vw;
    }
    .lam_style-model-content {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    .lam_style-model-info h2 {
        text-align: center;
        margin: 0 0 10px 0;
    }
    .lam_style-model-info p {
        margin: 5px 0;
    }
    .lam_style-model-info a {
        color: dodgerblue;
    }
    .lam_style-model-info a:hover {
        text-decoration: underline;
    }
    .lam_style-model-tags-list {
        display: flex;
        flex-wrap: wrap;
        list-style: none;
        gap: 10px;
        min-height: 100px;
        height: 60%;
        overflow: auto;
        margin: 10px 0;
        padding: 0;
    }
    .lam_style-model-tags-sel-list {
        display: flex;
        flex-wrap: wrap;
        list-style: none;
        gap: 10px;
        min-height: 100px;
        height: 20%;
        overflow: auto;
        margin: 10px 0;
        padding: 0;
    }
    .lam_style-model-tag {
        background-color: rgb(128, 213, 247);
        color: #000;
        display: flex;
        align-items: center;
        gap: 5px;
        border-radius: 5px;
        padding: 2px 5px;
        cursor: pointer;
        height: 26px;
    }
    .lam_style-model-tag--selected span::before {
        content: "✅";
        position: absolute;
        background-color: dodgerblue;
        top: 0;
        right: 0;
        bottom: 0;
        text-align: center;
    }
    .lam_style-model-tag:hover {
        outline: 2px solid dodgerblue;
    }
    .lam_style-model-tag p {
        margin: 0;
    }
    .lam_style-model-tag span {
        text-align: center;
        border-radius: 5px;
        background-color: dodgerblue;
        color: #fff;
        padding: 2px;
        position: relative;
        min-width: 20px;
        overflow: hidden;
    }
    
    .lam_style-model-metadata .comfy-modal-content {
        max-width: 100%;
    }
    .lam_style-model-metadata label {
        margin-right: 1ch;
        color: #ccc;
    }
    
    .lam_style-model-metadata span {
        color: dodgerblue;
    }
    
    .lam_style-preview {
        max-width: 50%;
        margin-left: 10px;
        position: relative;
    }
    .lam_style-preview img {
        max-height: 300px;
    }
    .lam_style-preview button {
        position: absolute;
        font-size: 12px;
        bottom: 10px;
        right: 10px;
        color: var(--input-text);
        background-color: var(--comfy-input-bg);
        border-radius: 8px;
        border-color: var(--border-color);
        border-style: solid;
        margin-top: 2px;
    }
    .lam_style-model-notes {
        background-color: rgba(0, 0, 0, 0.25);
        padding: 5px;
        margin-top: 5px;
    }
    .lam_style-model-notes:empty {
        display: none;
    }    

`,
parent: document.body,
})

let pb_cache = {};
async function getStyles(name) {
    if(pb_cache[name])
		return pb_cache[name];
	else {
        const resp = await api.fetchApi(`/lam/getStyles?name=${name}`);
        if (resp.status === 200) {
            let data = await resp.json();
            pb_cache[name] = data;
            return data;
        }
        return undefined;
    }
    
}

function getSelList(tags) {
    let rlist=[]
    tags.forEach((k) => {
        rlist.push($el(
            "li.lam_style-model-tag",
            {},
            [
                $el("p", {
                    textContent:k,
                })
            ]
        ))
    })
    return rlist;
}
function getTagList(tags) {
    let rlist=[]
    tags.forEach((k,i) => {
        let t=[ k['zhName'],k['name']]
        rlist.push($el(
            "li.lam_style-model-tag",
            {
                dataset: {
                    tag: t[1],
                    name: t[0],
                },
                $: (el) => {
                    el.onclick = () => {
                        el.classList.toggle("lam_style-model-tag--selected");
                    };
                },
            },
            [
                $el("p", {
                    textContent: t[0],
                }),
                $el("span", {
                    textContent: i,
                }),
            ]
        ))
    });
    return rlist
}
// Displays input text on a node
app.registerExtension({
    name: "StyleSelecto",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
		var names=['StyleSelecto']
        if (names.indexOf(nodeData.name)>=0) {
            // When the node is created we want to add a readonly text widget to display the text
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated?.apply(this, arguments);
                let style_type = this.widgets[this.widgets.findIndex(obj => obj.name === 'style_type')];
                const style_name = {value:''}
                this.setProperty("values", [])
                let names=[]
                //stylesEl.inputEl.classList.add("lam-model-notes");
                const list = $el("ol.lam_style-model-tags-list",[]);
                const lists = $el("ol.lam_style-model-tags-sel-list",[]);
                let styles=this.addDOMWidget('button',"btn",$el('div.lam_style-preview',[$el('button',{
                    textContent:'清除全部选择',
                    style:{},
                    onclick:()=>{
                            styles.element.children[1].querySelectorAll(".lam_style-model-tag--selected").forEach(el => {
                                el.classList.remove("lam_style-model-tag--selected");
                            })
                            this.properties["values"]=[]
                            names=[]
                            styles.element.children[3].innerHTML=''

                        }}
                    ),list,$el('span',{textContent:"选择内容"}),lists]));
                let st_values=''
                Object.defineProperty(style_type, "value", {
                    set: (x) => {
                        st_values=x
                        if(st_values){
                            getStyles(st_values);
                            styles.element.children[1].innerHTML=''
                            if(pb_cache[st_values]){
                                    let list =getTagList(pb_cache[st_values]);
                                    styles.element.children[1].append(...list)
                                    styles.element.children[1].querySelectorAll(".lam_style-model-tag").forEach(el => {
                                    if(this.properties["values"].includes(el.dataset.tag)){
                                        el.classList.add("lam_style-model-tag--selected");
                                    }
                                    this.setSize([500, 600]);
                                });
                            }
                            
                        }
                    },
                    get: () => {
                        if(pb_cache[st_values]&&styles.element.children[1].children.length==0){
                                let list =getTagList(pb_cache[st_values]);
                                styles.element.children[1].append(...list)
                                styles.element.children[1].querySelectorAll(".lam_style-model-tag").forEach(el => {
                                if(this.properties["values"].includes(el.dataset.tag)){
                                    el.classList.add("lam_style-model-tag--selected");
                                }
                                this.setSize([500, 600]);
                            });
                        }
                        return st_values;
                    }
                });
                let stylesValue=''
                Object.defineProperty(styles, "value", {
                    set: (x) => {
                        
                    },
                    get: () => {
                            let namestr=names.join(',')
                            styles.element.children[1].querySelectorAll(".lam_style-model-tag").forEach(el => {
                            if(el.classList.value.indexOf("lam_style-model-tag--selected")>=0){
                                if(!this.properties["values"].includes(el.dataset.tag)){
                                    this.properties["values"].push(el.dataset.tag);
                                }
                                if(!names.includes(el.dataset.name)){
                                    names.push(el.dataset.name)
                                }
                            }else{
                                if(this.properties["values"].includes(el.dataset.tag)){
                                    this.properties["values"]=this.properties["values"].filter(v=>v!=el.dataset.tag);
                                    names=names.filter(v=>v!=el.dataset.name);
                                }
                            }
                            if(namestr!=names.join(',')){
                                if(names.length>0){
                                    let sellist=getSelList(names)
                                    styles.element.children[3].innerHTML=''
                                    styles.element.children[3].append(...sellist)
                                }else{
                                    styles.element.children[3].innerHTML=''
                                }
                            }
                            stylesValue = this.properties["values"].join(',');

                        });
                        return stylesValue;
                    }
                });
                
                this.setSize([500, 600]);
                return r;
            };


        }
    },
});