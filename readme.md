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

# 接口设置

## 客户端接口

| 接口名          | 方法 | 字段             | 返回值                       | 备注                                                         |
| --------------- | ---- | ---------------- | ---------------------------- | ------------------------------------------------------------ |
| get_live        | GET  | 无               | 存活返回 1，不存活无法返回   |                                                              |
| get_pubs        | GET  | 无               | 返回自己的三种公钥           |                                                              |
| get_message     | POST | message<br />pub | 成功接收返回1                | 该接口接收密文和公钥并解密保存到数据库。                     |
| start_X3DH      | POST | pubs             | 完成X3DH返回1，未完成返回0   | 该接口通过双方交互公钥完成密钥认证并将对方添加到已连接的列表初始化KDF输入 |
| filter_messages | GET  | id，num          | 通过ID查询该ID下的所有消息   | num是上一次查询的末尾记录数。防止重复消息                    |
| others_live     | GET  | 无               | 返回自己的所有好友的存活信息 | 后端先访问服务器更新好友列表然后再逐个访问是否存活并返回存活信息 |



## 服务器接口

| 接口名  | 方法 | 字段                   | 返回值                               | 备注           |
| ------- | ---- | ---------------------- | ------------------------------------ | -------------- |
| user/   | GET  | 无                     | 返回所有 user 的信息                 | 后期不会使用了 |
| user/pk | GET  | 无                     | 返回该 userid 下的可被他人访问的信息 |                |
| user/pk | GET  | password               | 对比 password 返回结果               | 登录接口       |
| user/   | POST | username,password,pubs | 注册结果                             | 注册接口       |
| user/pk | PUT  | username,pubs          | 更新 username 或者 pub               |                |

## 前端逻辑

注册：/apis/user/ **POST**

登录：/apis/user/userid **GET**

| 字段     | 备注 |
| -------- | ---- |
| userid   |      |
| password |      |

