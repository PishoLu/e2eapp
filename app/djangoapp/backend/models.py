from django.db import models

# Create your models here.


class user(models.Model):
    userid = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=20, null=True)
    IdentityPub = models.CharField(max_length=64, null=True)
    SignedPub = models.CharField(max_length=64, null=True)
    OneTimePub = models.CharField(max_length=64, null=True)
    EphemeralPub = models.CharField(max_length=64, null=True)

    IdentityPri = models.CharField(max_length=64, null=True)
    SignedPri = models.CharField(max_length=64, null=True)
    OneTimePri = models.CharField(max_length=64, null=True)
    # user以及服务器的user数据库存放的是最开始的Ephemeral密钥
    EphemeralPri = models.CharField(max_length=64, null=True)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "_state" in dict:
            del dict["_state"]
        return dict


class messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    # * 由登录账号发送的和接收到的信息才能算是属于他的信息，才能进行读取和操作。
    # * 在数据库存储中，仅有成功发出消息和成功接收并解密消息，才能添加进数据库并添加belongUserid属性
    belongUserid = models.IntegerField()
    fromUserid = models.IntegerField()
    toUserid = models.IntegerField()
    kdf_next = models.CharField(max_length=64, null=True)
    date = models.DateTimeField()
    plaintext = models.CharField(max_length=2048)
    EphemeralPub = models.CharField(max_length=64, null=True)
    # 私钥字段可以不要，只是为了测试
    EphemeralPri = models.CharField(max_length=64, null=True)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "_state" in dict:
            del dict["_state"]
        return dict


class friends(models.Model):
    userid = models.IntegerField()
    whosfriend = models.IntegerField()
    username = models.CharField(max_length=20, null=True)
    remark = models.CharField(max_length=20, null=True)
    # 状态码，可以拉黑名单用，为0表示并不是好友，但是对方向自己发送过消息。
    status = models.IntegerField(default=1)
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
