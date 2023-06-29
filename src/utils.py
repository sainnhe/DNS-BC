# Author: Tianfu Gao
# Email: tfgao@stu.xidian.edu.cn
# License: GPL-3

import json
import os
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def get_conf():
    cur_path = os.path.realpath(__file__)
    cur_dir = os.path.dirname(cur_path)
    conf_path = cur_dir + "/../config.json"
    conf = open(conf_path)
    return json.load(conf)

def get_cert(type: str):
    cur_path = os.path.realpath(__file__)
    cur_dir = os.path.dirname(cur_path)
    cert_path = cur_dir + "/../cert/" + type + ".crt"
    key_path = cur_dir + "/../cert/" + type + ".key"
    return cert_path, key_path

def http_request_gen(domain: str, host: str):
    return "GET /?domain=" + domain + " HTTP/1.1\nHost: " + host + "\nUser-Agent: DNS-BC\nAccept-Encoding: gzip, deflate\nConnection: close"

def http_request_parse(request: str):
    tmp = re.sub('.*domain=', '', request)
    return re.sub(' HTTP.*', '', tmp).split("\n")[0]

def http_response_gen(record: str):
    return "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: 9\nConnection: close\n\n" + record

def http_response_parse(response: str):
    tmp = response.split("\n")
    return tmp[len(tmp) - 1]

def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return cipher.iv + ciphertext

def aes_decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext

