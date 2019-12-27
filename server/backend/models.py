from django.db import models


# Create your models here.


# 还是决定用userid来作为身份的一种凭据，通过服务器可以获取到该账号的上一次登陆的IP和端口，然后客户端自己去测试该账号是否还存活，再考虑是否进行通信，服务器仅提供信息，不转发，不保存。
class user(models.Model):
    userid = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=64, default=userid)
    password = models.CharField(max_length=64)

    IdentityPub = models.CharField(max_length=64, null=True)
    SignedPub = models.CharField(max_length=64, null=True)
    OneTimePub = models.CharField(max_length=64, null=True)

    friends = models.CharField(max_length=2048, null=True)

    last_ip = models.CharField(max_length=15, null=True)
    last_port = models.IntegerField(null=True)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def check_password(self, check_p):
        if self.password == check_p:
            return 1
        else:
            return 0
