# -*- coding: utf-8 -*-
from DataApp import app

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run( )
