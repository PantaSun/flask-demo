#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 15:35
# @Author  : Panta Sun
# @Site    : -i https://linux.xidian.edu.cn/mirrors/pypi/web/simple/
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')
db = SQLAlchemy(app)

from application import views, models