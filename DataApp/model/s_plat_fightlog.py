# -*- coding: utf-8 -*-
from DataApp import db

class s_plat_fightlog(db.Model):
    __tablename__ = 's_plat_fightlog'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    roomId = db.Column(db.Integer)
    roomCfg = db.Column(db.String(255))
    logTime = db.Column(db.Numeric(13,0))
    isHaoren = db.Column(db.Integer)
    u1 = db.Column(db.Integer)
    u2 = db.Column(db.Integer)
    u3 = db.Column(db.Integer)
    u4 = db.Column(db.Integer)
    u5 = db.Column(db.Integer)
    u6 = db.Column(db.Integer)
    u7 = db.Column(db.Integer)
    u8 = db.Column(db.Integer)
    c1 = db.Column(db.Integer)
    c2 = db.Column(db.Integer)
    c3 = db.Column(db.Integer)
    c4 = db.Column(db.Integer)
    c5 = db.Column(db.Integer)
    c6 = db.Column(db.Integer)
    c7 = db.Column(db.Integer)
    c8 = db.Column(db.Integer)
    n1 = db.Column(db.Integer)
    n2 = db.Column(db.Integer)
    n3 = db.Column(db.Integer)
    n4 = db.Column(db.Integer)
    n5 = db.Column(db.Integer)
    n6 = db.Column(db.Integer)
    n7 = db.Column(db.Integer)
    n8 = db.Column(db.Integer)



    def __init__(self, id, roomId,roomCfg,logTime,isHaoren,u1,u2,u3,u4,u5,u6,u7,u8,c1,c2,c3,c4,c5,c6,c7,c8,n1,n2,n3,n4,n5,n6,n7,n8):
        self.id = id
        self.roomId = roomId
        self.roomCfg = roomCfg
        self.logTime = logTime
        self.isHaoren = isHaoren
        self.u1 = u1
        self.u2 = u2
        self.u3 = u3
        self.u4 = u4
        self.u5 = u5
        self.u6 = u6
        self.u7 = u7
        self.u8 = u8
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.c5 = c5
        self.c6 = c6
        self.c7 = c7
        self.c8 = c8
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        self.n5 = n5
        self.n6 = n6
        self.n7 = n7
        self.n8 = n8


    def __repr__(self):
        return '<s_plat_fightlog %r>' % self.id