import json
import logging
import os

import requests  # 最好不用这个，让前端作为两个后端的跳板
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey, X25519PublicKey)
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from rest_framework import viewsets

from .models import friends, messages, user
from .serializers import UserSerializer

from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.response import Response

from rest_framework import generics

from rest_framework import mixins


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
        return JsonResponse(result)
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


# 登陆到服务器，获取好友列表即登陆IP信息。在初始化之前登陆。登录后初始化获取好友的存活信息。返回给前端列表,由于csrf的原因，登录和注册都交给前端完成，通过axios提交登录注册请求.
# 这里的登录是前端将登录成功的userid发送过来完成密钥初始化的。
# 登录是先账号密码服务器验证登录，然后后端生成新的密钥对返回给前端，前端再将服务器上的密钥对更新完成登录。
def create_new_keyspair(request):
    if request.method == "GET":
        pass
    else:
        post_data = json.dumps(request.body)
        if(post_data["userid"]):
            myself = user()
            myself.userid = post_data["userid"]
            myself.IdentityPri = X25519PrivateKey.generate()
            myself.IdentityPub = myself.IdentityPri.public_key()
            myself.SignedPri = X25519PrivateKey.generate()
            myself.SignedPub = myself.SignedPri.public_key()
            myself.OneTimePri = X25519PrivateKey.generate()
            myself.OneTimePub = myself.OneTimePri.public_key()
            myself.EphemeralPri = X25519PrivateKey.generate()
            myself.EphemeralPub = myself.EphemeralPri.public_key()

            result = {"code": 1, "data": myself.to_json(), "result": "生成新的密钥对"}
            return JsonResponse(result)
        else:
            result = {"code": -1, "data": "", "result": "需要提供userid"}
            return JsonResponse(result)


# 注册功能可以交给前端完成也可以前端发到后端再注册
def register(request):
    pass


def gettoken(request):
    if request.method == "GET":
        get_token(request)
        result = {"code": 1, "data": "", "result": "Token 获取成功!"}
        return JsonResponse(result)
    else:
        pass


@api_view(["GET", "POST"])
def user_list(request):
    """
    API endpoint that allows users to be viewed or edited.
    """
    if request.method == 'GET':
        users = user.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    Retrieve, update or delete a code user.
    """
    try:
        user_temp = user.objects.get(userid=pk)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user_temp)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user_temp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
