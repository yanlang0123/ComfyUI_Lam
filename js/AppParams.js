import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";
import { GroupNodeConfig, GroupNodeHandler } from "/extensions/core/groupNode.js";
import { $el, ComfyDialog } from "../../../scripts/ui.js";
import { api } from "../../../scripts/api.js";

// Displays input text on a node
const CONVERTED_TYPE = "converted-widget";
const type2paramType = {
    "STRING": "text",
    "combo": "select",
    "number": "number",
    "toggle": "toggle",
    "BOOLEAN": "switch",
    "text": "text",
    "string": "text",
    "customtext": "customtext"
}
var update_comfyui_button = null;
var switch_comfyui_button = null;
var fetch_updates_button = null;
var update_all_button = null;
let share_option = 'all';
let manager_instance = null;
$el("style", {
    textContent: `
    
/*表单样式*/
.lam_app_form {
    width: 85%;
    height:700px;
    overflow-x: auto;
    max-width: 600px;
    background-color: rgba(255, 255, 255, .05);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 0 5px #000;
    text-align: center;
    font-family: "微软雅黑";
    color: #fff;
}

/*表单标题样式*/
.lam_app_form h1 {
    margin-top: 0;
    font-weight: 200;
}

.lam_app_form .txtb {
    border: 1px solid #aaa;
    margin: 8px 0;
    padding: 12px 18px;
    border-radius: 10px;
}

.lam_app_form .txtb label {
    display: block;
    text-align: left;
    color: #fff;
    font-size: 14px;
}

/*姓名 手机 邮箱 备注框样式*/
.lam_app_form .txtb input,
.lam_app_form .txtb textarea {
    width: 100%;
    background: none;
    border: none;
    outline: none;
    margin-top: 6px;
    font-size: 18px;
    color: #fff;
}

/*备注框样式*/
.lam_app_form .txtb textarea{
    max-height: 300px;
}

/*提交按钮样式*/
.lam_app_form .btn {
    display: block;
    /* background-color: rgba(156, 39, 176, .5); */
    padding: 14px 0;
    color: #fff;
    cursor: pointer;
    margin-top: 8px;
    width: 100%;
    border: 1px solid #aaa;
    border-radius: 10px;
}
.scroll-container {
    overflow-x: auto;     /* 启用横向滚动条 ‌:ml-citation{ref="3,4" data="citationList"} */
    padding: 12px 0;      /* 垂直内边距 */
    width: 100%;          /* 容器宽度适配父元素 ‌:ml-citation{ref="2" data="citationList"} */
    gap: 15px;            /* 子元素间距 */
    list-style: none;     /* 清除默认列表样式 ‌:ml-citation{ref="6" data="citationList"} */
  }
  
  .scroll-container ol {
    align-items: center;  /* 垂直居中 */
    padding: 8px 15px;    /* 内边距 */
    background: #4f4f4f;  /* 背景色 */
    border-radius: 4px;   /* 圆角效果 */
    white-space: nowrap;  /* 禁止文本换行 ‌:ml-citation{ref="4" data="citationList"} */
  }
  
  .scroll-container span {
    margin-right: 10px;   /* 文本与按钮间距 */
    font-family: monospace; /* 等宽字体 */
  }
  
  .scroll-container button {
    padding: 3px 8px;     /* 按钮内边距 ‌:ml-citation{ref="5" data="citationList"} */
    background: #ff4444;  /* 警示色 */
    color: white;         /* 文字颜色 */
    border: none;         /* 清除边框 */
    border-radius: 3px;   /* 圆角 */
    cursor: pointer;      /* 手型指针 */
    transition: 0.2s;     /* 过渡动画 */
    font-size: smaller;
  }
  
  .scroll-container button:hover {
    background: #cc0000;  /* 悬停状态颜色 ‌:ml-citation{ref="5" data="citationList"} */
  }
  
  /* 隐藏滚动条（Webkit内核） */
  .scroll-container::-webkit-scrollbar {
    height: 0;            /* 隐藏横向滚动条 ‌:ml-citation{ref="3" data="citationList"} */
  }
  
`,
    parent: document.body,
})
let initData = {}
class ManagerMenuDialog extends ComfyDialog {

    createControlsLeft() {
        let self = this;
        let authorIds = initData?.base?.authorIds || []
        let commands = initData?.commands || []
        let authorEls = []
        for (let id of authorIds) {
            authorEls.push($el('ol', { style: { marginRight: '10px' } }, [
                $el('span', { textContent: id }),
                $el('button', {
                    textContent: '删除', dataset: { authorId: id }, $: (el) => {
                        el.onclick = () => {
                            initData.base.authorIds = authorIds.filter(id => id != el.dataset.authorId)
                            manager_instance.initElement();
                        }
                    }
                }),
            ]))
        }
        let commonEls = []
        for (let command in commands) {
            commonEls.push($el('ol', { style: { marginRight: '10px' } }, [
                $el('span', { textContent: command }),
                $el('button', {
                    textContent: '删除', dataset: { command: command }, $: (el) => {
                        el.onclick = () => {
                            delete initData.commands[command]
                            manager_instance.initElement();
                        }
                    }
                }),
            ]))
        }
        let from = $el("from", [
            $el("div.txtb", [
                $el("label", { textContent: "应用标题:" }),
                $el("input", {
                    name: "appTitle",
                    value: initData?.base?.appTitle,
                    onchange: (e) => {
                        initData.base.appTitle = e.target.value;
                    },
                }),
            ]),
            $el("div.txtb", [
                $el("label", { textContent: "应用logo:" }),
                $el("input", {
                    name: "appLogo",
                    value: initData?.base?.appLogo,
                    onchange: (e) => {
                        initData.base.appLogo = e.target.value;
                    },
                }),
            ]),
            $el("div.txtb", [
                $el("label", { textContent: "免费次数(0为无限):" }),
                $el("input", {
                    name: "freeSize",
                    value: initData?.base?.freeSize,
                    onchange: (e) => {
                        let value = e.target.value
                        if (isNaN(value)) {
                            value = 0
                        } else {
                            value = parseInt(value)
                        }
                        initData.base.freeSize = value;
                    },
                }),
            ]),
            $el("div.txtb", [
                $el("label", { textContent: "授权编号:" }, [
                    $el('button', {
                        textContent: '添加', $: (el) => {
                            el.onclick = () => {
                                //随机字符串
                                let authorId = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
                                initData.base.authorIds.push(authorId)
                                manager_instance.initElement();
                            }
                        }
                    })
                ]),
                $el("ul.scroll-container", authorEls)
            ]),
            $el("div.txtb", [
                $el("label", { textContent: "应用管理:" }),
                $el("ul.scroll-container", commonEls)
            ]),
        ])
        return [$el('div.lam_app_form', [from,
            $el('span.btn', {
                textContent: '提交', $: (el) => {
                    el.onclick = () => {
                        updateInitData()
                    }
                }
            }),
            $el('span.btn', {
                textContent: '应用预览', onclick: () => {
                    openAppPage('app')
                }
            }),
            $el('span.btn', {
                textContent: '画板预览', onclick: () => {
                    openAppPage('index')
                }
            }),
            $el('span.btn', {
                textContent: '有声绘本', onclick: () => {
                    openAppPage('pictureBook')
                }
            })
        ])];
    }

    constructor() {
        super();
        const close_button = $el("button", { id: "cm-close-button", type: "button", textContent: "Close", onclick: () => this.close() });
        const content =
            $el("div.comfy-modal-content",
                [
                    $el("tr.cm-title", {}, [
                        $el("font", { size: 6, color: "white" }, [`应用管理`])]
                    ),
                    $el("br", {}, []),
                    $el("div.cm-menu-container",
                        [
                            ...this.createControlsLeft()
                        ]),

                    $el("br", {}, []),
                    close_button,
                ]
            );

        content.style.width = '100%';
        content.style.height = '80%';
        this.element = $el("div.comfy-modal", { id: 'cm-manager-dialog', parent: document.body, style: { maxWidth: '700px', height: '800px' } }, [content]);
    }

    initElement() {
        this.element.children[0].children[2].innerHTML = ''
        this.element.children[0].children[2].appendChild(...this.createControlsLeft())
    }

    show() {
        this.initElement()
        this.element.style.display = "block";
    }
}
async function openAppPage(type='app') {
    try {
        const resp = await api.fetchApi(`/lam/getAdminNo`);
        if (resp.status === 200) {
            let data = await resp.json();
            //打开新标签页面
            window.open('/wechatauth/' + type + '?openId=' + data.data);
            return true;
        }
        throw new Error(resp.data.msg);
    } catch (error) {
        console.error(error);
    }
}

async function getAppInit() {
    try {
        const resp = await api.fetchApi(`/lam/getInitData`);
        if (resp.status === 200) {
            let data = await resp.json();
            if (data.success) {
                console.log(data)
                initData = data.data
                manager_instance.show();
            }
            return true;
        }
        throw new Error(resp.data.msg);
    } catch (error) {
        console.error(error);
    }
}

async function updateInitData() {
    try {
        let data = {
            appTitle: initData.base.appTitle,
            appLogo: initData.base.appLogo,
            freeSize: initData.base.freeSize,
            authorIds: initData.base.authorIds,
            commands: initData.commands
        }
        const response = await api.fetchApi("/lam/updateAppData", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        if (response.status === 200) {
            alert('更新成功');
            return true;
        }
        throw newError(response.data.msg);
    } catch (error) {
        console.error(error);
    }
}

async function setAppParams(data) {
    try {
        let workflow = await app.graphToPrompt();
        data['workflow'] = workflow['output']
        const response = await api.fetchApi("/lam/setAppParams", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        if (response.status === 200) {
            alert('设置成功');
            return true;
        }
        throw new Error(response.data.msg);
    } catch (error) {
        console.error(error);
    }
}
function add_param(w, appNode) {
    let typeEl = null;
    if (w.type == 'number' || w.type == 'slider') {
        typeEl = $el('td', [
            $el('select', {
                value: w.type, $: (el) => {
                    el.onchange = () => {
                        appNode.properties['paramList'].find(obj => obj.id === el.parentNode.parentNode.dataset.id).type = el.value
                    }
                }
            }, [
                $el('option', { selected: w.type == 'number', textContent: '数值输入', value: 'number' }),
                $el('option', { selected: w.type == 'slider', textContent: '数值滑条', value: 'slider' }),
            ])
        ])
    } else {
        typeEl = $el('td', { textContent: w.type })
    }
    let maskEl = null;
    let maskd = appNode.properties['paramList'].find(obj => obj.id == w?.maskKey)
    if (w.type == 'image') {
        maskEl = $el('td', [
            $el('span', {
                textContent: maskd ? '已关联:' + maskd.zhName : '关联遮罩', $: (el) => {
                    el.onclick = () => {
                        let thIndex = appNode.properties['paramList'].findIndex(obj => obj.id == el.parentNode.parentNode.dataset.id)
                        let imgs = appNode.properties['paramList'].filter(obj => obj.type === 'image' && obj.id != el.parentNode.parentNode.dataset.id)
                        let maskKey = appNode.properties['paramList'][thIndex]?.maskKey
                        if (imgs.length > 0) {
                            if (!maskKey) {
                                appNode.properties['paramList'][thIndex]['maskKey'] = imgs[0].id
                                el.innerHTML = '已关联：' + imgs[0].zhName
                            } else {
                                if (imgs.length == 1) {
                                    appNode.properties['paramList'][thIndex]['maskKey'] = null
                                    el.innerHTML = '关联遮罩'
                                } else {
                                    let imgIndex = imgs.findIndex(obj => obj.id === maskKey)
                                    if (imgIndex == -1 || imgIndex + 1 >= imgs.length) {
                                        appNode.properties['paramList'][thIndex]['maskKey'] = null
                                        el.innerHTML = '关联遮罩'
                                    } else {
                                        appNode.properties['paramList'][thIndex]['maskKey'] = imgs[imgIndex + 1].id
                                        el.innerHTML = '已关联：' + imgs[imgIndex + 1].zhName
                                    }
                                }
                            }
                        } else {
                            el.innerHTML = '关联遮罩'
                            alert('请先添加遮罩图片参数')
                        }

                    }
                }
            })
        ])
    } else {
        maskEl = $el('td')
    }

    return $el('tr', {
        dataset: {
            id: w.id,
            name: w.name,
            zhName: w.zhName,
            type: w.type,
            value: w.value
        }
    }, [
        $el('td', { textContent: w.name }),
        $el('td', {}, [
            $el('input', {
                name: w.name, value: w.zhName, $: (el) => {
                    el.onchange = () => {
                        appNode.properties['paramList'].find(obj => obj.id === el.parentNode.parentNode.dataset.id).zhName = el.value
                    }
                }
            })
        ]),
        typeEl,
        maskEl,
        $el('td', {}, [$el('button', {
            textContent: '删除', $: (el) => {
                el.onclick = () => {
                    appNode.properties['paramList'].splice(appNode.properties['paramList'].findIndex(obj => obj.id === el.parentNode.parentNode.dataset.id), 1)
                    el.parentNode.parentNode.parentNode.removeChild(el.parentNode.parentNode)
                }
            }
        }
        )]),
    ])
}
app.registerExtension({
    name: "AppParams",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        var names = ["AppParams"]
        if (names.indexOf(nodeData.name) >= 0) {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated?.apply(this, arguments);
                this.setProperty("paramList", [])
                const list = $el("table.lam_app_params_list", [
                    $el('tr', [
                        $el('td', { textContent: '参数名' }),
                        $el('td', { textContent: '中文名' }),
                        $el('td', { textContent: '组件类型' }),
                        $el('td', { textContent: '绘制遮罩' }),
                        $el('td', { textContent: '操作' }),
                    ])
                ]);
                let params = this.addDOMWidget('styles', "list", $el('div.lam_app_param_div', [$el('button', {
                    textContent: '应用预览',
                    style: {},
                    onclick: () => {
                        let appType = this.widgets[this.widgets.findIndex(obj => obj.name === 'appType')];
                        openAppPage(appType.value)
                    }
                }), $el('button', {
                    textContent: '参数应用',
                    style: {},
                    onclick: () => {
                        let paramList = this.properties['paramList']
                        let appName = this.widgets[this.widgets.findIndex(obj => obj.name === 'appName')];
                        let appType = this.widgets[this.widgets.findIndex(obj => obj.name === 'appType')];
                        let appDesc = this.widgets[this.widgets.findIndex(obj => obj.name === 'appDesc')];

                        if (!appName.value) {
                            alert('请输入应用名称');
                            return;
                        }
                        if (paramList.length <= 0) {
                            alert('请至少选择一个参数');
                            return;
                        }
                        let data = { appName: appName.value, appType: appType.value, appDesc: appDesc.value, paramList: paramList }
                        setAppParams(data)
                    }
                }), list]));
                this.setSize([500, 600]);
                return r;
            };
        }
    },
    loadedGraphNode(node, _) {
        if (node.type === "AppParams") {
            node.properties['paramList'].forEach(el => {
                node.widgets[3].element.children[2].appendChild(add_param(el, node))
            });
        }
    },
});

async function addConvertToGroupOptions() {
    // Add to nodes
    const getNodeMenuOptions = LGraphCanvas.prototype.getNodeMenuOptions;
    LGraphCanvas.prototype.getNodeMenuOptions = function (node) {
        const options = getNodeMenuOptions.apply(this, arguments);
        if (!GroupNodeHandler.isGroupNode(node) && node.type != 'AppParams' && node.widgets) {
            let toInput = [];
            let wNames = node.inputs.filter(obj => obj.widget !== undefined && obj.link === null).map(obj => obj.name);
            for (const w of node.widgets) {
                if (w.options?.forceInput || !wNames.includes(w.name)) {
                    continue;
                }
                if (w.type !== CONVERTED_TYPE) {
                    toInput.push({
                        content: `添加 ${w.label} 到输入参数`,
                        callback: async () => {
                            console.log(w)
                            let nodes = graph.computeExecutionOrder(false)
                            let appNode = nodes[nodes.findIndex(obj => obj.type === 'AppParams')]
                            if (!appNode) {
                                alert('请先添加AppParams节点');
                                return;
                            }
                            let appTypeEl = appNode.widgets[appNode.widgets.findIndex(obj => obj.name === 'appType')];
                            if (!w.type in type2paramType) {
                                return;
                            }
                            let paramData = { id: 'n' + node.id + '_' + w.name, keys: ['' + node.id, 'inputs', w.name], name: w.name, zhName: w.label, type: w.type, default: w.value, isRequired: false }
                            if (w.type == 'number') {
                                paramData['min'] = w.options.min
                                paramData['max'] = w.options.max
                                paramData['step'] = w.options.round
                            } else if (w.type == 'toggle' || w.type == 'boolean' || w.type == 'BOOLEAN') {
                                paramData['type'] = 'switch'
                                paramData['onVal'] = true
                                paramData['offVal'] = false
                            } else if (w.type == 'STRING') {
                                paramData['type'] = 'text'
                            } else if (w.type == 'combo') {
                                paramData['type'] = 'select'
                                let values = w.options.values
                                paramData['options'] = {}
                                for (let i = 0; i < values.length; i++) {
                                    paramData['options'][values[i]] = values[i]
                                }
                            }
                            if (node.type == "LamLoadPathImage" && w.name == 'image_path') {
                                paramData['type'] = 'image'
                                paramData['default'] = ''
                            } else if (node.type == "LamLoadImageBase64" && w.name == 'image') {
                                paramData['type'] = 'base64img'
                                paramData['isRequired'] = true
                            } else if (w.name == 'seed') {
                                paramData['type'] = 'seed'
                                if (appTypeEl.value == 'paint-board') {
                                    paramData['default'] = -1
                                }
                            } else if (w.name == 'batch_size') {
                                paramData['type'] = 'number'
                            } else if (w.name == 'denoise') {
                                paramData['type'] = 'slider'
                                if (appTypeEl.value == 'paint-board') {
                                    paramData['min'] = 0
                                    paramData['max'] = 100
                                    paramData['step'] = 1
                                    paramData['original'] = 1
                                }
                                paramData['default'] = parseFloat(paramData['default'].toFixed(2))
                            }

                            let index = appNode.properties['paramList'].findIndex(obj => obj.id === paramData.id)
                            if (index >= 0) {
                                return;
                            }
                            appNode.properties['paramList'].push(paramData)
                            let tr = add_param(paramData, appNode)
                            appNode.widgets[3].element.children[2].appendChild(tr)
                        }
                    });
                }
            }
            const index = options.findIndex((o) => o?.content === "Outputs") + 1 || options.length - 1;
            toInput.length > 0 && options.splice(index + 1, null, {
                content: `设置应用参数`,
                submenu: {
                    options: toInput
                }
            });
        }
        return options;
    };

    let cmGroup = new (await import("../../scripts/ui/components/buttonGroup.js")).ComfyButtonGroup(
        new (await import("../../scripts/ui/components/button.js")).ComfyButton({
            icon: "puzzle",
            action: () => {
                if (!manager_instance) {
                    manager_instance = new ManagerMenuDialog();
                }
                getAppInit()
            },
            tooltip: "应用管理器",
            content: "应用管理器",
            classList: "comfyui-button comfyui-menu-mobile-collapse primary"
        }).element
    );
    app.menu?.settingsGroup.element.before(cmGroup.element);

}

const id = "Lam.AppParams";
const ext = {
    name: id,
    async setup() {
        addConvertToGroupOptions();
    },
    // async beforeConfigureGraph(graphData, missingNodeTypes) {
    //     await getGroupNode(missingNodeTypes);
    // },
    // addCustomNodeDefs(defs) {
    //     // Store this so we can mutate it later with group nodes
    //     globalDefs = defs;
    // },
    // nodeCreated(node) {
    //     if (!GroupNodeHandler.isGroupNode(node)) {
    //     }
    // },
};

app.registerExtension(ext);