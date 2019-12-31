import binascii
import json
import os
import time

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey, X25519PublicKey)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


class Message_Node:
    def __init__(self):
        self.DH_next = None
        self.KDF_next = None
        self.DH = b""
        self.KDF_input = b""

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Message:
    def __init__(self):
        self.s_user_id = 0  # 设置为10位的随机数
        self.d_user_id = 0  # 设置为10位的随机数
        self.s_user_IK = ""  # 固定64位
        self.s_user_EK = ""  # 固定64位
        self.flags = ""  # 固定6位
        self.AD = ""  # 870位，不够补足0

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class User:
    User_id = 0
    Username = ""
    Password = ""

    def __init__(self):
        self.IdentityPri = X25519PrivateKey.generate()
        self.IdentityPub = self.IdentityPri.public_key()
        self.SignedPri = X25519PrivateKey.generate()
        self.SignedPub = self.SignedPri.public_key()
        self.OneTimePri = X25519PrivateKey.generate()
        self.OneTimePub = self.OneTimePri.public_key()
        self.EphemeralPri = X25519PrivateKey.generate()
        self.EphemeralPub = self.EphemeralPri.public_key()

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class DH:
    def __init__(self):
        self.DH1 = bytes([])
        self.DH2 = bytes([])
        self.DH3 = bytes([])
        self.DH4 = bytes([])
        self.share_key = bytes([])

    # DH1 = DH (IPK-A 私钥，SPK-B 公钥)
    # DH2 = DH (EPK-A 私钥，IPK-B 公钥)
    # DH3= DH (EPK-A 私钥，SPK-B 公钥)
    # DH4 = DH (IPK-A 私钥，OPK-B 公钥)
    # 作为接收方的DH初始化方法
    def receive(self, mine, other):
        self.DH1 = mine.SignedPri.exchange(other.IdentityPub)
        self.DH2 = mine.IdentityPri.exchange(other.EphemeralPub)
        self.DH3 = mine.SignedPri.exchange(other.EphemeralPub)
        self.DH4 = mine.OneTimePri.exchange(other.IdentityPub)
        if self.DH4:
            self.share_key = self.DH1 + self.DH2 + self.DH3 + self.DH4
        else:
            self.share_key = self.DH1 + self.DH2 + self.DH3

    # DH1 = DH (IPK-B 私钥，SPK-A 公钥)
    # DH2 = DH (EPK-B 私钥，IPK-A 公钥)
    # DH3= DH (EPK-B 私钥，SPK-A 公钥)
    # DH4 = DH (IPK-B 私钥，OPK-A 公钥)
    # 作为发送方的DH初始化方法
    def send(self, mine, other):
        self.DH1 = mine.IdentityPri.exchange(other.SignedPub)
        self.DH2 = mine.EphemeralPri.exchange(other.IdentityPub)
        self.DH3 = mine.EphemeralPri.exchange(other.SignedPub)
        self.DH4 = mine.IdentityPri.exchange(other.OneTimePub)
        if self.DH4:
            self.share_key = self.DH1 + self.DH2 + self.DH3 + self.DH4
        else:
            self.share_key = self.DH1 + self.DH2 + self.DH3

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


def Signalkdf(share_key, salt=None, info=""):
    kdf_output = HKDF(
        algorithm=hashes.SHA256(),
        length=64,
        salt=salt,
        info=info.encode("utf-8"),
        backend=default_backend()
    ).derive(share_key)
    return kdf_output


# 比较两个bytes字符串是否一致
def compare_bytes(A, B):
    nope = []
    if type(A) and type(B) is not bytes:
        return -1
    else:
        if len(A) is not len(B):
            return 0
        else:
            for i in range(len(A)):
                if A[i] is not B[i]:
                    nope.append(i)
    if len(nope) == 0:
        return 1
    else:
        return nope


if __name__ == '__main__':
    time_begin = time.time()
    mine = User()
    print(binascii.hexlify(mine.IdentityPub.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape"))
    print(binascii.hexlify(mine.SignedPub.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape"))
    print(binascii.hexlify(mine.OneTimePub.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape"))
    print(binascii.hexlify(mine.IdentityPri.private_bytes(encoding=serialization.Encoding.Raw,
                                                          format=serialization.PrivateFormat.Raw,
                                                          encryption_algorithm=serialization.NoEncryption())).decode("unicode_escape"))
    print(binascii.hexlify(mine.SignedPri.private_bytes(encoding=serialization.Encoding.Raw,
                                                        format=serialization.PrivateFormat.Raw,
                                                        encryption_algorithm=serialization.NoEncryption())).decode("unicode_escape"))
    print(binascii.hexlify(mine.OneTimePri.private_bytes(encoding=serialization.Encoding.Raw,
                                                         format=serialization.PrivateFormat.Raw,
                                                         encryption_algorithm=serialization.NoEncryption())).decode("unicode_escape"))

    mine_DH = DH()

    other = User()
    other_DH = DH()

    mine_DH.send(mine, other)
    other_DH.receive(other, mine)

    print("A的X3DH密钥：", binascii.hexlify(mine_DH.share_key))
    print("B的X3DH密钥：", binascii.hexlify(other_DH.share_key))
    print("X3DH密钥是否一致：", compare_bytes(mine_DH.share_key, other_DH.share_key))
    print("X3DH结束，开始双棘轮")

    root_message = Message_Node()
    lastest_send = root_message
    lastest_recv = root_message

    for i in range(1, 4):
        mine.EphemeralPri = X25519PrivateKey.generate()
        mine.EphemeralPub = mine.EphemeralPri.public_key()

        other.EphemeralPri = X25519PrivateKey.generate()
        other.EphemeralPub = other.EphemeralPri.public_key()

        self_salt = mine.EphemeralPri.exchange(other.EphemeralPub)
        print("A第", i, "轮盐：", binascii.hexlify(self_salt))
        other_salt = other.EphemeralPri.exchange(mine.EphemeralPub)
        print("B第", i, "轮盐：", binascii.hexlify(other_salt))

        kdf_output_self = Signalkdf(mine_DH.share_key, self_salt)
        kdf_output_other = Signalkdf(other_DH.share_key, other_salt)
        print("A第", i, "轮key：", binascii.hexlify(kdf_output_self[32:]))
        print("B第", i, "轮key：", binascii.hexlify(kdf_output_other[32:]))
        mine_DH.share_key = kdf_output_self[:32]
        other_DH.share_key = kdf_output_other[:32]

        # AES
        # backend = default_backend()
        # iv = os.urandom(16)
        # cipher = Cipher(algorithms.AES(
        #     kdf_output_other[32:]), modes.CBC(iv), backend=backend)
        # encryptor = cipher.encryptor()
        # ct = encryptor.update(b"a secret message") + encryptor.finalize()

        # ChaCha20
        nonce = os.urandom(16)
        algorithm = algorithms.ChaCha20(kdf_output_self[32:], nonce)
        backend = default_backend()
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(b"a secret message234")

        print("密文：", ct, "\n密文长度：", len(ct))
        decryptor = cipher.decryptor()
        print("解密后：", decryptor.update(ct))

        new_message = Message()
        new_message.d_user_id = 123456789
        new_message.s_user_id = 987654321
        new_message.s_user_EK = binascii.hexlify(mine.EphemeralPub.public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape")
        new_message.s_user_IK = binascii.hexlify(mine.IdentityPub.public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("unicode_escape")

        # new_message.s_user_EK=binascii.hexlify(mine.EphemeralPub.public_bytes()).decode("utf-8")
        # new_message.s_user_IK=binascii.hexlify(mine.IdentityPub.public_bytes()).decode("utf-8")

        new_message.flags = binascii.hexlify(bytes([1, 1, 0])).decode("utf-8")
        new_message.AD = binascii.hexlify(ct).decode("utf-8")
        send_bytes = json.dumps(new_message.to_json()).encode("utf-8")
        print(send_bytes)
        print("数据包长度：", len(send_bytes))

        print("开始解封装数据包")
        recv_bytes = send_bytes
        new_message_dict = json.loads(recv_bytes)
        print(new_message_dict)
        new_message2 = Message()
        new_message2.s_user_id = new_message_dict["s_user_id"]
        new_message2.d_user_id = new_message_dict["d_user_id"]
        new_message2.s_user_IK = new_message_dict["s_user_IK"]
        new_message2.s_user_EK = new_message_dict["s_user_EK"]
        new_message2.flags = new_message_dict["flags"]
        new_message2.AD = new_message_dict["AD"]

        flags = binascii.unhexlify(new_message2.flags.encode("utf-8"))
        # print(flags)
        AD = binascii.unhexlify(new_message2.AD.encode("utf-8"))
        # print(AD)
        print("密文是否一致：", compare_bytes(AD, ct))
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        decryptor = cipher.decryptor()
        print("解密后：", decryptor.update(ct))

        s_user_IK = X25519PublicKey.from_public_bytes(
            binascii.unhexlify(new_message2.s_user_IK.encode("unicode_escape")))
        s_user_EK = X25519PublicKey.from_public_bytes(
            binascii.unhexlify(new_message2.s_user_EK.encode("unicode_escape")))

        print("身份公钥是否一致：", compare_bytes(
            s_user_IK.public_bytes(
                encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw),
            mine.IdentityPub.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)))
        print("临时公钥是否一致：", compare_bytes(
            s_user_EK.public_bytes(
                encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw),
            mine.EphemeralPub.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)))

        # 通过服务器查询再次确认身份公钥一致
        if compare_bytes(
                s_user_IK.public_bytes(
                    encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw),
                mine.IdentityPub.public_bytes(encoding=serialization.Encoding.Raw,
                                              format=serialization.PublicFormat.Raw)):
            mess_node = Message_Node()
            # 关于接收链和发送链，通过识别是否对方密钥对有改变，如没有改变则仅KDF步进，如有改变则DH步进，并且发送链和接收链都需指向最新的DH下的节点。
            lastest_recv.DH_next = mess_node
            lastest_recv.KDF_next = mess_node
            mess_node.DH = other.EphemeralPri.exchange(mine.EphemeralPub)
            mess_node.KDF_input = other_DH.share_key
            lastest_recv = mess_node

    temp = root_message
    while temp.DH_next is not None:
        while temp.KDF_next is not None:
            print(binascii.hexlify(
                Signalkdf(temp.KDF_next.KDF_input, temp.KDF_next.DH)))
            temp = temp.KDF_next

    time_end = time.time()
    print("花费时间:", time_end - time_begin)
