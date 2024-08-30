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
        align-content: flex-start;
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
        align-content: flex-start;
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
        padding: 2px 2px;
        cursor: pointer;
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
async function getModelNames(name) {
    if(pb_cache[name])
		return pb_cache[name];
	else {
        const resp = await api.fetchApi(`/lam/getModelNames`);
        if (resp.status === 200) {
            let data = await resp.json();
            pb_cache = data;
            return pb_cache[name];
        }
        return undefined;
    }
    
}

function getSelList(tags) {
    let rlist=[]
    Object.keys(tags).forEach((k) => {
        rlist.push($el(
            "li.lam_style-model-tag",
            {
                dataset: {
                    imgName: tags[k]['imgName'],
                    name:   tags[k]['name'],
                    tag: tags[k]['tag']
                },
                $: (el) => {
                    el.onclick = () => {
                        el.classList.add("lam_style-model-tag--del");
                    };
                },
            },
            [
                $el("p", {
                    textContent:tags[k]['name'],
                })
            ]
        ))
    })
    return rlist;
}
function getTagList(tags) {
    let rlist=[]
    tags.forEach((k,i) => {
        rlist.push($el(
            "li.lam_style-model-tag",
            {
                dataset: {
                    tag: k,
                    name: k,
                },
                $: (el) => {
                    el.onclick = () => {
                        el.classList.toggle("lam_style-model-tag--selected");
                    };
                },
            },
            [
                $el("p", {
                    textContent: k,
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
    name: "LamCommonNames",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
		var names=['LamCommonNames']
        if (names.indexOf(nodeData.name)>=0) {
            // When the node is created we want to add a readonly text widget to display the text
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated?.apply(this, arguments);
                let style_type = this.widgets[this.widgets.findIndex(obj => obj.name === 'name_type')];
                this.setProperty("values", [])
                this.setProperty("selTags", {})
                //stylesEl.inputEl.classList.add("lam-model-notes");
                const list = $el("ol.lam_style-model-tags-list",[]);
                const lists = $el("ol.lam_style-model-tags-sel-list",[]);
                let styles=this.addDOMWidget('names',"list",$el('div.lam_style-preview',[$el('button',{
                        textContent:'清除全部选择',
                        style:{},
                        onclick:()=>{
                                styles.element.children[1].querySelectorAll(".lam_style-model-tag--selected").forEach(el => {
                                    el.classList.remove("lam_style-model-tag--selected");
                                })
                                this.properties["values"]=[]
                                this.properties['selTags']={}
                                styles.element.children[3].innerHTML=''
                            }}
                        ),list,$el('span',{textContent:"选择内容"}),lists,
                        $el('button',{
                            textContent:'选择全部',
                            style:{"right":"auto"},
                            onclick:()=>{
                                styles.element.children[1].querySelectorAll(".lam_style-model-tag").forEach(el => {
                                    el.classList.add("lam_style-model-tag--selected");
                                });
                            }}
                            )]));
                let st_values='';
                Object.defineProperty(style_type, "value", {
                    set: (x) => {
                        if(st_values!=x){
                            st_values=x
                            getModelNames(st_values);
                            styles.element.children[1].innerHTML=''
                            if(pb_cache[st_values]){
                                styles.element.children[1].querySelectorAll(".lam_style-model-tag--selected").forEach(el => {
                                    el.classList.remove("lam_style-model-tag--selected");
                                })
                                this.properties["values"]=[]
                                this.properties['selTags']={}
                                styles.element.children[3].innerHTML=''
                                this.setSize([500, 600]);
                            }
                            
                        }
                    },
                    get: () => {
                        if(st_values&&!pb_cache[st_values]){
                            getModelNames(st_values);
                            styles.element.children[1].innerHTML=''
                        }else if(!st_values){
                            style_type.value=style_type.options.values[0];
                            this.setSize([500, 600]);
                        }
                        if(pb_cache[st_values]&&styles.element.children[1].children.length==0){
                            this.properties["values"]=[]
                            this.properties['selTags']={}
                            let list =getTagList(pb_cache[st_values]);
                            styles.element.children[1].append(...list)
                            styles.element.children[1].querySelectorAll(".lam_style-model-tag").forEach(el => {
                                if(this.properties["values"].includes(el.dataset.tag)){
                                    el.classList.add("lam_style-model-tag--selected");
                                }
                            });
                            this.setSize([500, 600]);
                        }
                        return st_values;
                    }
                });
                let stylesValue=''
                Object.defineProperty(styles, "value", {
                    set: (x) => {
                    },
                    get: () => {
                        let namestr=Object.keys(this.properties['selTags']).join(',')
                        let delList=[]
                        styles.element.children[3].querySelectorAll(".lam_style-model-tag--del").forEach(el => {
                            delList.push(el.dataset.tag)
                        })
                        styles.element.children[1].querySelectorAll(".lam_style-model-tag").forEach(el => {
                            if(el.classList.value.indexOf("lam_style-model-tag--selected")>=0&&!delList.includes(el.dataset.tag)){
                                if(!this.properties["values"].includes(el.dataset.tag)){
                                    this.properties["values"].push(el.dataset.tag);
                                }
                                if(!Object.keys(this.properties['selTags']).includes(el.dataset.name)){
                                    this.properties['selTags'][el.dataset.tag]={imgName:el.dataset.imgName,tag:el.dataset.tag,name:el.dataset.name}
                                }
                            }else{
                                if(delList.includes(el.dataset.tag)){
                                    el.classList.remove("lam_style-model-tag--selected");
                                    delList=delList.filter(v=>v!=el.dataset.tag)
                                }
                                if(this.properties["values"].includes(el.dataset.tag)){
                                    this.properties["values"]=this.properties["values"].filter(v=>v!=el.dataset.tag);
                                    delete this.properties['selTags'][el.dataset.tag];
                                }
                            }

                        });
                        for(let i=0;i<delList.length;i++){
                            if(this.properties["values"].includes(delList[i])){
                                this.properties["values"]=this.properties["values"].filter(v=>v!=delList[i]);
                                delete this.properties['selTags'][delList[i]];
                            }
                        }
                        if(namestr!=Object.keys(this.properties['selTags']).join(',')||styles.element.children[3].innerHTML==''){
                            if(Object.keys(this.properties['selTags']).length>0){
                                let sellist=getSelList(this.properties['selTags'])
                                styles.element.children[3].innerHTML=''
                                styles.element.children[3].append(...sellist)
                            }else{
                                styles.element.children[3].innerHTML=''
                            }
                        }
                        stylesValue = this.properties["values"].join(',');
                        return stylesValue;
                    }
                });
                
                this.setSize([500, 600]);
                return r;
            };


        }
    },
});