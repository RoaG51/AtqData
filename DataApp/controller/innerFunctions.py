# -*- coding: utf-8 -*-
import json,requests
from DataApp.model.s_plat_user import s_plat_user
from DataApp.model.s_plat_fightbfs import s_plat_fightbfs
from DataApp.model.s_plat_fightlog import s_plat_fightlog
from DataApp.model.s_data_numbyday import s_data_numbyday
from datetime import datetime
from DataApp import db
import time


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

def refreshLocalDb():
    #更新日期为当日开始0点
    updateItem = s_data_numbyday.query.filter(s_data_numbyday.usertolnum == 0).first()
    if updateItem == None:
        updateTime = time.mktime(datetime(2017, 9, 9, 0, 0, 0).timetuple())
        newUpdateItem = s_data_numbyday(time =updateTime,usernum=0,usertolnum=0,gamenum=0,gametolnum=0 )
        db.session.add(newUpdateItem)
        db.session.commit()
    else:
        updateTime = updateItem.time

    toDay = time.time()
    secDay = 24 * 3600
    myData = []
    i = 0
    while updateTime + secDay * (i+1) < toDay:
        searchItem = s_data_numbyday.query.filter(s_data_numbyday.time == updateTime + secDay * i).first()
        if searchItem == None:
            usernum = len(s_plat_user.query.filter(s_plat_user.regTime < updateTime + secDay * (i+1)).filter(
                s_plat_user.regTime > updateTime + secDay * i).all())
            usertolnum = len(s_plat_user.query.filter(s_plat_user.regTime < updateTime + secDay * (i+1)).all())
            gamenum = len(s_plat_fightlog.query.filter(s_plat_fightlog.logTime < updateTime + secDay * (i + 1)).filter(
                s_plat_fightlog.logTime > updateTime + secDay * i).all())
            gametolnum = len(s_plat_fightlog.query.filter(s_plat_fightlog.logTime < updateTime + secDay * (i+1)).all())

            newItem = s_data_numbyday( time=updateTime + secDay * i, usernum=usernum, usertolnum=usertolnum, gamenum=gamenum,
                                      gametolnum=gametolnum)
            db.session.add(newItem)
            db.session.commit()
        i += 1
    delete = s_data_numbyday.query.filter(s_data_numbyday.usertolnum == 0).first()
    update = s_data_numbyday(time=updateTime + secDay * (i-1), usernum=0, usertolnum=0, gamenum=0, gametolnum=0)
    db.session.delete(delete)
    db.session.add(update)
    db.session.commit()

    return updateTime



# def ipToGeo(users):
#     for user in users[0:3]:
#         myurl="http://ip.taobao.com/service/getIpInfo.php?ip=39.108.126.132"
#         r = requests.get(myurl)
#         user.regIp = r.content
#     return users