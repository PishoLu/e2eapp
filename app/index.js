const {
    app,
    BrowserWindow
} = require("electron")

// 创建窗口
function createWindow() {
    let win = new BrowserWindow({
        width: 800,
        height: 600
    })
    // 加载 "templates/flask_welcome.html"
    win.loadURL("http://127.0.0.1:8000/")
}


// 使用 python-shell 调用 engine.py
const {
    PythonShell
} = require("python-shell")

let options = {
    mode: 'text',
    args: ['runserver', '0.0.0.0:8000']
};
PythonShell.run('djangoapp/manage.py', options, function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    console.log('results: %j', results);
});




// 启动
app.on("ready", createWindow)