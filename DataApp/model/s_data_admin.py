# -*- coding: utf-8 -*-
from DataApp import db

class s_data_admin(db.Model):
    __bind_key__ = 'localdb'
    __tablename__ = 's_data_admin'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(16))


    def __init__(self,username,password):
        self.username  = username
        self.password = password

    def __repr__(self):
        return '<s_data_admin %r>' % self.id