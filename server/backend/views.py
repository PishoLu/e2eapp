import json
import logging
import os

from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import user
from .serializers import UserSerializer
# Create your views here.

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


def get_info(request):
    if request.method == "GET":
        pass
    else:
        pass


def login(request):
    if request.method == "GET":
        pass
    else:
        post_data = json.loads(request.body)
        print(post_data)
        result = {"code": 1, "data": "", "result": "登录成功！"}
        return HttpResponse(json.dumps(result))


def register(request):
    if request.method == "GET":
        pass
    else:
        pass


def gettoken(request):
    if request.method == "GET":
        token = get_token(request)
        result = {"code": 1, "data": token, "result": "Token 获取成功!"}
        return HttpResponse(json.dumps(result))
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
