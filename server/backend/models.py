from django.db import models
import time

# Create your models here.


# 还是决定用userid来作为身份的一种凭据，通过服务器可以获取到该账号的上一次登陆的IP和端口，然后客户端自己去测试该账号是否还存活，再考虑是否进行通信，服务器仅提供信息，不转发，不保存。
class user(models.Model):
    userid = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    IdentityPub = models.CharField(max_length=64, null=True)
    SignedPub = models.CharField(max_length=64, null=True)
    OneTimePub = models.CharField(max_length=64, null=True)
    EphemeralPub = models.CharField(max_length=64, null=True)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "_state" in dict:
            del dict["_state"]
        return dict

    def check_password(self, check_p):
        if self.password == check_p:
            return 1
        else:
            return 0


class messages(models.Model):
    fromUserid = models.IntegerField()
    toUserid = models.IntegerField()
    date = models.DateTimeField(default=time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()))
    message = models.CharField(max_length=2048)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "_state" in dict:
            del dict["_state"]
        return dict
