# Author: Tianfu Gao
# Email: tfgao@stu.xidian.edu.cn
# License: GPL-3

import socket
import ssl
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import utils
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class Connection:
    def __init__(self, type="server", protocol="tcp", host="0.0.0.0", port=3456, message_size=1024):
        self.type = type
        self.protocol = protocol
        self.host = host
        self.port = port
        self.message_size = message_size
        if self.protocol == "dok":
            if self.type == "server":
                self.server_key = generate_key()
                self.server_sk = self.server_key.secret
                self.server_pk = self.server_key.public_key.format(True)
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.bind((self.host, self.port))
                self.socket.listen()
                self.conn, self.addr = self.socket.accept()
                self.conn.sendall(self.server_pk)
                self.client_pk = decrypt(self.server_sk, self.conn.recv(self.message_size))
                print("Server listening on " + self.host + ":" + str(self.port))
            else:
                self.client_key = generate_key()
                self.client_sk = self.client_key.secret
                self.client_pk = self.client_key.public_key.format(True)
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.server_pk = self.socket.recv(self.message_size)
                self.socket.sendall(encrypt(self.server_pk, self.client_pk))
        elif self.protocol == "tcp+aes":
            if self.type == "server":
                self.aes_key = get_random_bytes(32)
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.bind((self.host, self.port))
                self.socket.listen()
                self.conn, self.addr = self.socket.accept()
                self.conn.sendall(self.aes_key)
                print("Server listening on " + self.host + ":" + str(self.port))
            else:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.aes_key = self.socket.recv(self.message_size)
        else:
            if self.type == "server":
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.bind((self.host, self.port))
                self.socket.listen()
                print("Server listening on " + self.host + ":" + str(self.port))

    def recv(self) -> bytes:
        if self.protocol == "dok":
            if self.type == "server":
                return decrypt(self.server_sk, self.conn.recv(self.message_size))
            else:
                return decrypt(self.client_sk, self.socket.recv(self.message_size))
        elif self.protocol == "tcp+aes":
            if self.type == "server":
                return utils.aes_decrypt(self.conn.recv(self.message_size), self.aes_key)
            else:
                return utils.aes_decrypt(self.socket.recv(self.message_size), self.aes_key)
        else:
            if self.type == "server":
                self.conn, self.addr = self.socket.accept()
                if self.protocol == "tls" or self.protocol == "https":
                    cert, key = utils.get_cert("server")
                    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                    ssl_context.load_cert_chain(certfile=cert, keyfile=key)
                    self.conn = ssl_context.wrap_socket(self.conn, server_side=True)
                data = self.conn.recv(self.message_size)
                if self.protocol == "https":
                    data = utils.http_request_parse(data.decode("utf-8")).encode("utf-8")
                return data
            else:
                data = self.socket.recv(self.message_size)
                self.socket.close()
                if self.protocol == "https":
                    data = utils.http_response_parse(data.decode("utf-8")).encode("utf-8")
                return data

    def send(self, data: bytes):
        if self.protocol == "dok":
            if self.type == "server":
                self.conn.sendall(encrypt(self.client_pk, data))
            else:
                self.socket.sendall(encrypt(self.server_pk, data))
        elif self.protocol == "tcp+aes":
            if self.type == "server":
                self.conn.sendall(utils.aes_encrypt(data, self.aes_key))
            else:
                self.socket.sendall(utils.aes_encrypt(data, self.aes_key))
        else:
            if self.type == "server":
                if self.protocol == "https":
                    data = utils.http_response_gen(data.decode("utf-8")).encode("utf-8")
                self.conn.sendall(data)
                self.conn.close()
            else:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if self.protocol == "tls" or self.protocol == "https":
                    client_cert, client_key = utils.get_cert("client")
                    server_cert, server_key = utils.get_cert("server")
                    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
                    ssl_context.load_cert_chain(certfile=client_cert, keyfile=client_key)
                    ssl_context.load_verify_locations(cafile=server_cert)
                    self.socket = ssl_context.wrap_socket(self.socket, server_hostname=self.host)
                if self.protocol == "https":
                    data = utils.http_request_gen(data.decode("utf-8"), self.host).encode("utf-8")
                self.socket.connect((self.host, self.port))
                self.socket.sendall(data)

    def close(self):
        if self.type == "server":
            self.conn.close()
            self.socket.close()
        else:
            self.socket.close()
