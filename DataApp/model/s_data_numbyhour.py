# -*- coding: utf-8 -*-
from DataApp import db

class s_data_numbyhour(db.Model):
    __bind_key__ = 'localdb'
    __tablename__ = 's_data_numbyhour'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    time = db.Column(db.Numeric)
    hour = db.Column(db.Integer)
    usernum = db.Column(db.Integer)
    usertolnum = db.Column(db.Integer)
    gamenum = db.Column(db.Integer)
    gametolnum = db.Column(db.Integer)



    def __init__(self, time,hour,usernum,usertolnum,gamenum,gametolnum):
        self.time = time
        self.hour = hour
        self.usernum = usernum
        self.usertolnum = usertolnum
        self.gamenum = gamenum
        self.gametolnum = gametolnum

    def __repr__(self):
        return '<s_data_numbyhour %r>' % self.id