# -*- coding: utf-8 -*-
from DataApp.model.s_plat_user import s_plat_user
from DataApp.model.s_plat_fightbfs import s_plat_fightbfs
from DataApp.model.s_plat_fightlog import s_plat_fightlog
from DataApp import app
from flask import render_template,redirect,url_for
from datetime import datetime
import time,math

@app.route('/')
def show_index():
    gdusers = s_plat_user.query.all()
    wxusers = s_plat_user.query.filter(s_plat_user.wxid.like("player_%")).all()
    tol_user = len(gdusers)
    tol_guest = len(wxusers)
    tol_wechat = tol_user - tol_guest
    gdgames = s_plat_fightlog.query.all()
    tol_game = len(gdgames)
    return render_template('index.html',tol_user = tol_user,tol_wechat = tol_wechat, tol_guest = tol_guest , tol_game = tol_game)

@app.route('/gameList')
def gameList():
    return redirect(url_for('gameListPage', page=1))
@app.route('/gameList/<int:page>')
def gameListPage(page):
    gdgames = s_plat_fightlog.query.all()
    tol_item = len(gdgames)
    tol_page = int(math.ceil(tol_item/20.0))
    cur_page = page
    return render_template('gameList.html', games=gdgames[20*page-20:20*page], cur_page = cur_page, tol_page = tol_page, tol_game = tol_item )

@app.route('/userList')
def userList():
    return redirect(url_for('userListPage',page=1))
@app.route('/userList/<int:page>')
def userListPage(page):
    gdusers = s_plat_user.query.all()
    wxusers = s_plat_user.query.filter(s_plat_user.wxid.like("player_%")).all()
    users = []
    for user in gdusers[10 * page - 10:10 * page]:
        userbfs = s_plat_fightbfs.query.filter(s_plat_fightbfs.userId == user.id).all()
        if not userbfs:
            users.append([user,0])
        else:
            users.append([user,userbfs[0].wins + userbfs[0].losts])
    tol_item = len(gdusers)
    tol_guest = len(wxusers)
    tol_wechat = tol_item - tol_guest

    tol_page = int(math.ceil(tol_item / 10.0))
    cur_page = page
    return render_template('userList.html', users=users,cur_page=cur_page,tol_page=tol_page,tol_user = tol_item, tol_wechat = tol_wechat, tol_guest = tol_guest)

@app.route('/dayUpGameList')
def dayUpGameList():
    return redirect(url_for('dayUpGameListPage',page=1))
@app.route('/dayUpGameList/<int:page>')
def dayUpGameListPage(page):
    secDay = 24 * 3600
    firstDay = datetime(2017, 9, 9, 0, 0, 0)
    firstDay = time.mktime(firstDay.timetuple())
    toDay = time.time()
    myData = []
    preNum = 0
    i = 0
    while firstDay + secDay * i < toDay:
        gdusers = s_plat_fightlog.query.filter(s_plat_fightlog.logTime < firstDay + secDay * (i + 1)).all()
        Num = len(gdusers)
        myData.append([firstDay + secDay * i, Num, Num - preNum])
        preNum = Num
        i += 1
    tol_item = len(myData)
    tol_page = int(math.ceil(tol_item / 20.0))
    cur_page = page
    return render_template('dayUpGameList.html', games=myData[20*page-20:20*page],cur_page=cur_page,tol_page=tol_page)

@app.route('/dayUpUserList')
def dayUpUserList():
    return redirect(url_for('dayUpUserListPage',page=1))
@app.route('/dayUpUserList/<int:page>')
def dayUpUserListPage(page):
    secDay = 24 * 3600
    firstDay = datetime(2017, 9, 9, 0, 0, 0)
    firstDay = time.mktime(firstDay.timetuple())
    toDay = time.time()
    myData = []
    preNum = 0
    i = 0
    while firstDay + secDay * i < toDay:
        gdusers = s_plat_user.query.filter(s_plat_user.regTime < firstDay + secDay * (i + 1)).all()
        Num = len(gdusers)
        myData.append([firstDay + secDay * i, Num, Num - preNum])
        preNum = Num
        i += 1
    tol_item = len(myData)
    tol_page = int(math.ceil(tol_item / 20.0))
    cur_page = page
    return render_template('dayUpUserList.html', users=myData[20*page-20:20*page],cur_page=cur_page,tol_page=tol_page)




@app.route('/userDiagram')
def userDiagram():
    secDay = 24 * 3600
    firstDay = datetime(2017,9,9,0,0,0)
    firstDay = time.mktime(firstDay.timetuple())
    toDay = time.time()
    myData=[]
    preNum = 0
    i =0
    while firstDay+secDay*i < toDay:
        gdusers = s_plat_user.query.filter(s_plat_user.regTime <firstDay+secDay*(i+1)).all()
        Num = len(gdusers)
        myData.append([firstDay+secDay*i,Num,Num-preNum])
        preNum = Num
        i += 1
    return render_template('userDiagram.html',datas = myData)

@app.route('/gameDiagram')
def gameDiagram():
    secDay = 24 * 3600
    firstDay = datetime(2017,9,9,0,0,0)
    firstDay = time.mktime(firstDay.timetuple())
    toDay = time.time()
    myData=[]
    preNum = 0
    i =0
    while firstDay+secDay*i < toDay:
        gdusers = s_plat_fightlog.query.filter(s_plat_fightlog.logTime <firstDay+secDay*(i+1)).all()
        Num = len(gdusers)
        myData.append([firstDay+secDay*i,Num,Num-preNum])
        preNum = Num
        i += 1
    return render_template('gameDiagram.html',datas = myData)

