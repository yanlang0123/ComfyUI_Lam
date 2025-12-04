function formatTime(seconds) {
    const days = Math.floor(seconds / (3600 * 24));
    seconds -= days * 3600 * 24;
    const hours = Math.floor(seconds / 3600);
    seconds -= hours * 3600;
    const minutes = Math.floor(seconds / 60);
    seconds -= minutes * 60;

    const formattedDays = days > 0 ? days + ':' : '';
    const formattedHours = hours.toString().padStart(2, '0') + ':';
    const formattedMinutes = minutes.toString().padStart(2, '0') + ':';
    const formattedSeconds = seconds.toString().padStart(2, '0') + '';

    return formattedDays + formattedHours + formattedMinutes + formattedSeconds;
}

function getParams(url) {
    const regex = /[?&]([^=#]+)=([^&#]*)/g;
    const params = {};
    let match;
    while (match = regex.exec(url)) {
        params[decodeURIComponent(match[1])] = decodeURIComponent(match[2]);
    }
    return params;
}

let openId = window.APP_CONFIG.openId;

const app = Vue.createApp({
    data() {
        return {
            commandList: [],
            activeKey: '',
            paramList: [],
            brushSize: 20,
            canvas: null,
            dialogVisible: false,
            dialogImageUrl: '',
            dialogImageName: '',
            maskKey: '',
            historyList: [],
            queue_remaining: 0,
            page_number: 1,
            noMore: false,
            loading: false,
            disabled: false,
            isNotData: false,
            isConnect: false,
            isSuccess: false,
            authVisible: false,
            authCode: '',
            authMessage: '',
            form: {
                openId: '',
                command: '',
                status: "prepare",
                prompt_id: '',
                percenStatus: 'warning',
                percentage: 0,
                output: { images: [], texts: [] },
                nodeIds: [],
                doneNodeIds: []
            }
        }
    },
    mounted: function () {
        if (openId) {
            this.initMain();
        } else {
            this.authUser();
        }
    },
    watch: {
        loading(newVal, oldVal) {
            this.disabled = (newVal || this.noMore)
        },
        noMore(newVal, oldVal) {
            this.disabled = (newVal || this.loading)
        },
    },
    created() {

    },
    methods: {
        initMain() {
            this.loadData();
            document.getElementById("app").style.display = "block";
            this.initWebSocket();
            this.getHistorys();
        },
        authUser(msg = '') {
            this.authMessage = msg;
            this.authVisible = true;
        },
        submitAuth() {
            let that = this;
            if (this.authCode.length != 6) {
                this.authMessage = '验证码长度不正确！';
                return;
            }
            this.getUserOpenId(this.authCode);
        },
        isShowAdmin() {
            if ('pywebview' in window) {
                if (pywebview.api.isLogin()) {
                    return true;
                }
            }
            return false;
        },
        initWebSocket() {
            var that = this;
            var websocket = null;
            //var socketId = "ws-" + new Date().getTime();
            // 判断当前浏览器是否支持WebSocket， springboot是项目名
            if ('WebSocket' in window) {
                var host = window.location.host;
                websocket = new WebSocket("ws://" + host + '/ws?clientId=' + openId);
            } else {
                console.error("不支持WebSocket");
            }
            // 连接发生错误的回调方法
            websocket.onerror = function (e) {
                console.error("WebSocket连接发生错误");
            };
            // 连接成功建立的回调方法
            websocket.onopen = function () {
                // 获取所有在线用户
                console.log("WebSocket连接成功");
                that.isConnect = true;

            }
            // 接收到消息的回调方法
            websocket.onmessage = async function (event) {
                if (event.data == null || event.data == "" || event.data instanceof Blob) {
                    return;
                }
                var messageJson = eval("(" + event.data + ")");
                if (messageJson['type'] == 'crystools.monitor') {
                    return
                }
                console.log('messageJson', messageJson)
                if (messageJson['type'] == "status") {
                    that.queue_remaining = messageJson['data']['status']['exec_info']['queue_remaining'];
                } else if (messageJson['type'] == "execution_start") {
                    if (that.form.prompt_id == messageJson['data']['prompt_id']) {
                        that.form.percenStatus = 'success';
                    }
                } else if (messageJson['type'] == "execution_cached") {
                    if (that.form.prompt_id == messageJson['data']['prompt_id']) {
                        that.form.doneNodeIds = messageJson['data']['nodes'];
                    }
                } else if (messageJson['type'] == "executing") {
                    if (that.form.prompt_id == messageJson['data']['prompt_id']) {
                        let node = messageJson['data']['node'];
                        if (that.form.executing) {
                            that.form.doneNodeIds.push(that.form.executing);
                        }
                        if (!messageJson['data']['node']) {
                            that.form.status = 'prepare';
                            that.form.percenStatus = 'warning';
                            that.form.percentage = 0;
                            that.form.executing = '';
                            that.form.doneNodeIds = [];
                            that.form.nodeIds = [];
                            if (that.isSuccess) {
                                that.isSuccess = false
                                setTimeout(() => {
                                    that.page_number = 1;
                                    that.getHistorys();
                                }, 1000)
                            }
                        } else {
                            that.form.executing = node;
                        }
                    }
                } else if (messageJson['type'] == 'progress') {
                    if (that.form.prompt_id == messageJson['data']['prompt_id']) {
                        let max = messageJson['data']['max'];
                        let value = messageJson['data']['value'];
                        let node = messageJson['data']['node'];
                        let percentage = 0;
                        if (that.form.executing == node) {
                            percentage = parseFloat(value / max);
                        }
                        that.form.percentage = parseInt((that.form.doneNodeIds.length + percentage) / that.form.nodeIds.length * 100);
                    }
                } else if (messageJson['type'] == 'execution_success') {
                    if (that.form.prompt_id == messageJson['data']['prompt_id']) {
                        that.isSuccess = true;
                    }
                } else if (messageJson['type'] == 'executed') {
                    if (that.form.prompt_id == messageJson['data']['prompt_id']) {
                        let node_output = 'output' in messageJson['data'] ? messageJson['data']['output'] : {};
                        let images = [];
                        let texts = [];
                        if ('outputImg' in node_output) {
                            for (let img of node_output?.outputImg) {
                                let url = '../view?filename=' + img.filename + '&type=' + img.type + '&subfolder=' + img.subfolder + '&rand=' + Math.random();
                                images.push(url)
                            }
                        } else if ("wechat_text" in node_output) {
                            texts.push(...node_output.wechat_text);
                        }
                        if (images.length > 0 || texts.length > 0) {
                            that.form.output = { images: images, texts: texts };
                        }
                    }
                }
            }

            // 连接关闭的回调方法
            websocket.onclose = function () {
                console.error("WebSocket连接关闭");
                that.openCloseMsg();
            }
        },
        openCloseMsg() {
            var that = this;
            that.isConnect = false;
            ElementPlus.ElMessage({
                showClose: true,
                duration: 0,
                message: '服务器断开连接，关闭消息尝试重连',
                type: 'error',
                onClose: () => {
                    that.initWebSocket();
                }
            })
        },
        loadData() {
            var that = this;
            axios.get('../wechatauth/getCommands')
                .then(function (response) {
                    console.log(response);
                    if (response.status == 200) {
                        that.commandList = response.data;
                        that.clickTab(Object.keys(response.data)[0])
                    }
                })
                .catch(function (error) {
                    console.log(error);
                    ElementPlus.ElMessage.error(error);
                })
        },
        clickTab(key) {
            this.activeKey = key;
            if (this.commandList[key]) {
                this.paramList = this.commandList[key].params;
                for (let paramKey in this.paramList) {
                    this.paramList[paramKey]['value'] = this.paramList[paramKey]?.default;
                    if (this.paramList[paramKey].type == 'image') {
                        this.paramList[paramKey]['fileList'] = [];
                    }
                }
            }
        },
        clearValue(param) {
            param.value = '';
        },
        refreshSeed(param) {
            param.value = Math.floor(Math.random() * 1000000000000000);
        },
        handlePictureCardPreview(uploadFile, maskKey) {
            this.dialogImageUrl = uploadFile.url;
            this.dialogImageName = uploadFile.name;
            this.dialogVisible = true;
            this.maskKey = maskKey;
            if (this.maskKey) {
                this.initCanvas(uploadFile.url);
            } else {
                this.canvas = null;
            }
        },
        handleRemove(uploadFile, paramKey) {
            this.paramList[paramKey]['value'] = '';
        },
        beforeAvatarUpload(rawFile) {
            // 判断文件格式不为图片的
            if (rawFile.type !== 'image/png' && rawFile.type !== 'image/jpg' && rawFile.type !== 'image/jpeg') {
                ElementPlus.ElMessage.error('请上传图片文件!');
                return false
            }
            // else if (rawFile.size / 1024 / 1024 > 2) {
            //     ElementPlus.ElMessage.error('Avatar picture size can not exceed 2MB!')
            //     return false
            // }
            return true
        },
        updateSuccess(data, paramKey) {
            this.paramList[paramKey]['value'] = data.subfolder ? (data.type + '/' + data.name) : (data.type + '/' + data.subfolder + '/' + data.name)
        },
        changeSize(value) {
            this.canvas.freeDrawingBrush.width = parseInt(value);
        },
        clearCanvas() {
            this.canvas.clear();
            this.initCanvas(this.dialogImageUrl);
        },
        saveCanvas() {
            let that = this;
            // 清除背景图
            that.canvas.backgroundImage = null;
            that.canvas.backgroundColor = 'rgba(0,0,0,0)'
            that.canvas.renderAll();
            that.canvas.lowerCanvasEl.toBlob(function (blob) {
                let formData = new FormData();
                formData.append("image", blob, 'mask_' + openId + that.dialogImageName);
                formData.append("overwrite", "true");
                formData.append("type", "input");
                axios.post('../upload/image', formData)
                    .then(function (response) {
                        let data = response.data;
                        data['url'] = '../view?filename=' + data.name + '&type=input&subfolder=&rand=' + Math.random();
                        that.paramList[that.maskKey]['fileList'] = [data];
                        that.paramList[that.maskKey]['value'] = data.subfolder ? (data.type + '/' + data.name) : (data.type + '/' + data.subfolder + '/' + data.name);
                        that.initCanvas(that.dialogImageUrl);
                    })
                    .catch(function (error) {
                        console.log(error);
                        ElementPlus.ElMessage.error(error);
                    })
            }, "image/png");
        },
        initCanvas(backgroundUrl) {
            var that = this;
            fabric.Image.fromURL(backgroundUrl, (img) => {
                if (that.canvas == null) {
                    that.canvas = new fabric.Canvas("canvas", {
                        backgroundColor: "#FFFFFF",
                        isDrawingMode: true,
                    });
                    let freeDrawingBrush = new fabric.PencilBrush(that.canvas);
                    // Set initial brush settings
                    freeDrawingBrush.width = that.brushSize;
                    freeDrawingBrush.color = '#000000';
                    // Enable free drawing mode on canvas
                    that.canvas.isDrawingMode = true;
                    that.canvas.freeDrawingBrush = freeDrawingBrush;
                }
                let parentWidth = document.querySelector(".mask_edit_btn").clientWidth;
                let bili = img.width / parentWidth;
                let imgHeight = img.height / bili;
                that.canvas.setWidth(parentWidth);
                that.canvas.setHeight(imgHeight);
                that.canvas.setBackgroundImage(img, that.canvas.renderAll.bind(that.canvas), {
                    scaleX: that.canvas.width / img.width,
                    scaleY: that.canvas.height / img.height,
                });
                that.canvas.renderAll();
            });
        },
        getUserOpenId(code) {
            let that = this;
            let formData = new FormData();
            formData.append("code", code);
            axios.post('../wechatauth/getUserOpenId', formData)
                .then(function (response) {
                    if (response.data.success) {
                        openId = response.data.openId;
                        that.authVisible = false; // Close dialog
                        that.initMain();
                        if ('pywebview' in window) {
                            pywebview.api.setOpenId(openId);
                        }
                    } else {
                        that.authMessage = '授权码校验失败，请先扫码关注获取授权码！';
                    }
                })
                .catch(function (error) {
                    console.log(error);
                    that.authMessage = error.message || 'Unknown error';
                })
        },
        cancelTask() {
            let that = this;
            let formData = new FormData();
            formData.append("openId", openId);
            formData.append("prompt_id", that.form.prompt_id)
            axios.post('../wechatauth/cancelTask', formData)
                .then(function (response) {
                    if (response.data.success) {
                        that.form.prompt_id = '';
                        that.form.nodeIds = [];
                        that.form.status = 'prepare';
                        that.form.percenStatus = 'warning';
                        that.form.percentage = 0;
                    } else {
                        ElementPlus.ElMessage.error(response.data.msg);
                    }
                })
                .catch(function (error) {
                    console.log(error);
                    ElementPlus.ElMessage.error(error);
                })
        },
        startTask() {
            let that = this;
            if (that.form.status !== 'prepare') {
                ElementPlus.ElMessage.info('任务<' + that.form.command + '>正在运行，请勿重复操作！')
                return;
            }
            let formData = new FormData();
            formData.append("openId", openId);
            formData.append("command", this.activeKey);
            formData.append("status", "prepare");
            that.form.openId = openId;
            that.form.command = this.activeKey;
            that.form.status = "prepare";
            for (let paramKey in this.paramList) {
                if (this.paramList[paramKey]?.value) {
                    formData.append(paramKey, this.paramList[paramKey]?.value);
                }
            }
            axios.post('../wechatauth/addTask', formData)
                .then(function (response) {
                    console.log(response);
                    if (response.data.success) {
                        that.form.status = 'waiting';
                        that.form.prompt_id = response.data.prompt_id;
                        that.form.nodeIds = response.data.nodeIds;
                    } else {
                        ElementPlus.ElMessage.error(response.data.msg);
                    }
                })
                .catch(function (error) {
                    console.log(error);
                    ElementPlus.ElMessage.error(error);
                })
        },
        confirmSetParam(params) {
            let that = this;
            this.clickTab(params.command);
            for (let paramKey in this.paramList) {
                if (params[paramKey]) {
                    if (typeof params[paramKey] == 'string' && params[paramKey] == 'undefined') {
                        this.paramList[paramKey].value = '';
                    } else if (this.paramList[paramKey].type == 'slider'
                        || this.paramList[paramKey].type == 'number') {
                        this.paramList[paramKey].value = parseFloat(params[paramKey]);
                    } else {
                        if (this.paramList[paramKey].type == 'image') {
                            let ps = params[paramKey].split('//');
                            let url = '../view?filename=' + ps[1] + '&type=' + ps[0] + '&subfolder=&rand=' + Math.random();
                            //获取文件名称
                            this.paramList[paramKey].fileList = [{ url: url, name: ps[1] }];
                        }
                        this.paramList[paramKey].value = params[paramKey];
                    }
                }
            }
        },
        async handleDownload(imgs, name) {
            let that = this;
            var zip = new JSZip();
            for (let img of imgs) {
                let fileName = img.filename;
                let { data } = await axios({
                    method: 'get',
                    url: img.url,
                    responseType: 'blob',
                });
                zip.file(fileName, data);
            }
            zip.generateAsync({ type: 'blob' }).then(function (content) {
                let url = window.URL.createObjectURL(content);
                that.downloadFile(url, name);
            });
        },
        downloadFile(url, name) {
            let a = document.createElement('a');
            a.href = url;
            a.download = name;
            a.click();
        },
        loadHistory() {
            let that = this;
            if (this.isNotData) {
                this.noMore = true;
                setTimeout(() => {
                    this.noMore = false;
                }, 1000)
                return;
            }
            that.page_number += 1;
            that.getHistorys();
        },
        setRunTask(dataStr, prompt_id) {
            let that = this;
            let params = JSON.parse(dataStr)
            this.confirmSetParam(params)
            axios.get('../api/queue')
                .then(function (response) {
                    let queue_pending = response.data.queue_pending;
                    let queue_running = response.data.queue_running;
                    for (let data of queue_running) {
                        if (data[1] == prompt_id) {
                            that.form.status = 'waiting';
                            that.form.prompt_id = prompt_id;
                            that.form.percenStatus = 'success';
                            that.form.nodeIds = Object.keys(data[2]);
                            return;
                        }
                    }
                    for (let data of queue_pending) {
                        if (data[1] == prompt_id) {
                            that.form.status = 'waiting';
                            that.form.prompt_id = prompt_id;
                            that.form.nodeIds = Object.keys(data[2]);
                            return;
                        }
                    }
                }).catch(function (error) {
                    console.log(error);
                    ElementPlus.ElMessage.error(error);
                })

        },
        getHistorys() {
            let that = this;
            that.loading = true;
            axios.get('../wechatauth/getHistorys?openId=' + openId + '&page_number=' + that.page_number)
                .then(function (response) {
                    console.log(response);
                    if (that.page_number == 1) {
                        that.isNotData = false;
                        that.historyList = [];
                    }
                    let datas = response.data;
                    if (datas.length > 0 && datas[0][5] == 'waiting') {
                        that.setRunTask(datas[0][3], datas[0][4])
                    }
                    for (let res of datas) {
                        let command = JSON.parse(res[3])
                        if (res[5] == 'waiting') {
                            continue
                        } else if (res[5] == 'wcomplete') {
                            command['status'] = 'wcomplete'
                            let outputs = JSON.parse(res[8])
                            let images = [];
                            let texts = [];
                            let files = [];
                            for (let node_id in outputs) {
                                let node_output = outputs[node_id]
                                if (Object.keys(node_output).indexOf("outputImg") >= 0) {
                                    for (let img of node_output?.outputImg) {
                                        let url = '../view?filename=' + img.filename + '&type=' + img.type + '&subfolder=' + img.subfolder + '&rand=' + Math.random();
                                        images.push(url)
                                        img['url'] = url;
                                        files.push(img);
                                    }
                                } else if (Object.keys(node_output).indexOf("wechat_text") >= 0) {
                                    texts.push(...node_output.wechat_text);
                                }

                            }
                            that.historyList.push({ 'prompt_id': res[4], 'command': command, 'images': images, 'files': files, 'status': res[5], 'texts': texts })
                        }
                    }
                    if (datas.length < 10) {
                        that.isNotData = true;
                    }
                    that.loading = false;
                }).catch(function (error) {
                    console.log(error);
                    ElementPlus.ElMessage.error(error);
                })
        }
    },
    setup() {

    }
})

// use ElementPlus and ElementPlusIconsVue
app.use(ElementPlus)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

// use VueI18n
const browserLanguage = navigator.language || navigator.userLanguage; // zh-CN en-US
const languageTag = browserLanguage.split('-')[0]; // zh en
const i18n = VueI18n.createI18n({
    legacy: false, // you must set `false`, to use Composition API
    locale: languageTag, // set locale
    fallbackLocale: 'en', // set fallback locale
    messages: {},
})
app.use(i18n)
function loadLocaleMessages(locale) {
    return axios.get(`static/locales/${locale}.json`).then(response => {
        return response.data;
    });
}
async function loadLocales() {
    const locales = ['en', 'zh'];
    await Promise.all(
        locales.map(async (locale) => {
            const messages = await loadLocaleMessages(locale);
            i18n.global.setLocaleMessage(locale, messages);
        })
    );
}
loadLocales().then(() => {
    app.mount('#app');
});
