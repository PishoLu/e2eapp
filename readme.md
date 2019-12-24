# 项目结构
- 客户端
  - Electron 项目包
  - Electron 相关 Node 库
    - Django 后端
      - Vue 前端（生成静态文件给 Django 使用）
      - Vue相关 Node 库
    - Django 静态文件夹
- 服务器

- 服务器后端 Django 项目

## 项目运行

首先确保 node 库安装完成，前端需要在 Vue 文件夹内将前端所需库下载下来。然后是 Electron 的所需要的库。

然后 Django 所需的库需要用 Python 下载

### 注意事项
Django 关闭 Debug 模式后可能会找不到静态文件