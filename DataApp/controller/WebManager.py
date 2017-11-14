# -*- coding: utf-8 -*-
from DataApp.model.s_plat_user import s_plat_user
from DataApp.model.s_plat_fightbfs import s_plat_fightbfs
from DataApp.model.s_plat_fightlog import s_plat_fightlog
from DataApp.model.s_data_numbyday import s_data_numbyday
from DataApp.model.s_data_numbyweek import s_data_numbyweek
from DataApp.model.s_data_numbyhour import s_data_numbyhour
from DataApp.model.s_data_usergeo import s_data_usergeo
from DataApp.model.s_data_admin import s_data_admin
from DataApp import app,db
from flask import render_template,redirect,url_for,request,session,flash
from sqlalchemy import func,funcfilter
from datetime import datetime
from innerFunctions import periodAnalyse,refreshLocalDbDay,refreshLocalDbWeek,refreshLocalDbHour,refreshLocalUserGeo,ipToGeo
import time,math


@app.route('/')
def show_index():
    refreshLocalDbDay()
    myData = s_data_numbyday.query.filter(s_data_numbyday.usertolnum > 0).order_by(db.desc(s_data_numbyday.time)).all()

    now = time.time()
    todayUser = s_plat_user.query.filter(s_plat_user.regTime>myData[0].time).filter(s_plat_user.regTime < now).count()
    todayGame = s_plat_fightlog.query.filter(s_plat_fightlog.logTime >myData[0].time).filter(s_plat_fightlog.logTime < now).count()

    gdusers = s_plat_user.query.all()
    gsusers = s_plat_user.query.filter(s_plat_user.wxid.like("player_%")).all()

    tol_user = len(gdusers)
    tol_guest = len(gsusers)
    tol_wechat = tol_user - tol_guest
    gdgames = s_plat_fightlog.query.all()
    tol_game = len(gdgames)
    return render_template('index.html',tol_user = tol_user,tol_wechat = tol_wechat, tol_guest = tol_guest , tol_game = tol_game,todayUser = todayUser,todayGame=todayGame,datas = myData[0:4] )

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        user = s_data_admin.query.filter_by(username=request.form['username']).first()
        passwd = s_data_admin.query.filter_by(password=request.form['password']).first()

        if user is None:
            error = u'用户名错误！'
        elif passwd is None:
            error = u'密码错误！'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash(u'登录成功！')
            return redirect(url_for('show_index'))
    return render_template('index.html',error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash(u'登出成功！')
    return redirect(url_for('show_index'))

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
    refreshLocalDbDay()
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
    refreshLocalDbDay()
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
    refreshLocalDbDay()
    myData = s_data_numbyday.query.filter(s_data_numbyday.usertolnum > 0).all()
    return render_template('userDiagram.html', datas=myData)


@app.route('/gameDiagram')
def gameDiagram():
    refreshLocalDbDay()
    myData = s_data_numbyday.query.filter(s_data_numbyday.usertolnum > 0).all()
    return render_template('gameDiagram.html',datas = myData)


@app.route('/userDiagramByWeek')
def userDiagramByWeek():
    refreshLocalDbWeek()
    myData = s_data_numbyweek.query.filter(s_data_numbyweek.usertolnum > 0).all()
    return render_template('userDiagramByWeek.html', datas=myData)

@app.route('/gameDiagramByWeek')
def gameDiagramByWeek():
    refreshLocalDbWeek()
    myData = s_data_numbyweek.query.filter(s_data_numbyweek.usertolnum > 0).all()
    return render_template('gameDiagramByWeek.html',datas = myData)

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
    refreshLocalDbHour()
    myData = s_data_numbyhour.query.filter(s_data_numbyhour.hour < 25).filter(s_data_numbyhour.hour == order).all()
    return render_template('periodAnalyseByDay.html', datas=myData,order = order)

@app.route('/periodAnalyseByDayTotal')
def periodAnalyseByDayTotal():
    firstDay = time.mktime(datetime(2017, 9, 9, 0, 0, 0).timetuple())
    myData = []
    for order in range(24):
        users = s_plat_user.query.filter(((s_plat_user.regTime - firstDay) / 3600.0) % 24 > order).filter(
            ((s_plat_user.regTime - firstDay) / 3600.0) % 24 < order+1).all()
        games = s_plat_fightlog.query.filter(((s_plat_fightlog.logTime - firstDay) / 3600.0) % 24 > order).filter(
            ((s_plat_fightlog.logTime - firstDay) / 3600.0) % 24 < order+1).all()
        myData.append([order,len(users),len(games)])
    return render_template('periodAnalyseByDayTotal.html',datas=myData)

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
    firstDay = time.mktime(datetime(2017, 9, 9, 0, 0, 0).timetuple())
    myData = []
    for order in range(7):
        users = s_plat_user.query.filter(((s_plat_user.regTime - firstDay) / (24*3600.0)) % 7 > order).filter(
            ((s_plat_user.regTime - firstDay) / (24*3600.0)) % 7 < order+1).all()
        games = s_plat_fightlog.query.filter(((s_plat_fightlog.logTime - firstDay) / (24*3600.0)) % 7 > order).filter(
            ((s_plat_fightlog.logTime - firstDay) / (24*3600.0)) % 7 < order+1).all()
        myData.append([order,len(users),len(games)])
    return render_template('periodAnalyseByWeekTotal.html',datas=myData)

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

@app.route('/userListByGeo')
def userListByGeo():
    return redirect(url_for('userListByGeoPage', page=1))
@app.route('/userListByGeo/<int:page>')
def userListByGeoPage(page):
    refreshLocalUserGeo()
    myData = s_data_usergeo.query.order_by(db.desc(s_data_usergeo.game)).all()
    tol_item = len(myData)
    tol_page = int(math.ceil(tol_item / 20.0))
    cur_page = page
    return render_template('userListByGeo.html', users=myData[20*page-20:20*page], cur_page = cur_page, tol_page = tol_page, tol_user = tol_item )

@app.route('/userMapByProvince')
def userMapByProvince():
    transProvince ={
        u"北京市": u'北京',
        u"天津市": u'天津',
        u"上海市": u'上海',
        u"重庆市": u'重庆',
        u'河北省': u'河北',
        u'河南省': u'河南',
        u'云南省': u'云南',
        u'辽宁省': u'辽宁',
        u'黑龙江省': u'黑龙江',
        u'湖南省': u'湖南',
        u'安徽省': u'安徽',
        u'山东省': u'山东',
        u'新疆维吾尔自治区': u'新疆',
        u'江苏省': u'江苏',
        u'浙江省': u'浙江',
        u'江西省': u'江西',
        u'湖北省': u'湖北',
        u'广西壮族自治区': u'广西',
        u'甘肃省': u'甘肃',
        u'山西省': u'山西',
        u'内蒙古自治区': u'内蒙古',
        u'陕西省': u'陕西',
        u'吉林省': u'吉林',
        u'福建省': u'福建',
        u'贵州省': u'贵州',
        u'广东省': u'广东',
        u'青海省': u'青海',
        u'西藏自治区': u'西藏',
        u'四川省': u'四川',
        u'宁夏回族自治区': u'宁夏',
        u'海南省': u'海南',
        u'台湾省': u'台湾',
        u'香港特别行政区': u'香港',
        u'澳门特别行政区': u'澳门'
    }
    refreshLocalUserGeo()
    myData = []
    for i in range(3):
        dbdatas = db.session.query(s_data_usergeo.province,func.count(s_data_usergeo.province)).group_by(
        s_data_usergeo.province).distinct().filter(s_data_usergeo.wxsex == i+1).all()
        dataItem = []
        for dbdata in dbdatas:
            if dbdata.province in transProvince.keys():
                dataItem.append([transProvince[dbdata.province],dbdata[1]])
        myData.append(dataItem)
    return render_template('userMapByProvince.html',datas = myData)

@app.route('/userMapByCity')
def userMapByCity():
    refreshLocalUserGeo()
    posGeo = db.session.query(s_data_usergeo.city,s_data_usergeo.pos_x, s_data_usergeo.pos_y).group_by(s_data_usergeo.city).distinct().all()
    maleGeo = db.session.query(s_data_usergeo.city, func.count(s_data_usergeo.city)).group_by(s_data_usergeo.city).distinct().filter(s_data_usergeo.wxsex == 1).all()
    femaleGeo = db.session.query(s_data_usergeo.city, func.count(s_data_usergeo.city)).group_by(s_data_usergeo.city).distinct().filter(s_data_usergeo.wxsex == 2).all()
    guestGeo = db.session.query(s_data_usergeo.city, func.count(s_data_usergeo.city)).group_by(s_data_usergeo.city).distinct().filter(s_data_usergeo.wxsex == 3).all()
    totalGeo = db.session.query(s_data_usergeo.city,func.count(s_data_usergeo.city)).group_by(s_data_usergeo.city).distinct().all()
    return render_template('userMapByCity.html', posGeos = posGeo,maleGeos=maleGeo,femaleGeos=femaleGeo,guestGeos=guestGeo,totalGeos=totalGeo)