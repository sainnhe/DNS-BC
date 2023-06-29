# Author: Tianfu Gao
# Email: tfgao@stu.xidian.edu.cn
# License: GPL-3

import subprocess
import os
import utils
import re
import json

cur_path = os.path.realpath(__file__)
cur_dir = os.path.dirname(cur_path)
script_path = cur_dir + "/../run.sh"

def init():
    subprocess.run([script_path, "invoke", '{"function":"InitLedger","Args":[]}'], stdout=subprocess.DEVNULL)
    conf = utils.get_conf()
    records: dict[str, list[str]] = conf["records"]
    cred: dict[str, str] = conf["credibility"]
    for domain in records:
        subprocess.run([script_path, "invoke", '{"function":"CreateAsset","Args":["' + domain + '", "' + records[domain][0] + '", "' + records[domain][1] + '", "' + cred[records[domain][1]] + '", "' + records[domain][1] + '"]}'], stdout=subprocess.DEVNULL)

def query(domain: str):
    # Something like
    # 2023-03-23 03:01:25.673 UTC 0001 INFO [chaincodeCmd] chaincodeInvokeOrQuery -> Chaincode invoke successful. result: status:200 payload:"{\"Domain\":\"localhost\",\"Record\":\"127.0.0.1\",\"Owner\":\"Authority\",\"CredibilityVal\":1,\"CredibilityUsr\":\"Authority\"}"
    raw_result = subprocess.run([script_path, "invoke", '{"function":"ReadAsset","Args":["' + domain + '"]}'], stderr=subprocess.PIPE).stderr.decode("utf-8")
    raw_result = re.sub("\n", '', raw_result)
    raw_result = re.sub('.*payload:"', '', raw_result)
    raw_result = re.sub('" $', '', raw_result)
    raw_result = raw_result.replace("\\", "")
    result: dict[str, str] = json.loads(raw_result)
    return result

def query_record(domain: str):
    raw_result = subprocess.run([script_path, "invoke", '{"function":"ReadAsset","Args":["' + domain + '"]}'], stderr=subprocess.PIPE).stderr.decode("utf-8")
    raw_result = re.sub("\n", '', raw_result)
    raw_result = re.sub('.*payload:"', '', raw_result)
    raw_result = re.sub('" $', '', raw_result)
    raw_result = raw_result.replace("\\", "")
    result: dict[str, str] = json.loads(raw_result)
    return result["Record"]

def query_credibility(domain: str):
    raw_result = subprocess.run([script_path, "invoke", '{"function":"ReadAsset","Args":["' + domain + '"]}'], stderr=subprocess.PIPE).stderr.decode("utf-8")
    raw_result = re.sub("\n", '', raw_result)
    raw_result = re.sub('.*payload:"', '', raw_result)
    raw_result = re.sub('" $', '', raw_result)
    raw_result = raw_result.replace("\\", "")
    result: dict[str, str] = json.loads(raw_result)
    return result["CredibilityVal"]
