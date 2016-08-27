#!/usr/bin/python
# _*_ encoding:utf-8_*_
# __author__ = "Miles.Peng"
# # encoding:utf-8
# from Crypto.Cipher import AES
# from Crypto import Random
#
# def encrypt(data, password):
#     bs = AES.block_size
#     pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
#     iv = Random.new().read(bs)
#     cipher = AES.new(password, AES.MODE_CBC, iv)
#     data = cipher.encrypt(pad(data))
#     data = iv + data
#     return data
#
# def decrypt(data, password):
#     bs = AES.block_size
#     if len(data) <= bs:
#         return data
#     unpad = lambda s : s[0:-ord(s[-1])]
#     iv = data[:bs]
#     cipher = AES.new(password, AES.MODE_CBC, iv)
#     data  = unpad(cipher.decrypt(data[bs:]))
#     return data
#

#
#
#
# if __name__ == '__main__':
#     data = 'miles peng'
#     #16,24,32位长的密码
#     import sys
#     password = fill_leng(sys.argv[2])
#     method=sys.argv[1]
#     if method=='1':
#         encrypt_data = encrypt(data, password)
#         print 'encrypt_data:', encrypt_data
#     elif method=='0':
#         encrypt_data=sys.argv[3]
#         decrypt_data = decrypt(encrypt_data, password)
#         print 'decrypt_data:', decrypt_data

from crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import sys
class AESCrypto():

    @classmethod
    def __fill_leng(self,key):
        _len=[16,24,32]
        if len(key) in _len:
            return key
        else:
            is_fill=False
            for check_len in _len:
                if len(key)<check_len:
                    password=key.ljust(check_len,'\0')
                    is_fill=True
                    return password
            if not is_fill:
                print "Password is so long to can`t encrypt!"

    def __init__(self,key):
        self.key = key
        self.mode = AES.MODE_CBC
        self.values=b'0000000000000000'
        self.__fill_leng(key)



    #print AES.block_size


    def encrypt(self,text):
        if len(text)%16!=0:
            text=text+str((16-len(text)%16)*'0')
        cryptor = AES.new(self.key,self.mode,self.values)
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self,text):
        cryptor = AES.new(self.key,self.mode,self.values)
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')



if __name__ == '__main__':
    #password_=sys.argv[1]
    password_="123"
    pc = AESCrypto('milespeng') #初始化密钥
    e = pc.encrypt(password_)
    d = pc.decrypt(e) #解密
    print "加密:",e
    print "解密:",d