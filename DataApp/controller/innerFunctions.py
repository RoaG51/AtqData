# -*- coding: utf-8 -*-
import json,urllib
from urllib import urlencode
from DataApp.model.s_plat_user import s_plat_user
from DataApp.model.s_plat_fightbfs import s_plat_fightbfs
from DataApp.model.s_plat_fightlog import s_plat_fightlog
from DataApp.model.s_data_numbyday import s_data_numbyday
from DataApp.model.s_data_numbyweek import s_data_numbyweek
from DataApp.model.s_data_numbyhour import s_data_numbyhour
from DataApp.model.s_data_usergeo import s_data_usergeo
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

def refreshLocalDbDay():
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
    i = 0
    firstItem= s_data_numbyday.query.filter(s_data_numbyday.usertolnum > 0).filter(s_data_numbyday.time == updateTime).first()
    if updateTime + secDay * (i+2) >= toDay and firstItem != None:
        return updateTime
    while updateTime + secDay * (i+1) < toDay:
        searchItem = s_data_numbyday.query.filter(s_data_numbyday.usertolnum > 0).filter(s_data_numbyday.time == updateTime + secDay * i).first()
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

def refreshLocalDbWeek():
    # 更新日期为当日开始0点
    updateItem = s_data_numbyweek.query.filter(s_data_numbyweek.usertolnum == 0).first()
    if updateItem == None:
        updateTime = time.mktime(datetime(2017, 9, 9, 0, 0, 0).timetuple())
        newUpdateItem = s_data_numbyweek(time=updateTime, usernum=0, usertolnum=0, gamenum=0, gametolnum=0)
        db.session.add(newUpdateItem)
        db.session.commit()
    else:
        updateTime = updateItem.time
    toDay = time.time()
    secWeek = 24 * 3600 * 7
    i = 0
    firstItem = s_data_numbyweek.query.filter(s_data_numbyweek.time == updateTime).filter(s_data_numbyweek.usertolnum > 0).first()
    if updateTime + secWeek * (i + 2) >= toDay and firstItem != None:
        return updateTime
    while updateTime + secWeek * (i + 1) < toDay:
        searchItem = s_data_numbyweek.query.filter(s_data_numbyweek.time == updateTime + secWeek * i).filter(s_data_numbyweek.usertolnum > 0).first()
        if searchItem == None:
            usernum = len(s_plat_user.query.filter(s_plat_user.regTime < updateTime + secWeek * (i + 1)).filter(
                s_plat_user.regTime > updateTime + secWeek * i).all())
            usertolnum = len(s_plat_user.query.filter(s_plat_user.regTime < updateTime + secWeek * (i + 1)).all())
            gamenum = len(
                s_plat_fightlog.query.filter(s_plat_fightlog.logTime < updateTime + secWeek * (i + 1)).filter(
                    s_plat_fightlog.logTime > updateTime + secWeek * i).all())
            gametolnum = len(
                s_plat_fightlog.query.filter(s_plat_fightlog.logTime < updateTime + secWeek * (i + 1)).all())
            newItem = s_data_numbyweek(time=updateTime + secWeek * i, usernum=usernum, usertolnum=usertolnum,
                                       gamenum=gamenum,
                                       gametolnum=gametolnum)
            db.session.add(newItem)
            db.session.commit()
        i += 1
    delete = s_data_numbyweek.query.filter(s_data_numbyweek.usertolnum == 0).first()
    update = s_data_numbyweek(time=updateTime + secWeek * (i - 1), usernum=0, usertolnum=0, gamenum=0, gametolnum=0)
    db.session.delete(delete)
    db.session.add(update)
    db.session.commit()
    return updateTime

def refreshLocalDbHour():
    # 更新日期为当日开始0点
    updateItem = s_data_numbyhour.query.filter(s_data_numbyhour.hour > 24).first()
    if updateItem == None:
        updateTime = time.mktime(datetime(2017, 9, 9, 0, 0, 0).timetuple())
        newUpdateItem = s_data_numbyhour(time=updateTime,hour=25, usernum=0, usertolnum=0, gamenum=0, gametolnum=0)
        db.session.add(newUpdateItem)
        db.session.commit()
    else:
        updateTime = updateItem.time
    toDay = time.time()
    secHour =  3600
    hourcounter= updateItem.hour
    i = 0
    firstItem = s_data_numbyhour.query.filter(s_data_numbyhour.time == updateTime).filter(s_data_numbyhour.hour < 25).first()
    if updateTime + secHour * (i + 1) >= toDay and firstItem != None:
        return updateTime
    while updateTime + secHour * (i + 1) < toDay:
        searchItem = s_data_numbyhour.query.filter(s_data_numbyhour.time == updateTime + secHour * i).filter(s_data_numbyhour.hour < 25).first()
        if searchItem == None:
            usernum = len(s_plat_user.query.filter(s_plat_user.regTime < updateTime + secHour * (i + 1)).filter(
                s_plat_user.regTime > updateTime + secHour * i).all())
            usertolnum = len(s_plat_user.query.filter(s_plat_user.regTime < updateTime + secHour * (i + 1)).all())
            gamenum = len(
                s_plat_fightlog.query.filter(s_plat_fightlog.logTime < updateTime + secHour * (i + 1)).filter(
                    s_plat_fightlog.logTime > updateTime + secHour * i).all())
            gametolnum = len(
                s_plat_fightlog.query.filter(s_plat_fightlog.logTime < updateTime + secHour * (i + 1)).all())
            newItem = s_data_numbyhour(time=updateTime + secHour * i, hour= (hourcounter +i-1) % 24 + 1 ,usernum=usernum, usertolnum=usertolnum,
                                       gamenum=gamenum,
                                       gametolnum=gametolnum)
            db.session.add(newItem)
            db.session.commit()
        i += 1
    delete = s_data_numbyhour.query.filter(s_data_numbyhour.hour > 24).first()
    update = s_data_numbyhour(time=updateTime + secHour * (i - 1),hour = (hourcounter +i-2) % 24 + 25, usernum=0, usertolnum=0, gamenum=0, gametolnum=0)
    db.session.delete(delete)
    db.session.add(update)
    db.session.commit()
    return updateTime

def refreshLocalUserGeo():
    #更新日期为当日开始0点
    updateItem = s_data_usergeo.query.filter(s_data_usergeo.game == -1).first()
    if updateItem == None:
        updateID = 100082
        newUpdateItem = s_data_usergeo(userid =updateID,game = -1)
        db.session.add(newUpdateItem)
        db.session.commit()
    else:
        updateID = updateItem.userid

    i = 1
    searchItem = s_plat_user.query.filter(s_plat_user.id == updateID + i).first()
    exitItem = s_data_usergeo.query.filter(s_data_usergeo.userid == updateID + i).first()
    if searchItem == None:
        return updateID
    while searchItem != None:
        if exitItem == None:
            if searchItem.wxhead == '':
                iswx = 0
                wxsex = 3
            else:
                iswx = 1
                wxsex = searchItem.wxsex
            bfs = s_plat_fightbfs.query.filter(s_plat_fightbfs.userId == searchItem.id).first()
            if not bfs:
                game = 0
            else:
                game = bfs.wins +bfs.losts

            geo = ipToGeo(searchItem.regIp)
            if type(geo) != int:
                city_code = geo["content"]["address_detail"]["city_code"]
                province = geo["content"]["address_detail"]["province"]
                city = geo["content"]["address_detail"]["city"]
                pos_x = geo["content"]["point"]["x"]
                pos_y = geo["content"]["point"]["y"]
            else:
                city_code = -1
                province = "未知省份"
                city = "未知城市"
                pos_x = geo
                pos_y = geo


        newItem = s_data_usergeo(userid=searchItem.id,ip = searchItem.regIp,city_code=city_code,province=province, city=city, pos_x= pos_x ,pos_y=pos_y,iswx=iswx,wxsex=wxsex,name=searchItem.name,game=game)
        db.session.add(newItem)
        db.session.commit()
        i += 1
        searchItem = s_plat_user.query.filter(s_plat_user.id == updateID + i).first()
    delete = s_data_usergeo.query.filter(s_data_usergeo.game == -1).first()
    update = s_data_usergeo(userid =updateID+i-1,game = -1)
    db.session.delete(delete)
    db.session.add(update)
    db.session.commit()
    return updateID

def ipToGeo(ip):
    url = "http://api.map.baidu.com/location/ip"
    params = {
        "ip": ip,  # 需要查询的IP地址或域名
        "ak": "5FpQYWxvE34C1NFUENfkEqp0CcK1bNMz"	,  # 应用APPKEY(应用详细页查询)
        "coor": "bd09ll", #百度坐标

    }
    params = urlencode(params)
    f = urllib.urlopen("%s?%s" % (url, params))
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["status"]
        if error_code == 0:
            # 成功请求
            return res
        else:
            return error_code
    else:
        return -1