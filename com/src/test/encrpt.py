#coding=utf-8

import rsa
import binascii
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from com.src.test.logs import logger
import urllib3
from com.src.test.actionJava import encpwByJava

# host = "https://qaapis.dongmanmanhua.cn"
# host = "http://dev.dongmanmanhua.cn"
host = "https://qaptsapis.dongmanmanhua.cn"
def getNE():
    resp = requests.get(host+"/member/login/rsa/getKeys")
    resp_json = resp.json()
    evalue = resp_json["evalue"]
    keyName = resp_json["keyName"]
    nvalue = resp_json["nvalue"]
    sessionKey = resp_json["sessionKey"]
    return keyName,evalue,nvalue,sessionKey

def getNeAndroid():
    urllib3.disable_warnings()
    resp = requests.get(host+"/app/rsakey/get",verify=False)
    # print(resp,resp.text)
    resp_json = resp.json()
    evalue = resp_json["message"]["result"]["evalue"]
    keyName = resp_json["message"]["result"]["keyName"]
    nvalue = resp_json["message"]["result"]["nvalue"]
    sessionKey = resp_json["message"]["result"]["sessionKey"]
    return keyName,evalue,nvalue,sessionKey

def rsaByCipher(rsa_n,rsa_e,sessionKey,mobile,passwd):
    key = RSA.construct((int(rsa_e,16),int(rsa_n,16)))
    message = chr(len(sessionKey))+sessionKey+chr(len(mobile))+mobile+chr(len(passwd))+passwd
    # print(message)
    ciper_rsa = PKCS1_OAEP.new(key)
    message = ciper_rsa.encrypt(message.encode())
    # print(message)
    message = binascii.b2a_hex(message).decode()
    return message.decode()

def rsaEnc(rsa_n,rsa_e,sessionKey,mobile,passwd):
    rsa_e = rsa_e.lower()
    rsa_n = rsa_n.lower()
    key = rsa.PublicKey(int(rsa_e,16),int(rsa_n,16))
    message = chr(len(sessionKey))+sessionKey+chr(len(mobile))+mobile+chr(len(passwd))+passwd
    # print(message)
    message = rsa.encrypt(message.encode(),key)
    # print(message)
    message = binascii.b2a_hex(message)
    # print(message,len(message))
    # print(message.decode())
    return message.decode()

def getLoin(mobile="13683580001",passwd="111111"):
    # ne = getNE()
    ne = getNeAndroid()
    # print(ne)
    language = "zh-hans"
    logger.info("%s:%s" % (mobile,passwd))
    encpw = rsaEnc(ne[2], ne[1], ne[3], mobile=mobile, passwd=passwd)
    # encpw = encpwByJava(mobile, passwd, ne[3],ne[1],ne[2])
    encnm = ne[0]
    # encnm = 9
    loginType = "PHONE_NUMBER"
    # loginType = "PHONE_VERIFICATION_CODE"
    serviceZone = "CHINA"
    data={"encnm":encnm,"encpw":encpw,"loginType":loginType,"serviceZone":serviceZone,"language":language,"v":1,"platform":"APP_ANDROID"}
    # resp = requests.post("http://dev.dongmanmanhua.cn/member/login/doLoginById",json=data)
    # payload = {"md5":"q4vOE8iwEM3fl0Po0wm0cw","expires":"1542866118"}
    # cookies = {"uuid":"92b0c90e60861ac06f93c092ad82cc9d"}
    # resp = requests.post(" http://dev.dongmanmanhua.cn/app/member/id/login", data=data,headers={"Content-Type":"application/x-www-form-urlencoded","HOST":"dev.apis.dongmanmanhua.cn"})
    # print(resp.status_code,resp.text)
    return data







if __name__ == "__main__":
    print(getLoin(mobile="15010173763",passwd="123qwe"))
    # print(getNeAndroid())