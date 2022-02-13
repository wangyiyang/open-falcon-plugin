#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import json
import time
import codecs

falcon_list = []


def get_ip():
    ip=""
    ts = int(time.time())
    f = codecs.open('/usr/local/LeMonitor/falcon-agent/cfg.json','r','utf-8')
    for l in f:
        s = l.strip().split(' ')
        if s[0] == '"hostname":':
            ip = str(s[1]).strip(",").strip("\"")
    return ip
    

def ipam_check():
    ipam_check_dict={"step": 1800,"endpoint": get_ip(),"tags": "leengine-cni=ipam_check","timestamp": int(time.time()),"metric": "cni-ipam-check","value": 0.00,"counterType": "GAUGE"}
    ipam_check_output = subprocess.check_output("leengine-cnictl ipam check |wc -l", shell=True)
    lost_ip = int(ipam_check_output) - 4
    if lost_ip > 10:
        ipam_check_dict["value"] = 1.0
    else:
        ipam_check_dict["value"] = 0.0
    falcon_list.append(ipam_check_dict)

if __name__ == "__main__":
    ipam_check()
    print json.dumps(falcon_list)