#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import time
import codecs
import json

falcon_list = []


def get_ip():
    ip=""
    f = codecs.open('/usr/local/LeMonitor/falcon-agent/cfg.json','r','utf-8')
    for l in f:
        s = l.strip().split(' ')
        if s[0] == '"hostname":':
            ip = str(s[1]).strip(",").strip("\"")
    return ip


def ovs_bad_port():
    ovs_bad_port_dict={"step": 600,"endpoint": get_ip(),"tags": "leengine-cni=ovs_bad_port","timestamp": int(time.time()),"metric": "cni-ovs-bad-port","value": 0.00,"counterType": "GAUGE"}
    ovs_output = subprocess.check_output("ovs-vsctl show | grep error | awk '{print $7}'", shell=True)
    if ovs_output == "":
        ovs_bad_port_dict["value"] = 0.0
    else:
        ovs_bad_port_dict["value"] = 1.0
    falcon_list.append(ovs_bad_port_dict)

if __name__ == "__main__":
    ovs_bad_port()
    print json.dumps(falcon_list)