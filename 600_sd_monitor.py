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


def sd_monitor():
    sd_monitor_dict={"step": 600,"endpoint": get_ip(),"tags": "leengine-sd=sd_monitor","timestamp": int(time.time()),"metric": "sd_monitor","value": 0.00,"counterType": "GAUGE"}
    sd_monitor_proc = subprocess.Popen("tail -n 1000 /var/log/leengine-sd/monitor.log  | grep '\[C\]'", shell=True, stdout=subprocess.PIPE)

    sd_monitor_output = sd_monitor_proc.communicate()[0]
    if sd_monitor_output == "":
        sd_monitor_dict["value"] = 0.0
    else:
        sd_monitor_dict["value"] = 1.0
    falcon_list.append(sd_monitor_dict)

if __name__ == "__main__":
    sd_monitor()
    print json.dumps(falcon_list)