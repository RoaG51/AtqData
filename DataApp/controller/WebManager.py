# -*- coding: utf-8 -*-
from DataApp.model.s_plat_user import s_plat_user
from DataApp.model.s_plat_fightbfs import s_plat_fightbfs
from DataApp.model.s_plat_fightlog import s_plat_fightlog
from DataApp.model.s_data_numbyday import s_data_numbyday
from DataApp import app,db
from flask import render_template,redirect,url_for
from datetime import datetime
from innerFunctions import periodAnalyse,refreshLocalDb
import time,math



@app.route('/')
def show_index():
    gdusers = s_plat_user.query.all()
    gsusers = s_plat_user.query.filter(s_plat_user.wxid.like("player_%")).all()

    tol_user = len(gdusers)
    tol_guest = len(gsusers)
    tol_wechat = tol_user - tol_guest
    gdgames = s_plat_fightlog.query.all()
    tol_game = len(gdgames)
    return render_template('index.html',tol_user = tol_user,tol_wechat = tol_wechat, tol_guest = tol_guest , tol_game = tol_game )


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
    refreshLocalDb()
    myData = s_data_numbyday.query.filter(s_data_numbyday.usertolnum > 0).all()
    myData.reverse()
    tol_item = len(myData)
    tol_page = int(math.ceil(tol_item / 20.0))
    cur_page = page
    return render_template('dayUpGameList.html', games=myData[20*page-20:20*page],cur_page=cur_page,tol_page=tol_page)

@app.route('/dayUpUserList')
def dayUpUserList():
    return redirect(url_for('dayUpUserListPage',page=1))
@app.route('/dayUpUserList/<int:page>')
def dayUpUserListPage(page):
    refreshLocalDb()
    myData = s_data_numbyday.query.filter(s_data_numbyday.usertolnum > 0).all()
    myData.reverse()
    tol_item = len(myData)
    tol_page = int(math.ceil(tol_item / 20.0))
    cur_page = page
    return render_template('dayUpUserList.html', users=myData[20*page-20:20*page],cur_page=cur_page,tol_page=tol_page)

@app.route('/userListByGame')
def userListByGame():
    return redirect(url_for('userListByGamePage',page=1))
@app.route('/userListByGame/<int:page>')
def userListByGamePage(page):
    gdusers = s_plat_fightbfs.query.join(s_plat_user).order_by(db.desc(s_plat_fightbfs.wins+s_plat_fightbfs.losts)).all()

    tol_item = len(gdusers)
    tol_page = int(math.ceil(tol_item /10.0))
    cur_page = page
    return render_template('userListByGame.html', users=gdusers[10 * page - 10:10 * page], cur_page=cur_page, tol_page=tol_page, tol_user = tol_item)


@app.route('/userDiagram')
def userDiagram():
    refreshLocalDb()
    myData = s_data_numbyday.query.filter(s_data_numbyday.usertolnum > 0).all()
    return render_template('userDiagram.html', datas=myData)

@app.route('/gameDiagram')
def gameDiagram():
    refreshLocalDb()
    myData = s_data_numbyday.query.filter(s_data_numbyday.usertolnum > 0).all()
    return render_template('gameDiagram.html',datas = myData)

@app.route('/userDataByGame')
def userDataByGame():
    total_users = s_plat_user.query.all()
    played_users = s_plat_fightbfs.query.all()
    myData = []
    myData.append(["0", len(total_users) - len(played_users)])
    for i in range(9):
        myData.append([str(i+1), len(s_plat_fightbfs.query.filter((s_plat_fightbfs.wins + s_plat_fightbfs.losts)==i+1).all())])
    users_10_19 = s_plat_fightbfs.query.filter((s_plat_fightbfs.wins + s_plat_fightbfs.losts) >= 10).filter((s_plat_fightbfs.wins + s_plat_fightbfs.losts) <= 19 ).all()
    users_20_29 = s_plat_fightbfs.query.filter((s_plat_fightbfs.wins + s_plat_fightbfs.losts) >= 20).filter((s_plat_fightbfs.wins + s_plat_fightbfs.losts) <= 29 ).all()
    users_10_30 = s_plat_fightbfs.query.filter((s_plat_fightbfs.wins + s_plat_fightbfs.losts) >= 30).all()
    myData.append(["10-19", len(users_10_19)])
    myData.append(["20-29", len(users_20_29)])
    myData.append(["30+", len(users_10_30)])
    return render_template('userDataByGame.html', datas = myData)

@app.route('/userDiagramByGame')
def userDiagramByGame():
    total_users = s_plat_user.query.all()
    played_users = s_plat_fightbfs.query.all()
    myData = []
    myData.append(["0", len(total_users) - len(played_users)])
    for i in range(9):
        myData.append([str(i + 1), len(
            s_plat_fightbfs.query.filter((s_plat_fightbfs.wins + s_plat_fightbfs.losts) == i + 1).all())])
    users_10_19 = s_plat_fightbfs.query.filter((s_plat_fightbfs.wins + s_plat_fightbfs.losts) >= 10).filter(
        (s_plat_fightbfs.wins + s_plat_fightbfs.losts) <= 19).all()
    users_20_29 = s_plat_fightbfs.query.filter((s_plat_fightbfs.wins + s_plat_fightbfs.losts) >= 20).filter(
        (s_plat_fightbfs.wins + s_plat_fightbfs.losts) <= 29).all()
    users_10_30 = s_plat_fightbfs.query.filter((s_plat_fightbfs.wins + s_plat_fightbfs.losts) >= 30).all()
    myData.append(["10-19", len(users_10_19)])
    myData.append(["20-29", len(users_20_29)])
    myData.append(["30+", len(users_10_30)])
    return render_template('userDiagramByGame.html',datas = myData)

@app.route('/periodAnalyseByDay')
def periodAnalyseByDay():
    return redirect(url_for('periodAnalyseByDayOrder', order=1))
@app.route('/periodAnalyseByDay/<int:order>')
def periodAnalyseByDayOrder(order):
    secHour = 3600
    firstDay = datetime(2017, 9, 9, 0, 0, 0)
    firstDay = time.mktime(firstDay.timetuple())
    toDay = time.time()
    myData = periodAnalyse(start=firstDay, step=secHour, end=toDay, unit=24, order=order)
    return render_template('testList.html', datas=myData)

@app.route('/periodAnalyseByDayTotal')
def periodAnalyseByDayTotal():
    secHour = 3600
    firstDay = datetime(2017, 9, 9, 0, 0, 0)
    firstDay = time.mktime(firstDay.timetuple())
    toDay = time.time()
    myData = []
    for order in range(24):
        myData.append(periodAnalyse(start=firstDay, step=secHour, end=toDay, unit=24, order=order + 1, type=2))
    return render_template('testList.html')

@app.route('/periodAnalyseByWeek')
def periodAnalyseByWeek():
    return redirect(url_for('periodAnalyseByWeekOrder', order=1))
@app.route('/periodAnalyseByWeek/<int:order>')
def periodAnalyseByWeekOrder(order):
    secDay = 24 * 3600
    firstDay = datetime(2017, 9, 9, 0, 0, 0)
    firstDay = time.mktime(firstDay.timetuple())
    toDay = time.time()
    myData = periodAnalyse(start=firstDay, step=secDay, end=toDay, unit=7, order=order)
    return render_template('periodAnalyseByWeek.html',datas = myData,order = order)

@app.route('/periodAnalyseByWeekTotal')
def periodAnalyseByWeekTotal():
    secDay = 24 * 3600
    firstDay = datetime(2017, 9, 9, 0, 0, 0)
    firstDay = time.mktime(firstDay.timetuple())
    toDay = time.time()
    myData = []
    for i in range(7):
        myData.append(periodAnalyse(start=firstDay, step=secDay, end=toDay, unit=7, order=i+1,type=2))
    return render_template('periodAnalyseByWeekTotal.html', datas=myData)

@app.route('/userDiagramBySex')
def userDiagramBySex():
    wxmale = s_plat_user.query.filter(s_plat_user.wxid.like("o0%")).filter(s_plat_user.wxsex == 1).all()
    wxfemale = s_plat_user.query.filter(s_plat_user.wxid.like("o0%")).filter(s_plat_user.wxsex == 2).all()
    gsusers = s_plat_user.query.filter(s_plat_user.wxid.like("player_%")).all()
    myData = []
    myData.append([u"游客", len(gsusers)])
    myData.append([u"男性注册用户", len(wxmale)])
    myData.append([u"女性注册用户", len(wxfemale)])
    return render_template('userDiagramBySex.html',datas = myData)

@app.route('/gameDiagramByNum')
def gameDiagramByNum():
    game_6 = s_plat_fightlog.query.filter(s_plat_fightlog.u7 == None).all()
    game_7 = s_plat_fightlog.query.filter(s_plat_fightlog.u7 != None).filter(s_plat_fightlog.u8 == None).all()
    game_8 = s_plat_fightlog.query.filter(s_plat_fightlog.u8 != None).all()
    myData = []
    myData.append([u"6人局", len(game_6)])
    myData.append([u"7人局", len(game_7)])
    myData.append([u"8人局", len(game_8)])
    return render_template('gameDiagramByNum.html',datas = myData)

@app.route('/winrateDiagramByNum')
def winrateDiagramByNum():
    return redirect(url_for('winrateDiagramByNumPage', num=6))
@app.route('/winrateDiagramByNum/<int:num>')
def winrateDiagramByNumPage(num):
    if num == 6:
        xy = s_plat_fightlog.query.filter(s_plat_fightlog.u7 == None).filter(s_plat_fightlog.isHaoren == 1).all()
        lcf = s_plat_fightlog.query.filter(s_plat_fightlog.u7 == None).filter(s_plat_fightlog.isHaoren == 0).all()
        title = u"6人局"
    elif num == 7:
        xy = s_plat_fightlog.query.filter(s_plat_fightlog.u7 != None).filter(s_plat_fightlog.u8 == None).filter(s_plat_fightlog.isHaoren == 1).all()
        lcf = s_plat_fightlog.query.filter(s_plat_fightlog.u7 != None).filter(s_plat_fightlog.u8 == None).filter(s_plat_fightlog.isHaoren == 0).all()
        title = u"7人局"
    elif num == 8:
        xy = s_plat_fightlog.query.filter(s_plat_fightlog.u8 != None).filter(s_plat_fightlog.isHaoren == 1).all()
        lcf = s_plat_fightlog.query.filter(s_plat_fightlog.u8 != None).filter(s_plat_fightlog.isHaoren == 0).all()
        title = u"7人局"
    else :
        xy = s_plat_fightlog.query.filter(s_plat_fightlog.isHaoren == 1).all()
        lcf = s_plat_fightlog.query.filter(s_plat_fightlog.isHaoren == 0).all()
        title = u"全部局"
    myData = []
    myData.append([u"许愿阵营获胜", len(xy)])
    myData.append([u"老朝奉阵营获胜", len(lcf)])
    return render_template('winrateDiagramByNum.html', datas=myData, title = title)
