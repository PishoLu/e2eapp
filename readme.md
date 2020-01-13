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

| 接口名          | 方法 | 字段                 | 返回值                     | 备注                                                   |
| --------------- | ---- | -------------------- | -------------------------- | ------------------------------------------------------ |
| get_live        | GET  | 无                   | 存活返回 1，不存活无法返回 |                                                        |
| get_message     | POST | message<br />pub     | 成功接收返回1              | 该接口接收密文并解密保存到数据库。通过操作可以添加好友 |
| filter_messages | GET  | id，num              | 通过ID查询该ID下的所有消息 | num是上一次查询的末尾记录数。防止重复消息              |
| friends_list    | GET  | 无                   | 返回自己的所有好友信息     | 返回好友列表让前端去完成存活确认                       |
| decrypt_message | POST | 目标ID，密文         | 返回解密的明文             | 通过密钥解密                                           |
| encrypt_message | POST | 目标ID，明文         | 返回加密的密文             | 查询是否连接X3DH，返回加密密文。                       |
| sotre_message   | POST | 目标ID，明文         | 无                         | 保存消息到数据库                                       |
| sotre_user      | POST | 目标信息或自身的信息 | 无                         | 保存User类信息                                         |

## 服务器接口

| 接口名         | 方法 | 字段                           | 返回值                               | 备注           |
| -------------- | ---- | ------------------------------ | ------------------------------------ | -------------- |
| user/pk        | GET  | 无                             | 返回该 userid 下的可被他人访问的信息 | 返回是否为好友 |
| user/pk        | POST | password                       | 对比 password 返回结果               | 登录接口       |
| user/          | POST | username,password,pubs         | 注册结果                             | 注册接口       |
| user/pk        | PUT  | username,pubs                  | 更新 username，pub                   |                |
| message_detail | POST | fromUserid,toUserid,ciphertext | 是否保存成功                         | 消息上传接口   |
| message_detail | GET  | logining_userid                | 查询是否有已登录用户的消息暂存记录   | 获取自己的消息 |

## 前端逻辑

注册：/apis/user/ **POST**

| 字段     | 备注                   |
| -------- | ---------------------- |
| username |                        |
| password | 前端对password完成hash |

服务器随机生成userid并返回，

登录：/apis/user/userid **GET**

| 字段     | 备注 |
| -------- | ---- |
| userid   |      |
| password |      |

登录后在主页操作

好友：

- 在本地获取好友列表。
- 添加好友通过服务器搜索结果并添加好友的公钥到数据库。

发送消息：

- 查询是否有该好友的公钥信息
- 通过 encrypt_message 接口加密信息
- 上传到服务器
- 保存到本地数据库

接收消息：

- 从服务器获取自己的暂存信息
- 给后端解析分析是否是好友
- 前端决定是否添加为好友
- 解密消息返回
- 保存到数据库


