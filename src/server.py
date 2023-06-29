# Author: Tianfu Gao
# Email: tfgao@stu.xidian.edu.cn
# License: GPL-3

import connection
import utils
import blockchain
import json
import random

conf = utils.get_conf()


class Server:
    def __init__(self, cache_type="hashmap"):
        """Start a server

        Args:
            cache_type (string): Cache type. Possible values are "hashmap" and "blockchain"
        """
        self.type = cache_type
        # Init log
        if cache_type == "hashmap":
            self.log = open("hashmap.log", "a")
        else:
            self.log = open("blockchain.log", "a")
        # Init cache
        if cache_type == "hashmap":
            self.records: dict[str, list[str]] = conf["records"]
        elif cache_type == "blockchain":
            blockchain.init()
        else:
            print("Invalid cache type.")
            exit(1)
        # Init connection
        self.conn = connection.Connection(
            type="server", protocol=conf["protocol"], host=conf["host"], port=conf["port"], message_size=conf["message_size"])

    def query_hm(self, domain: str):
        try:
            result = self.records[domain][0]
        except:
            result = "Not found."
        return result

    def query_bc(self, domain: str):
        if conf["arch"] == "mono":
            try:
                result = blockchain.query(domain)
                record = result["Record"]
                credibility = float(result["CredibilityVal"])
            except:
                return "Not Found."
        else:
            try:
                record = blockchain.query_record(domain)
                credibility = float(blockchain.query_credibility(domain))
            except:
                return "Not Found."
        random_num = random.random()
        if random_num <= credibility:
            return record
        else:
            return blockchain.query_record(domain)

    def serve(self):
        while True:
            request: str = self.conn.recv().decode("utf-8")
            if request == "exit":
                self.conn.close()
                self.log.close()
                print("Server connection closed.")
                break
            if self.type == "hashmap":
                response = self.query_hm(request)
                self.conn.send(response.encode("utf-8"))
                self.log.write(request + "\n")
                self.log.write(response + "\n")
                print("Request: " + request + "\nResponse: " + response)
            else:
                response = self.query_bc(request)
                self.conn.send(response.encode("utf-8"))
                self.log.write(json.dumps(
                    response, separators=(",", ":")) + "\n")
                print(json.dumps(response, separators=(",", ":")))


s = Server(cache_type=conf["type"])
s.serve()
