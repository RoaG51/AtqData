# -*- coding: utf-8 -*-
from DataApp import db

class s_data_numbyweek(db.Model):
    __bind_key__ = 'localdb'
    __tablename__ = 's_data_numbyweek'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    time = db.Column(db.Numeric)
    usernum = db.Column(db.Integer)
    usertolnum = db.Column(db.Integer)
    gamenum = db.Column(db.Integer)
    gametolnum = db.Column(db.Integer)



    def __init__(self, time,usernum,usertolnum,gamenum,gametolnum):
        self.time = time
        self.usernum = usernum
        self.usertolnum = usertolnum
        self.gamenum = gamenum
        self.gametolnum = gametolnum

    def __repr__(self):
        return '<s_data_numbyweek %r>' % self.id