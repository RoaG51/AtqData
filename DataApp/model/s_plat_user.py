# -*- coding: utf-8 -*-
from DataApp import db

class s_plat_user(db.Model):
    __tablename__ = 's_plat_user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    wxsex = db.Column(db.Integer)
    canTuiguang = db.Column(db.Integer)
    score = db.Column(db.String(32))
    iswx = db.Column(db.Integer)
    vipExp = db.Column(db.Integer)
    regIp = db.Column(db.String(20))
    regTime = db.Column(db.Numeric(13,0))
    wxtoken = db.Column(db.String(128))
    createBy = db.Column(db.Integer)
    tel = db.Column(db.String(16))
    vipLv = db.Column(db.Integer)
    webid = db.Column(db.String(20))
    isLock = db.Column(db.Integer)
    token = db.Column(db.String(32))
    money = db.Column(db.String(32))
    des = db.Column(db.String(255))
    wxhead = db.Column(db.String(255))
    name = db.Column(db.String(255))
    wxid = db.Column(db.String(128))
    bfs = db.relationship('s_plat_fightbfs', backref='user',
                                lazy='dynamic')



    def __init__(self, id, wxsex,canTuiguang,score,iswx,vipExp,regIp,regTime,wxtoken,createBy,tel,vipLv,webid,isLock,token,money,des,wxhead,name,wxid):
        self.id = id
        self.wxsex = wxsex
        self.canTuiguang = canTuiguang
        self.score = score
        self.iswx = iswx
        self.vipExp = vipExp
        self.regIp = regIp
        self.regTime = regTime
        self.wxtoken = wxtoken
        self.createBy = createBy
        self.tel = tel
        self.vipLv = vipLv
        self.webid = webid
        self.isLock = isLock
        self.token = token
        self.money = money
        self.des = des
        self.wxhead = wxhead
        self.name = name
        self.wxid = wxid

    def __repr__(self):
        return '<s_plat_user %r>' % self.id