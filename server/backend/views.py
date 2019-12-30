import json
import logging
import os
import random

from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from .models import user
from .serializers import UserSerializer

# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = BASE_DIR + "/log/"


# 日志类
class Logger():
    def __init__(self):
        logging.basicConfig(filename=log_path + "logging.log", filemode="a",
                            format="%(asctime)s-%(funcName)s-%(levelname)s-%(message)s", datefmt="%Y-%M-%d %H:%M:%S",
                            level=logging.DEBUG)
        self.logger = logging.getLogger()

    def getlogger(self):
        return self.logger


logger = Logger()


def gettoken(request):
    if request.method == "GET":
        token = get_token(request)
        result = {"code": 1, "data": token, "result": "Token 获取成功!"}
        return HttpResponse(json.dumps(result))
    else:
        pass


@csrf_exempt
@api_view(["POST"])
def user_list(request):
    # 注册接口
    if request.method == 'POST':
        post_data = request.data.copy()
        if (len(post_data["password"]) == 64):
            post_data["userid"] = random.randint(10000000, 100000000)

            user.objects.create(userid=post_data["userid"],
                                password=post_data["password"],
                                username=post_data["username"],
                                IdentityPub=post_data["IdentityPub"],
                                SignedPub=post_data["SignedPub"],
                                OneTimePub=post_data["OneTimePub"])

            result = {"code": 1,
                      "data": post_data["userid"], "reuslt": "成功注册!"}
            return JsonResponse(result)
        else:
            result = {"code": 0, "result": "密码不符合规范!"}
            return JsonResponse(result)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT'])
def user_detail(request, pk):
    try:
        user_temp = user.objects.get(userid=pk)
    except user.DoesNotExist:
        result = {"code": -1, "result": "未找到相关信息"}
        return JsonResponse(result)
# 登录接口
    if request.method == 'POST':
        try:
            password = request.data["password"]
            if user_temp.check_password(password):
                result = {"code": 1, "result": "登录成功"}
                return JsonResponse(result)
            else:
                result = {"code": -1, "result": "登录失败"}
                return JsonResponse(result)
        except MultiValueDictKeyError:
            serializer = UserSerializer(user_temp)
            return Response(serializer.data)
# 更新信息（还没修改）
    elif request.method == 'PUT':
        serializer = UserSerializer(user_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 通过该方法可以查询目标是否为好友以及目标其他的可被访问的信息（用户名，用户ID，公钥，上次的IP，上次的端口）
    elif request.method == 'GET':
        serializer = UserSerializer(user_temp)
        # seriadata = serializer.data
        # request_id = request.COOKIES["logining_userid"]
        # if(request_id in seriadata["friends"]):
        #     seriadata["friends"] = "is_friend"
        # else:
        #     seriadata["friends"] = "not_friend"
        return Response(serializer.data)
