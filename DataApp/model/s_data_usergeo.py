# -*- coding: utf-8 -*-
from DataApp import db

class s_data_usergeo(db.Model):
    __bind_key__ = 'localdb'
    __tablename__ = 's_data_usergeo'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userid = db.Column(db.Integer)
    ip = db.Column(db.String(32))
    city_code = db.Column(db.Integer)
    province = db.Column(db.String(32))
    city = db.Column(db.String(32))
    pos_x = db.Column(db.Float)
    pos_y = db.Column(db.Float)
    iswx = db.Column(db.Integer)
    wxsex = db.Column(db.Integer)
    game = db.Column(db.Integer)
    name = db.Column(db.String(32))



    def __init__(self,userid,ip="",city_code = 0,province = "",city = "",pos_x = 0,pos_y = 0,iswx = 0,wxsex = 0,game = 0,name = ""):
        self.userid = userid
        self.ip = ip
        self.city_code = city_code
        self.province = province
        self.city = city
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.iswx = iswx
        self.wxsex = wxsex
        self.game = game
        self.name = name

    def __repr__(self):
        return '<s_data_usergeo %r>' % self.id