# -*- coding: utf-8 -*-
from DataApp import db

class s_plat_fightbfs(db.Model):
    __tablename__ = 's_plat_fightbfs'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('s_plat_user.id'))
    wins = db.Column(db.Integer)
    losts = db.Column(db.Integer)
    bf = db.Column(db.Integer)


    def __init__(self, id, userId,wins,losts,bf):
        self.id = id
        self.userId = userId
        self.wins = wins
        self.losts = losts
        self.bf = bf


    def __repr__(self):
        return '<s_plat_fightbfs %r>' % self.id