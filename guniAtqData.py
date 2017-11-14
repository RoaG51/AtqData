# -*- coding: utf-8 -*-
from DataApp import app
from werkzeug.contrib.fixers import ProxyFix


app.wsgi_app = ProxyFix(app.wsgi_app)
    #nohup command & gunicorn -w 8 -b 0.0.0.0:8080 guniAtqData:app