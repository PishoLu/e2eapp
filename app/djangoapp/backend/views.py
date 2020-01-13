import binascii
import json
import logging
import os
import sqlite3

import requests  # 最好不用这个，让前端作为两个后端的跳板
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey, X25519PublicKey)
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import friends, messages, user
from .X3DH import Signalkdf, compare_bytes
from django.db.models import Q

wite_list = []  # 等待被添加的好友列表(只有双方在线的时候才能正常添加)

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


# 开始连接，将连接对象存到列表中，如果没有两个kdf就开始X3DH获取到kdf初始值。
def start_X3DH(request):
    if request.method == "GET":
        pass
    else:
        pass


# 保存发送和接收的消息
@csrf_exempt
def store_message(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        try:
            messages.objects.create(
                fromUserid=post_data["fromUserid"], toUserid=post_data["toUserid"], kdf_next=post_data["kdf_next"], EphemeralPub=post_data["EphemeralPub"], plaintext=post_data["plaintext"])
            result = {"code": 1, "result": "添加成功"}
            return JsonResponse(result)
        except:
            result = {"code": -1, "result": "添加失败！"}
            return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 从数据库过滤消息
@csrf_exempt
def filter_messages(request, pk):
    try:
        logining_userid = int(request.COOKIES["logining_userid"])
        # 这么写不一定能行，行了
        messages_temp = list(messages.objects.filter(
            (Q(fromUserid=pk) and Q(toUserid=logining_userid)) | (Q(toUserid=pk) and Q(fromUserid=logining_userid))).order_by("date"))
        for i in range(len(messages_temp)):
            messages_temp[i] = messages_temp[i].to_json()
        for i in messages_temp:
            if i["fromUserid"] == logining_userid:
                i["fromUserid"] = 1

    except messages.DoesNotExist:
        result = {"code": -1, "result": "该用户不存在"}
        return JsonResponse(result)

    if request.method == 'GET':
        if len(messages_temp):
            result = {"code": 1, "data": messages_temp,
                      "result": "与该用户的来往记录。"}
            return JsonResponse(result)
        else:
            result = {"code": -1, "result": "该用户不存在"}
            return JsonResponse(result)
        return JsonResponse(result)
    elif request.method == 'POST':
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 保存user类相关信息
@csrf_exempt
def store_user(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        # print(post_data)
        # try:
        user.objects.create(userid=post_data["userid"], username=post_data["username"],
                            IdentityPub=post_data["IdentityPub"], SignedPub=post_data["SignedPub"],
                            OneTimePub=post_data["OneTimePub"], EphemeralPub=post_data["EphemeralPub"],
                            IdentityPri=post_data["IdentityPri"], SignedPri=post_data["SignedPri"],
                            OneTimePri=post_data["OneTimePri"], EphemeralPri=post_data["EphemeralPri"])
        result = {"code": 1, "result": "添加成功！"}
        return JsonResponse(result)
        # except:
        #     result = {"code": -1, "result": "添加失败！"}
        #     return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


@csrf_exempt
def get_user(request, pk):
    try:
        logining_userid = request.COOKIES["logining_userid"]
        user_temp = []
        user_temp_t = user.objects.filter(userid=pk)
        for i in user_temp_t:
            user_temp_json = i.to_json()
            # 如果是含有私钥的信息只能由已登录的用户查看
            # is有点问题
            if str(logining_userid) != str(user_temp_json["userid"]):
                user_temp_json["IdentityPri"] = ""
                user_temp_json["SignedPri"] = ""
                user_temp_json["OneTimePri"] = ""
            user_temp.append(user_temp_json)
    except user.DoesNotExist:
        result = {"code": -1, "result": "该用户不存在"}
        return JsonResponse(result)
    except KeyError:
        user_temp = []
        user_temp_t = user.objects.filter(userid=pk)
        for i in user_temp_t:
            user_temp_json = i.to_json()
            user_temp.append(user_temp_json)

    if request.method == 'GET':
        if len(user_temp):
            result = {"code": 1, "data": user_temp,
                      "result": "该用户的信息。"}
            return JsonResponse(result)
        else:
            result = {"code": -1, "result": "该用户不存在"}
            return JsonResponse(result)

    elif request.method == 'POST':
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 保存friend类相关信息
@csrf_exempt
def store_friend(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        logining_userid = int(request.COOKIES["logining_userid"])
        try:
            friends.objects.create(userid=post_data["userid"], username=post_data["username"], whosfriend=logining_userid,
                                   remark=post_data["remark"], status=post_data["status"], IdentityPub=post_data["IdentityPub"],
                                   SignedPub=post_data["SignedPub"], OneTimePub=post_data["OneTimePub"], EphemeralPub=post_data["EphemeralPub"])
            result = {"code": 1, "result": "添加成功！"}
            return JsonResponse(result)
        except:
            result = {"code": -1, "result": "添加失败！"}
            return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 获取好友列表
@csrf_exempt
def friends_list(request):
    try:
        logining_userid = int(request.COOKIES["logining_userid"])
        friends_temp = []
        friends_temp_t = friends.objects.filter(
            whosfriend=logining_userid)
        # print(friends_temp_t)
        for i in friends_temp_t:
            friends_temp.append(i.to_json())
    except friends.DoesNotExist:
        result = {"code": -1, "result": "该用户不存在"}
        return JsonResponse(result)

    if request.method == 'GET':
        if len(friends_temp):
            result = {"code": 1, "data": friends_temp, "result": "好友列表"}
            return JsonResponse(result)
        else:
            result = {"code": -1, "result": "好友列表为空"}
            return JsonResponse(result)
        return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)

# 获取详细好友信息
@csrf_exempt
def friend_detail(request, pk):
    try:
        logining_userid = int(request.COOKIES["logining_userid"])
        friends_temp = friends.objects.get(
            whosfriend=logining_userid, userid=pk).to_json()
    except friends.DoesNotExist:
        result = {"code": -1, "result": "该用户不存在"}
        return JsonResponse(result)

    if request.method == "GET":
        if len(friends_temp):
            result = {"code": 1, "data": friends_temp, "result": "好友详细信息"}
            return JsonResponse(result)
        else:
            result = {"code": -1, "result": "该用户不存在"}
            return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 返回解密消息
# 参数：对方的ID，对方发来的消息
@csrf_exempt
def decrypt_message(request):
    if request.method == "POST":
        post_data = json.loads(request.body)

    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 解析服务器返回的数据包。
# 返回发送人的id信息
# 通过 decrypt_message 解密。（不一定）
@csrf_exempt
def message_parse(request):
    if request.method == "POST":
        post_data = json.loads(request.body)

    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 返回加密药效
# 参数：对方的ID，我要发送的消息
# DH1 = DH (IPK-B 私钥，SPK-A 公钥)
# DH2 = DH (EPK-B 私钥，IPK-A 公钥)
# DH3= DH (EPK-B 私钥，SPK-A 公钥)
# DH4 = DH (IPK-B 私钥，OPK-A 公钥)
# 作为发送方的DH初始化方法
@csrf_exempt
def encrypt_message(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        logining_userid = int(request.COOKIES["logining_userid"])
        # print(logining_userid)
        usertemp = user.objects.get(userid=logining_userid).to_json()

        if(usertemp):
            usertemp["IdentityPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["IdentityPri"].encode("unicode_escape")))
            usertemp["SignedPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["SignedPri"].encode("unicode_escape")))
            usertemp["OneTimePri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["OneTimePri"].encode("unicode_escape")))
            usertemp["EphemeralPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["EphemeralPri"].encode("unicode_escape")))
        user_send_to = friends.objects.get(
            userid=post_data["toUserid"], whosfriend=logining_userid).to_json()
        if(user_send_to):
            user_send_to["IdentityPub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(user_send_to["IdentityPub"].encode("unicode_escape")))
            user_send_to["SignedPub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(user_send_to["SignedPub"].encode("unicode_escape")))
            user_send_to["OneTimePub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(user_send_to["OneTimePub"].encode("unicode_escape")))
            user_send_to["EphemeralPub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(user_send_to["EphemeralPub"].encode("unicode_escape")))
        never_send = 0
        never_receive = 0
        kdf_in = None
        salt = None
        try:
            last_messages_to = list(messages.objects.filter(
                fromUserid=logining_userid, toUserid=post_data["toUserid"]))
            # 获取发给对象的所有消息的最后一个
            if(len(last_messages_to)):
                last_messages_to = last_messages_to[-1].to_json()
            else:
                # 没有向目标发送过消息
                never_send = 1
            last_messages_from = messages.objects.filter(
                toUserid=logining_userid, fromUserid=post_data["toUserid"])
            # 获取对象回复的所有消息的最后一个
            if(len(last_messages_from)):
                last_messages_from = last_messages_from[-1].to_json()
            else:
                # 目标没有向我发送过消息
                never_receive = 1
        except:
            result = {"code": -1, "result": "获取数据库消息出错!"}
            return JsonResponse(result)

        message_EphemeralPri = X25519PrivateKey.generate()
        message_EphemeralPub = message_EphemeralPri.public_key()
        if never_send and never_receive:
            # 没有发过消息也没有收到过对方的消息，生成初始化的kdf用作以后与对象的消息上。
            DH1 = usertemp["IdentityPri"].exchange(user_send_to["SignedPub"])
            DH2 = usertemp["EphemeralPri"].exchange(
                user_send_to["IdentityPub"])
            DH3 = usertemp["EphemeralPri"].exchange(user_send_to["SignedPub"])
            DH4 = usertemp["IdentityPri"].exchange(user_send_to["OneTimePub"])
            # 第一次的share_key长度有128位，但是后续需要的密钥长度只要32位，不过第一次后的kdf输出有64位，前32位为下一次的kdf输入，后32位为这次的加密密钥
            kdf_in = DH1+DH2+DH3+DH4

            salt = message_EphemeralPri.exchange(user_send_to["EphemeralPub"])
        elif never_send and not never_receive:
            # 没有发过消息，但是接收过对方的消息，使用对方最新的Ephemeral公钥以及kdf，接收消息时将目标的临时公钥以及算出的kdf存入数据库
            kdf_in = binascii.hexlify(
                last_messages_from["kdf_next"].encode("unicode_escape"))

            salt = message_EphemeralPri.exchange(
                last_messages_from["EphemeralPub"])
        elif not never_send and never_receive:
            # 发送过消息但是没有收到过回应，使用上一次发送时的kdf，使用对方的临时公钥
            kdf_in = binascii.hexlify(
                last_messages_to["kdf_next"].encode("unicode_escape"))
            salt = message_EphemeralPri.exchange(
                user_send_to["EphemeralPub"])
        elif not never_send and not never_receive:
            # 双方有来有回则根据最近时间是接收还是发送确定kdf输入
            # 不能确定时间前后，先不写这个
            pass

        # 不管之前是否与目标有过联系，只是kdf的输入和对方的临时公钥有所不同，加密使用的新临时密钥是新生成的，对方的临时公钥是一直最新更新在消息数据库的。
        kdf_out = Signalkdf(kdf_in, salt)

        aad = b"a secret message"
        chacha = ChaCha20Poly1305(kdf_out[32:])
        nonce = os.urandom(12)
        ct = chacha.encrypt(nonce, post_data["plaintext"].encode("utf-8"), aad)
        pt = chacha.decrypt(nonce, ct, aad)
        result_data = {
            "fromUserid": logining_userid,
            "toUserid": post_data["toUserid"],
            "kdf_next": binascii.hexlify(kdf_out[:32]).decode("unicode_escape"),
            "message": {
                "aad": aad.decode("utf-8"),
                "EphemeralPub": binascii.hexlify(message_EphemeralPub.public_bytes(
                    encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape"),
                "ciphertext": str(ct),
            },
            "plaintext": post_data["plaintext"]
        }

        result = {"code": 1, "data": result_data, "result": "X3DH密钥"}
        return JsonResponse(result)
        # if(last_messages_from["date"] < last_messages_to["date"]):
        #     pass

        # usertemp["IdentityPri"] = X25519PrivateKey.from_private_bytes(
        #     usertemp["IdentityPri"])
        # usertemp["SignedPri"] = X25519PrivateKey.from_private_bytes(
        #     usertemp["SignedPri"])
        # usertemp["OneTimePri"] = X25519PrivateKey.from_private_bytes(
        #     usertemp["OneTimePri"])
        # DH1 = usertemp["IdentityPri"].exchange(post_data["SignedPub"])
        # DH2 = usertemp["EphemeralPri"].exchange(post_data["IdentityPub"])
        # DH3 = usertemp["EphemeralPri"].exchange(post_data["SignedPub"])
        # DH4 = usertemp["IdentityPri"].exchange(post_data["OneTimePub"])
        # X3DH密钥
        # share_key = DH1+DH2+DH3+DH4
        # message_EphemeralPri = X25519PrivateKey.generate()
        # message_EphemeralPub = message_EphemeralPri.public_key()
        # salt = message_EphemeralPri.exchange(post_data["EphemeralPub"])
        # kdf_out = Signalkdf(share_key, salt)
        # # 后32位为密钥
        # message_key = kdf_out[32:]
        # # 前32位为连贯对话的下一次的share_key
        # kdf_next = kdf_out[:32]
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 登陆到服务器，获取好友列表即登陆IP信息。在初始化之前登陆。登录后初始化获取好友的存活信息。返回给前端列表,由于csrf的原因，登录和注册都交给前端完成，通过axios提交登录注册请求.
# 这里的登录是前端将登录成功的userid发送过来完成密钥初始化的。
# 登录是先账号密码服务器验证登录，然后后端生成新的密钥对返回给前端，前端再将服务器上的密钥对更新完成登录。
@csrf_exempt
def create_new_keyspair(request):
    if request.method == "GET":
        pass
    else:
        pubs = {}
        pubs["IdentityPri"] = X25519PrivateKey.generate()
        pubs["IdentityPub"] = pubs["IdentityPri"].public_key()
        pubs["SignedPri"] = X25519PrivateKey.generate()
        pubs["SignedPub"] = pubs["SignedPri"].public_key()
        pubs["OneTimePri"] = X25519PrivateKey.generate()
        pubs["OneTimePub"] = pubs["OneTimePri"].public_key()
        pubs["EphemeralPri"] = X25519PrivateKey.generate()
        pubs["EphemeralPub"] = pubs["EphemeralPri"].public_key()
        pubs["IdentityPri"] = binascii.hexlify(pubs["IdentityPri"].private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )).decode("unicode_escape")
        pubs["SignedPri"] = binascii.hexlify(pubs["SignedPri"].private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )).decode("unicode_escape")
        pubs["OneTimePri"] = binascii.hexlify(pubs["OneTimePri"].private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )).decode("unicode_escape")
        pubs["EphemeralPri"] = binascii.hexlify(pubs["EphemeralPri"].private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )).decode("unicode_escape")
        pubs["IdentityPub"] = binascii.hexlify(pubs["IdentityPub"].public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )).decode("unicode_escape")
        pubs["SignedPub"] = binascii.hexlify(pubs["SignedPub"].public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )).decode("unicode_escape")
        pubs["OneTimePub"] = binascii.hexlify(pubs["OneTimePub"].public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )).decode("unicode_escape")
        pubs["EphemeralPub"] = binascii.hexlify(pubs["EphemeralPub"].public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )).decode("unicode_escape")
        result = {"code": 1, "data": pubs, "result": "生成新的密钥对"}
        return JsonResponse(result)


def gettoken(request):
    if request.method == "GET":
        get_token(request)
        result = {"code": 1, "data": "", "result": "Token 获取成功!"}
        return JsonResponse(result)
    else:
        pass


@csrf_exempt
def check_pri(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        post_data_temp = post_data.copy()
        try:
            post_data_temp["IdentityPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(post_data["IdentityPri"].encode("unicode_escape")))
            post_data_temp["SignedPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(post_data["SignedPri"].encode("unicode_escape")))
            post_data_temp["OneTimePri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(post_data["OneTimePri"].encode("unicode_escape")))
            post_data_temp["EphemeralPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(post_data["EphemeralPri"].encode("unicode_escape")))

            post_data["IdentityPub"] = binascii.hexlify(post_data_temp["IdentityPri"].public_key().public_bytes(
                encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape")
            post_data["SignedPub"] = binascii.hexlify(post_data_temp["SignedPri"].public_key().public_bytes(
                encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape")
            post_data["OneTimePub"] = binascii.hexlify(post_data_temp["OneTimePri"].public_key().public_bytes(
                encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape")
            post_data["EphemeralPub"] = binascii.hexlify(post_data_temp["EphemeralPub"].public_key().public_bytes(
                encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape")
            # print(post_data)
            # print(post_data_temp)
            result = {"code": 1, "data": post_data, "result": "私钥格式正常！"}
            return JsonResponse(result)
        except:
            result = {"code": -1, "result": "私钥格式有误！"}
            return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)
