# -*- coding: utf-8 -*-
from DataApp.model.s_plat_user import s_plat_user
from DataApp.model.s_plat_fightbfs import s_plat_fightbfs
from DataApp.model.s_plat_fightlog import s_plat_fightlog
from DataApp import app
from flask import render_template,redirect,url_for
from datetime import datetime
import time

@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/gameList')
def gameList():
    gdgames = s_plat_fightlog.query.all()
    return render_template('gameList.html',games = gdgames[0:100])
@app.route('/userList')
def userList():
    return redirect(url_for('userListPage',page=1))

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
    time.localtime()
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
    time.localtime()
    return render_template('gameDiagram.html',datas = myData)

@app.route('/userList/<int:page>')
def userListPage(page):
    gdusers = s_plat_user.query.join(s_plat_fightbfs).all()
    return render_template('userList.html', users=gdusers[10*page-10:10*page])

@app.route('/1')
def test1():
    gdusers = s_plat_user.query.join(s_plat_fightbfs).all()
    return render_template('test1.html',users = gdusers[0:100])

@app.route('/1/<int:page>')
def test(page):
    gdusers = s_plat_user.query.filter(s_plat_user.id <= 100200).all()
    return render_template('test1.html',users = gdusers[page*10-10:page*10])

@app.route('/2')
def xuexi1():
    gduser = s_plat_user.query.first()
    return render_template('xuexi1.html',result_json = gduser)