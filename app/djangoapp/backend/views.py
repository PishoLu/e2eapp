import json
import logging
import requests
import os

from django.http import HttpResponse
from django.shortcuts import render

from .models import user


class linked():
    def __init__(self):
        self.fromIP = ""
        self.fromPort = 0
        self.userinfo = user()  # 连接的当前使用的密钥对象F
        self.kdf_in = ""  # 连接的当前使用的kdf输入
        self.kdf_dh = ""  # 连接的当前使用的kdf dh输入
        self.status = 0


linked_list = []  # 已连接的好友列表
alive_list = []  # 存活的好友列表

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = BASE_DIR+"/log/"


# 日志类
class Logger():
    def __init__(self):
        logging.basicConfig(filename=log_path+"logging.log", filemode="a",
                            format="%(asctime)s-%(funcName)s-%(levelname)s-%(message)s", datefmt="%Y-%M-%d %H:%M:%S", level=logging.DEBUG)
        self.logger = logging.getLogger()

    def getlogger(self):
        return self.logger


logger = Logger()


# 返回自己的存活信息
def get_live(request):
    if request.method == "GET":
        logger.getlogger().info(request.META["REMOTE_ADDR"])
        result = {"code": 1, "data": "", "result": "存活"}
        return HttpResponse(json.dumps(result))
    else:
        pass


# 返回自己的公钥，服务器的信息也是包括公钥信息，所以可以用来互相对照。
def get_pubs(request):
    if request.method == "GET":
        pass
    else:
        pass


# 接收别人发来的消息
def get_message(request):
    if request.method == "GET":
        pass
    else:
        pass


# 开始连接，将连接对象存到列表中，如果没有两个kdf就开始X3DH获取到kdf初始值。
def start_X3DH(request):
    if request.method == "GET":
        pass
    else:
        pass


# 从数据库过滤某IP的消息
def filter_messages(request):
    if request.method == "GET":
        pass
    else:
        pass


# 获取好友列表的存活情况
def others_live(request):
    if request.method == "GET":
        pass
    else:
        pass


# 发送消息给其他人
def send_message(request):
    if request.method == "GET":
        pass
    else:
        pass


# 首页初始化
# 获取好友列表
# 尝试获取好友存活信息
def index_init(request):
    if request.method == "GET":
        pass
    else:
        pass


# 登陆到服务器，获取好友列表即登陆IP信息。在初始化之前登陆。登录后初始化获取好友的存活信息。返回给前端列表
def login(request):
    if request.method == "GET":
        pass
    else:
        post_data = json.loads(request.body)
        userid = post_data["userid"]
        password = post_data["password"]
        payload = {"userid": userid, "password": password}
        login_to_host = requests.post(
            "http:/127.0.0.1:8888/apis/login", data=json.dumps(payload))
        print(login_to_host.text)
