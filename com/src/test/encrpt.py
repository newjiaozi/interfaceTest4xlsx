#coding=utf-8

import rsa
import binascii
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def getNE():
    resp = requests.post("https://www.dongmanmanhua.cn/member/login/rsa/getKeys")
    resp_json = resp.json()
    evalue = resp_json["evalue"]
    keyName = resp_json["keyName"]
    nvalue = resp_json["nvalue"]
    sessionKey = resp_json["sessionKey"]
    return keyName,evalue,nvalue,sessionKey

def rsaByCipher(rsa_n,rsa_e,sessionKey,mobile,passwd):
    key = RSA.construct((int(rsa_e,16),int(rsa_n,16)))
    message = chr(len(sessionKey))+sessionKey+chr(len(mobile))+mobile+chr(len(passwd))+passwd
    print(message)
    ciper_rsa = PKCS1_OAEP.new(key)
    message = ciper_rsa.encrypt(message.encode())
    print(message)
    message = binascii.b2a_hex(message)
    print(message,len(message))
    print(message.decode())
    return message.decode()

def rsaEnc(rsa_n,rsa_e,sessionKey,mobile,passwd):
    key = rsa.PublicKey(int(rsa_e,16),int(rsa_n,16))
    message = chr(len(sessionKey))+sessionKey+chr(len(mobile))+mobile+chr(len(passwd))+passwd
    print(message)
    message = rsa.encrypt(message.encode(),key)
    print(message)
    message = binascii.b2a_hex(message)
    print(message,len(message))
    print(message.decode())
    return message.decode()

def getLoin(mobile="13683580001",passwd="111111"):
    ne = getNE()
    encpw = rsaByCipher(ne[2], ne[1], ne[3], mobile=mobile, passwd=passwd)
    encnm = ne[0]
    # encnm = 9
    loginType = "PHONE_NUMBER"
    serviceZone = "CHINA"
    data={"encnm":encnm,"encpw":encpw,"loginType":loginType,"serviceZone":serviceZone}
    resp = requests.post("https://www.dongmanmanhua.cn/member/login/doLoginById",json=data)
    print(resp.status_code)

getLoin()









