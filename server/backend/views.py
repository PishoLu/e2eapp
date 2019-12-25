import json
import logging

from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render

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
