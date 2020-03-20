import binascii
import json
import logging
import os
import sqlite3
import time

import requests  # 最好不用这个，让前端作为两个后端的跳板
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey, X25519PublicKey)
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from django.db.models import Q
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import friends, messages, user
from .X3DH import Signalkdf, compare_bytes

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


# 保存发送和接收的消息
@csrf_exempt
def storeMessage(request):
    if request.method == "POST":
        postData = json.loads(request.body)
        try:
            messages.objects.create(
                belongUserid=postData["belongUserid"], fromUserid=postData["fromUserid"], toUserid=postData["toUserid"], kdf_next=postData["kdf_next"], EphemeralPub=postData["EphemeralPub"], plaintext=postData["plaintext"], EphemeralPri=postData["EphemeralPri"])
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
def filterMessages(request, pk):
    try:
        loginingUserid = int(request.COOKIES["loginingUserid"])
        # 这么写不一定能行，行了
        messagesTemp = list(messages.objects.filter(
            (Q(fromUserid=pk) & Q(toUserid=loginingUserid) & Q(belongUserid=loginingUserid)) |
            (Q(fromUserid=loginingUserid) & Q(toUserid=pk)
             & Q(belongUserid=loginingUserid))
        ).order_by("date"))
        for i in range(len(messagesTemp)):
            messagesTemp[i] = messagesTemp[i].to_json()
        for i in messagesTemp:
            if i["fromUserid"] == loginingUserid:
                i["fromUserid"] = 1

    except messages.DoesNotExist:
        result = {"code": -1, "result": "该用户不存在或者没有消息记录"}
        return JsonResponse(result)

    if request.method == 'GET':
        if len(messagesTemp):
            result = {"code": 1, "data": messagesTemp,
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
def storeUser(request):
    if request.method == "POST":
        postData = json.loads(request.body)
        # print(postData)
        # try:
        user.objects.create(userid=postData["userid"], username=postData["username"],
                            IdentityPub=postData["IdentityPub"], SignedPub=postData["SignedPub"],
                            OneTimePub=postData["OneTimePub"], EphemeralPub=postData["EphemeralPub"],
                            IdentityPri=postData["IdentityPri"], SignedPri=postData["SignedPri"],
                            OneTimePri=postData["OneTimePri"], EphemeralPri=postData["EphemeralPri"])
        result = {"code": 1, "result": "添加成功！"}
        return JsonResponse(result)
        # except:
        #     result = {"code": -1, "result": "添加失败！"}
        #     return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


@csrf_exempt
def getUser(request, pk):
    try:
        loginingUserid = request.COOKIES["loginingUserid"]
        userTemp = []
        userTemp_t = user.objects.filter(userid=pk)
        for i in userTemp_t:
            userTemp_json = i.to_json()
            # 如果是含有私钥的信息只能由已登录的用户查看
            # is有点问题
            if str(loginingUserid) != str(userTemp_json["userid"]):
                userTemp_json["IdentityPri"] = ""
                userTemp_json["SignedPri"] = ""
                userTemp_json["OneTimePri"] = ""
            userTemp.append(userTemp_json)
    except user.DoesNotExist:
        result = {"code": -1, "result": "该用户不存在"}
        return JsonResponse(result)
    except KeyError:
        userTemp = []
        userTemp_t = user.objects.filter(userid=pk)
        for i in userTemp_t:
            userTemp_json = i.to_json()
            userTemp.append(userTemp_json)

    if request.method == 'GET':
        if len(userTemp):
            result = {"code": 1, "data": userTemp,
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
def storeFriend(request):
    try:
        postData = json.loads(request.body)
        loginingUserid = int(request.COOKIES["loginingUserid"])
    except:
        result = {"code": -1, "result": "获取cookie出错"}
        return JsonResponse(result)

    if request.method == "POST":
        try:
            friends.objects.create(userid=postData["userid"], username=postData["username"], whosfriend=loginingUserid,
                                   remark=postData["remark"], status=postData["status"], IdentityPub=postData["IdentityPub"],
                                   SignedPub=postData["SignedPub"], OneTimePub=postData["OneTimePub"], EphemeralPub=postData["EphemeralPub"])
            result = {"code": 1, "result": "添加成功！"}
            return JsonResponse(result)
        except:
            result = {"code": -1, "result": "添加失败！"}
            return JsonResponse(result)
    elif request.method == "PUT":
        try:
            tempFriend = friends.objects.get(
                userid=postData["userid"], whosfriend=loginingUserid)
            tempFriend.status = 1
            tempFriend.save()
            result = {"code": 1, "result": "更新成功！"}
            return JsonResponse(result)

        except:
            result = {"code": -1, "result": "更新失败！"}
            return JsonResponse(result)
    elif request.method == "DELETE":
        try:
            tempFriend = friends.objects.get(
                userid=postData["userid"], whosfriend=loginingUserid, status=0)
            tempFriend.delete()
            result = {"code": 1, "result": "删除成功！"}
            return JsonResponse(result)

        except:
            result = {"code": -1, "result": "删除失败！"}
            return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 获取好友列表
@csrf_exempt
def friendsList(request):
    try:
        loginingUserid = int(request.COOKIES["loginingUserid"])
        # print(loginingUserid)
        friendsTemp = []
        friendsTemp_t = friends.objects.filter(
            whosfriend=loginingUserid)
        # print(friendsTemp_t)
        for i in friendsTemp_t:
            friendsTemp.append(i.to_json())
    except friends.DoesNotExist:
        result = {"code": -1, "result": "该用户不存在"}
        return JsonResponse(result)

    if request.method == 'GET':
        if len(friendsTemp):
            result = {"code": 1, "data": friendsTemp, "result": "好友列表"}
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
        loginingUserid = int(request.COOKIES["loginingUserid"])
        friendsTemp = friends.objects.get(
            whosfriend=loginingUserid, userid=pk).to_json()
    except friends.DoesNotExist:
        result = {"code": -1, "result": "该用户不存在"}
        return JsonResponse(result)

    if request.method == "GET":
        if len(friendsTemp):
            result = {"code": 1, "data": friendsTemp, "result": "好友详细信息"}
            return JsonResponse(result)
        else:
            result = {"code": -1, "result": "该用户不存在"}
            return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 功能函数，遍历一个bytes的字符串并返回对应unicode编码的列表
def bytes2list(bytesString):
    tempList = []
    for i in bytesString:
        tempList.append(i)
    return tempList


# 功能函数，遍历一个数组list并返回对应的bytes字符串
def list2bytes(tempList):
    return bytes(tempList)


# 返回解密消息
# 参数：对方的ID，对方发来的消息
# 需要分析是否是第一次接收通话
@csrf_exempt
def decryptMessage(request):
    if request.method == "POST":
        loginingUserid = int(request.COOKIES["loginingUserid"])
        postData = json.loads(request.body)
        postData["message"] = eval(postData["message"])
        # print(postData["message"])
        usertemp = user.objects.get(userid=loginingUserid).to_json()
        if(usertemp):
            usertemp["IdentityPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["IdentityPri"].encode("unicode_escape")))
            usertemp["SignedPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["SignedPri"].encode("unicode_escape")))
            usertemp["OneTimePri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["OneTimePri"].encode("unicode_escape")))
            usertemp["EphemeralPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["EphemeralPri"].encode("unicode_escape")))

        userReceiveFrom = friends.objects.get(
            userid=postData["fromUserid"], whosfriend=loginingUserid).to_json()
        if(userReceiveFrom):
            userReceiveFrom["IdentityPub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(userReceiveFrom["IdentityPub"].encode("unicode_escape")))
            userReceiveFrom["SignedPub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(userReceiveFrom["SignedPub"].encode("unicode_escape")))
            userReceiveFrom["OneTimePub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(userReceiveFrom["OneTimePub"].encode("unicode_escape")))
            userReceiveFrom["EphemeralPub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(userReceiveFrom["EphemeralPub"].encode("unicode_escape")))
        tempReceiveFromNextEphPub = X25519PublicKey.from_public_bytes(
            binascii.unhexlify(postData["message"]["EphemeralPub"].encode("unicode_escape")))
        # 通过消息记录来获取上一次对话的kdf

        neverSend = 0
        neverReceive = 0
        kdf_in = None
        salt = None

        try:
            lastMessagesTo = messages.objects.filter(
                fromUserid=loginingUserid, toUserid=postData["fromUserid"], belongUserid=loginingUserid).order_by("-date")
            # 获取发给对象的所有消息的最后一个
            # print(len(lastMessagesTo))
            if(len(lastMessagesTo)):
                lastMessagesTo = lastMessagesTo[0].to_json()
                lastMessagesTo["EphemeralPri"] = X25519PrivateKey.from_private_bytes(
                    binascii.unhexlify(lastMessagesTo["EphemeralPri"].encode("unicode_escape")))
                lastMessagesTo["EphemeralPub"] = X25519PublicKey.from_public_bytes(
                    binascii.unhexlify(lastMessagesTo["EphemeralPub"].encode("unicode_escape")))
            else:
                # 没有向目标发送过消息
                neverSend = 1
            lastMessagesFrom = messages.objects.filter(
                toUserid=loginingUserid, fromUserid=postData["fromUserid"], belongUserid=loginingUserid).order_by("-date")
            # 获取对象回复的所有消息的最后一个
            if(len(lastMessagesFrom)):
                lastMessagesFrom = lastMessagesFrom[0].to_json()
                lastMessagesFrom["EphemeralPub"] = X25519PublicKey.from_public_bytes(
                    binascii.unhexlify(lastMessagesFrom["EphemeralPub"].encode("unicode_escape")))
            else:
                # 目标没有向我发送过消息
                neverReceive = 1
        except:
            result = {"code": -1, "result": "获取数据库消息出错!"}
            return JsonResponse(result)
        # 第一次收到信息解密的话使用user的私钥以及对方发送过来的公钥
        # DH1 = DH (IPK-A 私钥，SPK-B 公钥)
        # DH2 = DH (EPK-A 私钥，IPK-B 公钥)
        # DH3= DH (EPK-A 私钥，SPK-B 公钥)
        # DH4 = DH (IPK-A 私钥，OPK-B 公钥)
        # 作为接收方的DH初始化方法
        if neverReceive and neverSend:
            DH1 = usertemp["SignedPri"].exchange(
                userReceiveFrom["IdentityPub"])
            DH2 = usertemp["IdentityPri"].exchange(
                userReceiveFrom["EphemeralPub"])
            DH3 = usertemp["SignedPri"].exchange(
                userReceiveFrom["EphemeralPub"])
            DH4 = usertemp["OneTimePri"].exchange(
                userReceiveFrom["IdentityPub"])
            # 第一次的share_key长度有128位，但是后续需要的密钥长度只要32位，不过第一次后的kdf输出有64位，前32位为下一次的kdf输入，后32位为这次的加密密钥
            print("没有发送也没有接收过消息。")
            kdf_in = DH1+DH2+DH3+DH4
            salt = usertemp["EphemeralPri"].exchange(tempReceiveFromNextEphPub)
        # 不是第一次收到信息但是没有发送过消息，解密使用上一次的kdf以及自己的私钥，以及对方发送过来的公钥。
        elif neverSend and not neverReceive:
            print("没有发送过消息但是接收到过消息。")
            kdf_in = binascii.hexlify(
                lastMessagesFrom["kdf_next"].encode("unicode_escape"))
            salt = usertemp["EphemeralPri"].exchange(tempReceiveFromNextEphPub)
        # 没有收到过消息，但是发送过消息，即这是第一次收到对方的消息，使用上一次发送的kdf以及自己的私钥，使用对方发送来的公钥解密。
        elif neverReceive and not neverSend:
            print("发送过消息但是没有接收过消息。")
            kdf_in = binascii.hexlify(
                lastMessagesTo["kdf_next"].encode("unicode_escape"))
            salt = lastMessagesTo["EphemeralPri"].exchange(
                tempReceiveFromNextEphPub)
        # 之前的消息有来有往，使用上一次自己发送消息的私钥,以及对方当前使用的公钥。kdf通过对比时间戳来选取最近的一个。
        else:
            print("发送过也接收到过消息。")
            lastTimeSend = time.strptime(
                str(lastMessagesTo["date"]), "%Y-%m-%d %H:%M:%S")
            lastTimeReceive = time.strptime(
                str(lastMessagesFrom["date"]), "%Y-%m-%d %H:%M:%S")
            if(lastTimeReceive < lastTimeSend):
                kdf_in = binascii.hexlify(
                    lastMessagesTo["kdf_next"].encode("unicode_escape"))
            else:
                kdf_in = binascii.hexlify(
                    lastMessagesFrom["kdf_next"].encode("unicode_escape"))
            salt = lastMessagesTo["EphemeralPri"].exchange(
                tempReceiveFromNextEphPub)

        # 解密过程
        print(kdf_in)
        print(salt)
        kdf_out = Signalkdf(kdf_in, salt)
        aad = postData["message"]["aad"].encode("utf-8")
        chacha = ChaCha20Poly1305(kdf_out[32:])
        nonce = list2bytes(postData["message"]["nonce"])
        ct = list2bytes(postData["message"]["ciphertext"])
        pt = chacha.decrypt(nonce, ct, aad)
        resultData = {
            "plaintext": pt.decode('utf-8'),
            "kdf_next": binascii.hexlify(kdf_out[:32]).decode("unicode_escape"),
            "fromUserid": postData["fromUserid"],
            "toUserid": postData["toUserid"],
            "EphemeralPub": postData["message"]["EphemeralPub"],
            "date": postData["date"]
        }
        # 解密后返回目标更新的临时公钥，返回下一次的kdf，返回明文用于保存。
        result = {"code": 1, "data": resultData, "result": "密文解析成功！"}
        return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)


# 解析服务器返回的数据包。
# 返回发送人的id信息
# 通过 decrypt_message 解密。（不一定）
# 分析是否是好友，是否之前有过聊天记录。如果有聊天记录就可以通过上次的kdf继续沿用，如果没有记录就让前端重新获取目的好友公钥，
# 如果不是好友就返回给前端让前端决定是否添加为好友。
# 解析功能交给前端。
# @csrf_exempt
# def message_parse(request):
#     if request.method == "POST":
#         result
#         postData = json.loads(request.body)
#         for i in postData:
#             pass
#     else:
#         result = {"code": -1, "result": "请求方式有误!"}


# 返回加密药效
# 参数：对方的ID，我要发送的消息
@csrf_exempt
def encryptMessage(request):
    if request.method == "POST":
        postData = json.loads(request.body)
        # print(postData["plaintext"])
        loginingUserid = int(request.COOKIES["loginingUserid"])
        # print(loginingUserid)
        usertemp = user.objects.get(userid=loginingUserid).to_json()

        if(usertemp):
            usertemp["IdentityPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["IdentityPri"].encode("unicode_escape")))
            usertemp["SignedPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["SignedPri"].encode("unicode_escape")))
            usertemp["OneTimePri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["OneTimePri"].encode("unicode_escape")))
            usertemp["EphemeralPri"] = X25519PrivateKey.from_private_bytes(
                binascii.unhexlify(usertemp["EphemeralPri"].encode("unicode_escape")))

        userSendTo = friends.objects.get(
            userid=postData["toUserid"], whosfriend=loginingUserid).to_json()
        if(userSendTo):
            userSendTo["IdentityPub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(userSendTo["IdentityPub"].encode("unicode_escape")))
            userSendTo["SignedPub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(userSendTo["SignedPub"].encode("unicode_escape")))
            userSendTo["OneTimePub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(userSendTo["OneTimePub"].encode("unicode_escape")))
            userSendTo["EphemeralPub"] = X25519PublicKey.from_public_bytes(
                binascii.unhexlify(userSendTo["EphemeralPub"].encode("unicode_escape")))
        neverSend = 0
        neverReceive = 0
        kdf_in = None
        salt = None
        try:
            lastMessagesTo = messages.objects.filter(
                fromUserid=loginingUserid, toUserid=postData["toUserid"], belongUserid=loginingUserid).order_by("-date")
            # 获取发给对象的所有消息的最后一个
            # print(len(lastMessagesTo))
            if(len(lastMessagesTo)):
                lastMessagesTo = lastMessagesTo[0].to_json()
                lastMessagesTo["EphemeralPub"] = X25519PublicKey.from_public_bytes(
                    binascii.unhexlify(lastMessagesTo["EphemeralPub"].encode("unicode_escape")))
            else:
                # 没有向目标发送过消息
                neverSend = 1
            lastMessagesFrom = messages.objects.filter(
                toUserid=loginingUserid, fromUserid=postData["toUserid"], belongUserid=loginingUserid).order_by("-date")
            # 获取对象回复的所有消息的最后一个
            # print(lastMessagesFrom)
            if(len(lastMessagesFrom)):
                lastMessagesFrom = lastMessagesFrom[0].to_json()
                lastMessagesFrom["EphemeralPub"] = X25519PublicKey.from_public_bytes(
                    binascii.unhexlify(lastMessagesFrom["EphemeralPub"].encode("unicode_escape")))
            else:
                # 目标没有向我发送过消息
                neverReceive = 1
        except:
            result = {"code": -1, "result": "获取数据库历史消息出错!"}
            return JsonResponse(result)

        message_EphemeralPri = X25519PrivateKey.generate()
        message_EphemeralPub = message_EphemeralPri.public_key()
        if neverSend and neverReceive:
            # 没有发过消息也没有收到过对方的消息，生成初始化的kdf用作以后与对象的消息上。
            # DH1 = DH (IPK-B 私钥，SPK-A 公钥)
            # DH2 = DH (EPK-B 私钥，IPK-A 公钥)
            # DH3= DH (EPK-B 私钥，SPK-A 公钥)
            # DH4 = DH (IPK-B 私钥，OPK-A 公钥)
            # 作为发送方的DH初始化方法
            DH1 = usertemp["IdentityPri"].exchange(userSendTo["SignedPub"])
            DH2 = usertemp["EphemeralPri"].exchange(
                userSendTo["IdentityPub"])
            DH3 = usertemp["EphemeralPri"].exchange(userSendTo["SignedPub"])
            DH4 = usertemp["IdentityPri"].exchange(userSendTo["OneTimePub"])
            # 第一次的share_key长度有128位，但是后续需要的密钥长度只要32位，不过第一次后的kdf输出有64位，前32位为下一次的kdf输入，后32位为这次的加密密钥
            print("没有接收过也没有发送过消息。")
            kdf_in = DH1+DH2+DH3+DH4
            salt = message_EphemeralPri.exchange(userSendTo["EphemeralPub"])
        elif neverSend and not neverReceive:
            # 没有发过消息，但是接收过对方的消息，使用对方最新的Ephemeral公钥以及kdf，接收消息时将目标的临时公钥以及算出的kdf存入数据库
            print("没有发送过消息但是接收过消息。")
            kdf_in = binascii.hexlify(
                lastMessagesFrom["kdf_next"].encode("unicode_escape"))
            salt = message_EphemeralPri.exchange(
                lastMessagesFrom["EphemeralPub"])
        elif not neverSend and neverReceive:
            # 发送过消息但是没有收到过回应，使用上一次发送时的kdf，使用对方的临时公钥
            print("发送过消息但是没有收到过消息。")
            kdf_in = binascii.hexlify(
                lastMessagesTo["kdf_next"].encode("unicode_escape"))
            salt = message_EphemeralPri.exchange(
                userSendTo["EphemeralPub"])
        elif not neverSend and not neverReceive:
            # 双方有来有回则根据最近时间是接收还是发送确定kdf输入
            # 不能确定时间前后，先不写这个
            print("接收到也发送过消息。")
            lastTimeSend = time.strptime(
                str(lastMessagesTo["date"]), "%Y-%m-%d %H:%M:%S")
            lastTimeReceive = time.strptime(
                str(lastMessagesFrom["date"]), "%Y-%m-%d %H:%M:%S")
            if(lastTimeSend > lastTimeReceive):
                kdf_in = binascii.hexlify(
                    lastMessagesTo["kdf_next"].encode("unicode_escape"))
                salt = message_EphemeralPri.exchange(
                    lastMessagesFrom["EphemeralPub"])
            else:
                kdf_in = binascii.hexlify(
                    lastMessagesFrom["kdf_next"].encode("unicode_escape"))
                salt = message_EphemeralPri.exchange(
                    lastMessagesFrom["EphemeralPub"])
                # 不管之前是否与目标有过联系，只是kdf的输入和对方的临时公钥有所不同，加密使用的新临时密钥是新生成的，对方的临时公钥是一直最新更新在消息数据库的。

        # 加密过程
        print(kdf_in)
        print(salt)
        kdf_out = Signalkdf(kdf_in, salt)
        aad = b"a secret message"
        chacha = ChaCha20Poly1305(kdf_out[32:])
        nonce = os.urandom(12)
        ct = chacha.encrypt(nonce, postData["plaintext"].encode("utf-8"), aad)
        # pt = chacha.decrypt(nonce, ct, aad)
        resultData = {
            "fromUserid": loginingUserid,
            "toUserid": postData["toUserid"],
            "kdf_next": binascii.hexlify(kdf_out[:32]).decode("unicode_escape"),
            "EphemeralPri": binascii.hexlify(message_EphemeralPri.private_bytes(encoding=serialization.Encoding.Raw,
                                                                                format=serialization.PrivateFormat.Raw,
                                                                                encryption_algorithm=serialization.NoEncryption())).decode("unicode_escape"),
            "message": {
                'aad': aad.decode("utf-8"),
                'nonce': bytes2list(nonce),
                'EphemeralPub': binascii.hexlify(message_EphemeralPub.public_bytes(
                    encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape"),
                'ciphertext': bytes2list(ct),
            },
            "plaintext": postData["plaintext"]
        }

        result = {"code": 1, "data": resultData, "result": "X3DH密钥"}
        return JsonResponse(result)
        # if(lastMessagesFrom["date"] < lastMessagesTo["date"]):
        #     pass

        # usertemp["IdentityPri"] = X25519PrivateKey.from_private_bytes(
        #     usertemp["IdentityPri"])
        # usertemp["SignedPri"] = X25519PrivateKey.from_private_bytes(
        #     usertemp["SignedPri"])
        # usertemp["OneTimePri"] = X25519PrivateKey.from_private_bytes(
        #     usertemp["OneTimePri"])
        # DH1 = usertemp["IdentityPri"].exchange(postData["SignedPub"])
        # DH2 = usertemp["EphemeralPri"].exchange(postData["IdentityPub"])
        # DH3 = usertemp["EphemeralPri"].exchange(postData["SignedPub"])
        # DH4 = usertemp["IdentityPri"].exchange(postData["OneTimePub"])
        # X3DH密钥
        # share_key = DH1+DH2+DH3+DH4
        # message_EphemeralPri = X25519PrivateKey.generate()
        # message_EphemeralPub = message_EphemeralPri.public_key()
        # salt = message_EphemeralPri.exchange(postData["EphemeralPub"])
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
def createNewKeyspair(request):
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
def checkPri(request):
    if request.method == "POST":
        postData = json.loads(request.body)
        postData_temp = postData.copy()
        postData_temp2 = postData.copy()
        # try:
        postData_temp["IdentityPri"] = X25519PrivateKey.from_private_bytes(
            binascii.unhexlify(postData["IdentityPri"].encode("unicode_escape")))
        postData_temp["SignedPri"] = X25519PrivateKey.from_private_bytes(
            binascii.unhexlify(postData["SignedPri"].encode("unicode_escape")))
        postData_temp["OneTimePri"] = X25519PrivateKey.from_private_bytes(
            binascii.unhexlify(postData["OneTimePri"].encode("unicode_escape")))
        postData_temp["EphemeralPri"] = X25519PrivateKey.from_private_bytes(
            binascii.unhexlify(postData["EphemeralPri"].encode("unicode_escape")))

        postData_temp2["IdentityPub"] = binascii.hexlify(postData_temp["IdentityPri"].public_key().public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape")
        postData_temp2["SignedPub"] = binascii.hexlify(postData_temp["SignedPri"].public_key().public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape")
        postData_temp2["OneTimePub"] = binascii.hexlify(postData_temp["OneTimePri"].public_key().public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape")
        postData_temp2["EphemeralPub"] = binascii.hexlify(postData_temp["EphemeralPri"].public_key().public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape")
        # print(postData)
        # print(postData_temp)
        result = {"code": 1, "data": postData_temp2, "result": "私钥格式正常！"}
        return JsonResponse(result)
        # except:
        #     result = {"code": -1, "result": "私钥格式有误！"}
        #     return JsonResponse(result)
    else:
        result = {"code": -1, "result": "请求方式有误!"}
        return JsonResponse(result)
