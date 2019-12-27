from django.db import models
import json

# Create your models here.


class user(models.Model):
    userid = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=20, null=True)
    IdentityPub = models.CharField(max_length=64, null=True)
    SignedPub = models.CharField(max_length=64, null=True)
    OneTimePub = models.CharField(max_length=64, null=True)
    ElephantPub = models.CharField(max_length=64, null=True)

    IdentityPri = models.CharField(max_length=64, null=True)
    SignedPri = models.CharField(max_length=64, null=True)
    OneTimePri = models.CharField(max_length=64, null=True)
    ElephantPri = models.CharField(max_length=64, null=True)

    last_ip = models.CharField(max_length=15, null=True)
    last_port = models.IntegerField(null=True)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class messages(models.Model):
    fromUserid = models.IntegerField(primary_key=True)
    toUserid = models.IntegerField()

    date = models.DateTimeField()
    plaintext = models.CharField(max_length=2048)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class friends(models.Model):
    urerid = models.IntegerField(primary_key=True)
    IP = models.CharField(max_length=15)
    Port = models.IntegerField()
    remark = models.CharField(max_length=20, null=True)
    status = models.IntegerField(default=1)  # 状态码，可以拉黑名单用
    group = models.CharField(max_length=20, null=True)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
