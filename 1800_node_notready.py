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


def node_not_ready():
    node_not_ready_dict={"step": 1800,"endpoint": get_ip(),"tags": "leengine-kube=node_not_ready","timestamp": int(time.time()),"metric": "kube_node_not_ready","value": 0.00,"counterType": "GAUGE"}
    node_not_ready_proc = subprocess.Popen("kubectl --server=0.0.0.0:6222 get node | grep NotReady | wc -l", shell=True, stdout=subprocess.PIPE)
    node_not_ready_output = node_not_ready_proc.communicate()[0]
    if int(node_not_ready_output) < 2:
        node_not_ready_dict["value"] = 0.0
    else:
        node_not_ready_dict["value"] = 1.0
    falcon_list.append(node_not_ready_dict)

if __name__ == "__main__":
    node_not_ready()
    print json.dumps(falcon_list)