#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import cgitb
import os
cgitb.enable()

os.environ['FLASK_SECRET_KEY'] = "a9N6Hd5zLVQ3sT8gjKr2XycDWe1AmEPF"
os.environ['FLASK_ENV'] = "production"

os.environ['SMTP_SERVER'] = "mipo.sakura.ne.jp"
os.environ['SMTP_PORT'] = '587'
os.environ['SMTP_USER']="info@mipo.sakura.ne.jp"


os.environ['SMTP_PASSWORD'] = "5yw6da98"
os.environ['MAIL_FROM'] = "info@mipo.co.jp"
os.environ['MAIL_TO'] = "y.nakamura@digital-city.jp"

from wsgiref.handlers import CGIHandler
from app import app
from sys import path

class ProxyFix(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CGIHandler().run(app)
