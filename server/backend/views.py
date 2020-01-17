import json
import logging
import os
import random

from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.utils.datastructures import MultiValueDictKeyError

from django.views.decorators.csrf import csrf_exempt
from .models import user, messages

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
        get_token(request)
        result = {"code": 1, "result": "Token 获取成功!"}
        return HttpResponse(json.dumps(result))
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


@csrf_exempt
def user_list(request):
    # 注册接口
    if request.method == 'POST':
        post_data = json.loads(request.body)
        # print(post_data)
        if (len(post_data["password"]) == 64):
            post_data["userid"] = random.randint(10000000, 100000000)

            user.objects.create(userid=post_data["userid"],
                                password=post_data["password"],
                                username=post_data["username"],
                                IdentityPub=post_data["IdentityPub"],
                                SignedPub=post_data["SignedPub"],
                                OneTimePub=post_data["OneTimePub"],
                                EphemeralPub=post_data["EphemeralPub"])

            result = {"code": 1,
                      "data": post_data["userid"], "reuslt": "成功注册!"}
            return JsonResponse(result)
        else:
            result = {"code": 0, "result": "密码不符合规范!"}
            return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


@csrf_exempt
def user_detail(request, pk):
    try:
        user_temp = user.objects.get(userid=pk)
    except user.DoesNotExist:
        result = {"code": -1, "result": "该用户不存在"}
        return JsonResponse(result)
    # 登录接口
    if request.method == 'POST':
        try:
            password = json.loads(request.body)["password"]
            if user_temp.check_password(password):
                result = {"code": 1, "data": user_temp.to_json(),
                          "result": "登录成功"}
                return JsonResponse(result)
            else:
                result = {"code": -1, "result": "登录失败"}
                return JsonResponse(result)
        except MultiValueDictKeyError:
            result = {"code": -1, "result": "登录失败"}
            return JsonResponse(result)
    # 更新信息（还没修改）
    elif request.method == 'PUT':
        pass
        # 通过该方法可以查询目标是否为好友以及目标其他的可被访问的信息（用户名，用户ID，公钥，上次的IP，上次的端口）
    elif request.method == 'GET':
        user_temp_json = user_temp.to_json()
        user_temp_json.pop("password")
        result = {"code": 1, "data": user_temp_json,
                  "result": "该用户的信息。"}
        return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 获取已登录用户的消息（获取后删除服务器数据）
@csrf_exempt
def messageDetail(request):
    # 上传消息
    if request.method == "POST":
        try:
            post_data = json.loads(request.body)
            messages.objects.create(fromUserid=post_data["fromUserid"],
                                    toUserid=post_data["toUserid"],
                                    ciphertext=post_data["ciphertext"])
        except:
            result = {"code": -1, "result": "消息发送失败"}
            return JsonResponse(result)
        result = {"code": 1, "result": "消息发送成功！"}
        return JsonResponse(result)

    # 获取自己的消息
    elif request.method == "GET":
        logining_userid = int(request.COOKIES["logining_userid"])
        try:
            messages_temp = list(
                messages.objects.filter(toUserid=logining_userid))
            for i in range(len(messages_temp)):
                messages_temp[i] = messages_temp[i].to_json()
        except:
            result = {"code": -1, "result": "消息获取失败"}
            return JsonResponse(result)
        try:
            messages.objects.filter(toUserid=logining_userid).delete()
        except:
            result = {"code": -1, "result": "服务器删除暂存数据失败"}
            return JsonResponse(result)
        if len(messages_temp):
            result = {"code": 1, "data": messages_temp, "result": "服务器暂存的消息"}
            return JsonResponse(result)
        else:
            result = {"code": -1, "result": "没有暂存数据"}
            return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)
