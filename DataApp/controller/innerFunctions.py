# -*- coding: utf-8 -*-
import json,requests
from DataApp.model.s_plat_user import s_plat_user
from DataApp.model.s_plat_fightbfs import s_plat_fightbfs
from DataApp.model.s_plat_fightlog import s_plat_fightlog

#周期增长分析函数，起始时间，步长，周期，排序号，类型：1同比、2叠加，是否倒序
#返回值：数组
def periodAnalyse(start,step,end,unit=0,order=1,type=1,reverse= False):
    myData = []
    i = 0
    tol_user_num = 0
    tol_game_num = 0
    while start + unit * step * i + step * (order - 1)  < end:
        uni_user = s_plat_user.query.filter(s_plat_user.regTime > start + unit * step * i + step * (order - 1)  ).filter(s_plat_user.regTime < start + unit * step * i + step * order ).all()
        uni_user_num = len(uni_user)
        uni_game = s_plat_fightlog.query.filter(s_plat_fightlog.logTime > start + unit * step * i + step * (order - 1)).filter(s_plat_fightlog.logTime < start + unit * step * i + step * order).all()
        uni_game_num = len(uni_game)
        if type == 1:
            myData.append([ start + unit * step * i + step * (order - 1), uni_user_num,uni_game_num])
        elif type == 2:
            tol_user_num += uni_user_num
            tol_game_num += uni_game_num
        i += 1
    if reverse:
        myData.reverse()
    if type == 2:
        myData = [order,tol_user_num,tol_game_num]
    return myData

# def ipToGeo(users):
#     for user in users[0:3]:
#         myurl="http://ip.taobao.com/service/getIpInfo.php?ip=39.108.126.132"
#         r = requests.get(myurl)
#         user.regIp = r.content
#     return users