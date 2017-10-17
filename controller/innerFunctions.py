# -*- coding: utf-8 -*-
import json,requests

def ipToGeo(users):
    for user in users[0:3]:
        myurl="http://ip.taobao.com/service/getIpInfo.php?ip=39.108.126.132"
        r = requests.get(myurl)
        user.regIp = r.content
    return users