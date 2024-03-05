import { app } from "/scripts/app.js";
import { $el } from "../../../scripts/ui.js";
import { ComfyWidgets } from "/scripts/widgets.js";
import { api } from "../../../scripts/api.js";

$el("style", {
	textContent: `
    .lam-model-info {
        color: white;
        font-family: sans-serif;
        max-width: 90vw;
    }
    .lam-model-content {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    .lam-model-info h2 {
        text-align: center;
        margin: 0 0 10px 0;
    }
    .lam-model-info p {
        margin: 5px 0;
    }
    .lam-model-info a {
        color: dodgerblue;
    }
    .lam-model-info a:hover {
        text-decoration: underline;
    }
    .lam-model-tags-list {
        display: flex;
        align-content: flex-start;
        flex-wrap: wrap;
        list-style: none;
        gap: 10px;
        min-height: 100px;
        height: 45%;
        overflow: auto;
        margin: 10px 0;
        padding: 0;
    }
    .lam-model-tags-sel-list {
        display: flex;
        align-content: flex-start;
        flex-wrap: wrap;
        list-style: none;
        gap: 10px;
        min-height: 100px;
        height: 35%;
        overflow: auto;
        margin: 10px 0;
        padding: 0;
    }
    .lam-model-tag {
        background-color: rgb(128, 213, 247);
        color: #000;
        display: flex;
        align-items: center;
        gap: 5px;
        border-radius: 5px;
        padding: 2px 5px;
        cursor: pointer;
    }
    .lam-model-tag--selected span::before {
        content: "✅";
        position: absolute;
        background-color: dodgerblue;
        top: 0;
        right: 0;
        bottom: 0;
        text-align: center;
    }
    .lam-model-tag:hover {
        outline: 2px solid dodgerblue;
    }
    .lam-model-tag p {
        margin: 0;
    }
    .lam-model-tag span.lable {
        text-align: center;
        border-radius: 5px;
        background-color: dodgerblue;
        color: #fff;
        padding: 2px;
        position:
         relative;
        min-width: 20px;
        overflow: hidden;
        min-width: 35px;
    }
    .lam-model-tag span.btn {
        text-align: center;
        border-radius: 5px;
        background-color: red;
        color: #fff;
        padding: 2px;
        position: relative;
        min-width: 20px;
        overflow: hidden;
        user-select: none;
    }
    
    .lam-model-metadata .comfy-modal-content {
        max-width: 100%;
    }
    .lam-model-metadata label {
        margin-right: 1ch;
        color: #ccc;
    }
    
    .lam-model-metadata span {
        color: dodgerblue;
    }
    
    .lam-preview {
        max-width: 50%;
        margin-left: 10px;
        position: relative;
    }
    .lam-preview img {
        max-height: 300px;
    }
    .lam-preview button {
        position: absolute;
        font-size: 12px;
        bottom: 10px;
        right: 10px;
    }
    .lam-model-notes {
        background-color: rgba(0, 0, 0, 0.25);
        padding: 5px;
        margin-top: 5px;
    }
    .lam-model-notes:empty {
        display: none;
    }    
`,
parent: document.body,
})

let pb_cache = {};
async function getPrompt(name) {
    if(pb_cache[name])
		return pb_cache[name];
	else {
        const resp = await api.fetchApi(`/lam/getPrompt?name=${name}`);
        if (resp.status === 200) {
            let data = await resp.json();
            pb_cache[name] = data;
            return data;
        }
        return undefined;
    }
    
}
function getTagList(tags,cat) {
    let rlist=[]
    Object.keys(tags).forEach((k) => {
        if (typeof tags[k] === "string") {
            let t=[k, tags[k]]
            rlist.push($el(
                "li.lam-model-tag",
                {
                    dataset: {
                        tag: t[1],
                        name: t[0],
                        cat:cat,
                        weight: 1
                    },
                    $: (el) => {
                        el.onclick = () => {
                            el.classList.toggle("lam-model-tag--selected");
                        };
                    },
                },
                [
                    $el("p", {
                        textContent: t[0],
                    }),
                    $el("span.lable", {
                        textContent: t[1],
                    }),
                ]
            ))
        }else{
            rlist.push(...getTagList(tags[k],cat))
        }
    });
    return rlist
}
function getSelList(tags) {
    let rlist=[]
    Object.keys(tags).forEach((k) => {
        rlist.push($el(
            "li.lam-model-tag",
            {
                dataset: {
                    name:  tags[k]['name'],
                    tag: tags[k]['tag'],
                    cat: tags[k]['cat'],
                    weight: tags[k]['weight'],
                },
                // $: (el) => {
                //     el.onclick = () => {
                //         el.classList.add("lam-model-tag--del");
                //     };
                // },
            },
            [
                $el("span.btn", {
                    textContent: "-",
                    $: (el) => {
                        el.onclick = () => {
                            el.parentElement.dataset.weight = (((Number(el.parentElement.dataset.weight)*1000)-(0.05*1000))/1000).toFixed(2);
                        };
                    },
                }),
                $el("p", {
                    textContent: tags[k]['name'],
                }),
                $el("span.lable", {
                    textContent: tags[k]['weight'],
                }),
                $el("span.lable", {
                    textContent: tags[k]['cat'],
                }),
                $el("span.btn", {
                    textContent: "+",
                    $: (el) => {
                        el.onclick = () => {
                            el.parentElement.dataset.weight = (((Number(el.parentElement.dataset.weight)*1000)+(0.05*1000))/1000).toFixed(2);
                        };
                    },
                }),
                $el("span.btn", {
                    textContent: "X",
                    $: (el) => {
                        el.onclick = () => {
                            el.parentElement.classList.add("lam-model-tag--del");
                        };
                    },
                }),
            ]
        ))
    })
    return rlist;
}
// Displays input text on a node
app.registerExtension({
    name: "EasyPromptSelecto",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
		var names=['EasyPromptSelecto']
        if (names.indexOf(nodeData.name)>=0) {
            // When the node is created we want to add a readonly text widget to display the text
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated?.apply(this, arguments);
                this.setProperty("values", [])
                this.setProperty("selTags", {})
                ComfyWidgets["COMBO"](this, "category", ['a','b']).widget;
                const list = $el("ol.lam-model-tags-list",[]);
                const lists = $el("ol.lam-model-tags-sel-list",[]);
                let tags=this.addDOMWidget('tags',"list",$el('div.lam_style-preview',[$el('button',{
                    textContent:'清除全部选择',
                    style:{},
                    onclick:()=>{
                            tags.element.children[1].querySelectorAll(".lam-model-tag--selected").forEach(el => {
                                el.classList.remove("lam-model-tag--selected");
                            })
                            this.properties["values"]=[]
                            this.properties['selTags']={}
                            tags.element.children[3].innerHTML=''

                        }}
                    ),list,$el('span',{textContent:"选择内容"}),lists]));
                let prompt_type = this.widgets[this.widgets.findIndex(obj => obj.name === 'prompt_type')];
                let textEl = this.widgets[this.widgets.findIndex(obj => obj.name === 'text')];
                let category = this.widgets[this.widgets.findIndex(obj => obj.name === 'category')];
                let cat_values=[]
                let cat_value=''
                let tagsValue=''

                Object.defineProperty(category.options, "values", {
                    set: (x) => {
                    },
                    get: () => {
                        getPrompt(prompt_type.value);
                        if(pb_cache[prompt_type.value] == undefined) {
                            return cat_values;
                        }
                        if(cat_values.join(',')!=Object.keys(pb_cache[prompt_type.value]).join(',')){
                            cat_values=Object.keys(pb_cache[prompt_type.value])
                            cat_value=''
                        }
                        return cat_values;
                    }
                });
                Object.defineProperty(category, "value", {
                    set: (x) => {
                        if(cat_value!=x){
                            cat_value=x;
                            if(!cat_value){
                                return 
                            }
                            if(pb_cache[prompt_type.value]&&pb_cache[prompt_type.value][cat_value]){
                                tags.element.children[1].innerHTML=''
                                let list =getTagList(pb_cache[prompt_type.value][cat_value],cat_value);
                                tags.element.children[1].append(...list)
                            }
                            tags.element.children[1].querySelectorAll(".lam-model-tag").forEach(el => {
                                if(this.properties["values"].includes(el.dataset.tag)){
                                    el.classList.add("lam-model-tag--selected");
                                }
                            });
                            this.setSize([600, 700]);

                            
                        }
                    },
                    get: () => {
                        if(pb_cache[prompt_type.value]&&pb_cache[prompt_type.value][cat_value]&&tags.element.children[1].children.length==0){
                            let list =getTagList(pb_cache[prompt_type.value][cat_value],cat_value);
                            tags.element.children[1].append(...list)
                            tags.element.children[1].querySelectorAll(".lam-model-tag").forEach(el => {
                            if(this.properties["values"].includes(el.dataset.tag)){
                                el.classList.add("lam-model-tag--selected");
                            }
                            this.setSize([600, 700]);
                        });
                    }
                        return cat_value;
                    }
                });               
                Object.defineProperty(tags, "value", {
                    set: (x) => {
                        
                    },
                    get: () => {
                        let namestr=Object.values(this.properties["selTags"]).map(item => {
                            if(item.weight!=1) {
                                return `(${item.tag}:${item.weight})`;
                            } else {
                                return item.tag;
                            }
                        }).join(',')
                        let delList=[]
                        tags.element.children[3].querySelectorAll(".lam-model-tag--del").forEach(el => {
                            delList.push(el.dataset.tag)
                        })
                        tags.element.children[1].querySelectorAll(".lam-model-tag").forEach(el => {
                            if(el.classList.value.indexOf("lam-model-tag--selected")>=0&&!delList.includes(el.dataset.tag)){
                                if(!this.properties["values"].includes(el.dataset.tag)){
                                    this.properties["values"].push(el.dataset.tag);
                                }
                                if(!Object.keys(this.properties['selTags']).includes(el.dataset.tag)){
                                    this.properties['selTags'][el.dataset.tag]={tag:el.dataset.tag,name:el.dataset.name,cat:el.dataset.cat,weight:Number(el.dataset.weight)}
                                }
                            }else{
                                if(delList.includes(el.dataset.tag)){
                                    el.classList.remove("lam-model-tag--selected");
                                    delList=delList.filter(v=>v!=el.dataset.tag)
                                }
                                if(this.properties["values"].includes(el.dataset.tag)){
                                    this.properties["values"]=this.properties["values"].filter(v=>v!=el.dataset.tag);
                                    delete this.properties['selTags'][el.dataset.tag];
                                }
                            }
                        });
                        tags.element.children[3].querySelectorAll(".lam-model-tag").forEach(el => {
                            if(Object.keys(this.properties['selTags']).includes(el.dataset.tag)){
                                this.properties['selTags'][el.dataset.tag]={tag:el.dataset.tag,name:el.dataset.name,cat:el.dataset.cat,weight:Number(el.dataset.weight)}
                            }
                        })
                        for(let i=0;i<delList.length;i++){
                            if(this.properties["values"].includes(delList[i])){
                                this.properties["values"]=this.properties["values"].filter(v=>v!=delList[i]);
                                delete this.properties['selTags'][delList[i]];
                            }
                        }
                        tagsValue = Object.values(this.properties["selTags"]).map(item => {
                            if(item.weight!=1) {
                                return `(${item.tag}:${item.weight})`;
                            } else {
                                return item.tag;
                            }
                        }).join(',');
                        if(namestr!=tagsValue||tags.element.children[3].innerHTML==''){
                            if(Object.keys(this.properties['selTags']).length>0){
                                let sellist=getSelList(this.properties['selTags'])
                                tags.element.children[3].innerHTML=''
                                tags.element.children[3].append(...sellist)
                            }else{
                                tags.element.children[3].innerHTML=''
                            }
                        }
                        return tagsValue;
                    }
                });
                this.setSize([600, 700]);
                return r;
            };

        }
    },
});