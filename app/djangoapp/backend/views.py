from django.shortcuts import render
from .models import user

from django.http import HttpResponse


class linked:
    def __init__(self):
        self.fromIP = ""
        self.fromPort = 0
        self.userinfo = user()


linked_list = []


# 获取存活信息
def get_live(requests):
    pass


# 获取公钥
def get_pubs():
    pass


# 接收消息
def get_message():
    pass


# 开始连接，将连接对象存到列表中
def start_X3DH():
    pass


# 从数据库过滤某IP的
def filter_messages():
    pass
