from django.shortcuts import render
from .models import user

from django.http import HttpResponse


class linked:
    def __init__(self):
        self.fromIP = ""
        self.fromPort = 0
        self.userinfo = user()  # 连接的当前使用的密钥对象F
        self.kdf_in = ""  # 连接的当前使用的kdf输入
        self.kdf_dh = ""  # 连接的当前使用的kdf dh输入


linked_list = []
alive_list = []


# 获取好友列表
def get_friends_lsit():
    pass


# 返回自己的存活信息
def get_live(requests):
    pass


# 返回自己的公钥
def get_pubs():
    pass


# 接收别人发来的消息
def get_message():
    pass


# 开始连接，将连接对象存到列表中
def start_X3DH():
    pass


# 从数据库过滤某IP的消息
def filter_messages():
    pass


# 获取好友列表的存活情况
def others_live():
    pass


# 发送消息给其他人
def send_message():
    pass


# 首页初始化
# 获取好友列表
# 尝试获取好友存活信息
def index_init():
    pass
