# _*_ coding: utf-8 _*_

#调试模式是否开启
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

#mysql数据库连接信息,这里改为自己的账号
SQLALCHEMY_DATABASE_URI = "mysql://user:password@ip:port/db"

SQLALCHEMY_BINDS = {
    'localdb':"mysql://user:password@localhost/db"
}