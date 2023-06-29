# Author: Tianfu Gao
# Email: tfgao@stu.xidian.edu.cn
# License: GPL-3

import connection
import utils
import time

conf = utils.get_conf()

log = open("client.log", "a")
log.write("Request   Response   Time (s)\n")

conn = connection.Connection(type="client", protocol=conf["protocol"], host=conf["host"], port=conf["port"], message_size=conf["message_size"])

print("Input \"exit\" to exit.")
print("Domain to query: ", end="")
request = input()
while request != "exit":
    start_time = time.time()
    conn.send(request.encode("utf-8"))
    response: bytes = conn.recv()
    end_time = time.time()
    print("Record: " + response.decode("utf-8"))
    print("Domain to query: ", end="")
    log.write(request + "   " + response.decode("utf-8") + "   " + str(end_time - start_time) + "\n")
    request = input()

conn.send("exit".encode("utf-8"))
conn.close()
print("Client connection closed.")
