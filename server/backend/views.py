from django.shortcuts import render
from django.http import HttpResponse
import json
import logging
# Create your views here.

log_path = "./log/"


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
        return HttpResponse(1)


def register(request):
    if request.method == "GET":
        pass
    else:
        pass
