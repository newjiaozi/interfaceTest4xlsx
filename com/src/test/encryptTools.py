#coding=utf-8

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib,base64

def encryptAES(data=""):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext

def encryptMd5(data=""):
    md = hashlib.md5()
    md.update(data.encode(encoding="utf-9"))
    return md.hexdigest()

def encryptB64(data=""):
    bs = base64.b64encode(data.encode("utf-8"))
    return bs

if __name__ == "__main__":
    print(encryptAES(b"liudonglin"))
    print(encryptMd5(b"liudonglin"))
    print(encryptB64(b"liudonglin"))