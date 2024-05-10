import { app } from "/scripts/app.js";
import { $el } from "../../../scripts/ui.js";
import { ComfyWidgets } from "/scripts/widgets.js";
import { api } from "../../../scripts/api.js";
//background-image: url("http://alexfeds.com/wp-content/uploads/2018/04/save_icon.svg");
$el("style", {
	textContent: `
    .lam_btn {
        border: none;
        color: grey;
        padding: 12px 12px;
        background-color: #494848;
        font-size: 16px;
        cursor: pointer;
        background-repeat: repeat-y;
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
    name: "LamAllInOne",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
		var names=['LamAllInOne']
        if (names.indexOf(nodeData.name)>=0) {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated?.apply(this, arguments);
                this.widgets.splice(this.widgets.findIndex(obj => obj.name === 'prompt'),1);
                this.widgets.splice(this.widgets.findIndex(obj => obj.name === 'negative'),1);
                const promptText = $el("textarea.comfy-multiline-input.dynamic_prompt",{
                    placeholder:"正向提示词",
                    style:{
                        width: '100%',
                        height: '50%'  
                    }
                });
                const btn1=$el('i.lam_btn',{
                    style:{'mask-image':'url(/lam/getImage?type=icons&&name=close.svg)'}
                })
                const prompt =this.addDOMWidget('prompt',"list",$el("div",[promptText,btn1]))
                const negative =this.addDOMWidget('negative',"list",$el("div",[]))

                this.setSize([700, 800]);
                return r;
            }

        }
    },
});