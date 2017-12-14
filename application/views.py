#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 16:13
# @Author  : Panta Sun
# @Site    : -i https://linux.xidian.edu.cn/mirrors/pypi/web/simple/
# @File    : views.py
# @Software: PyCharm
from application import app
from flask import render_template, redirect
from models import Image, User


@app.route('/')
def index():
    images = Image.query.order_by('id desc').limit(10).all()
    return render_template('index.html', images=images)


@app.route('/image/<int:image_id>')
def image(image_id):
    img = Image.query.get(image_id)
    if img is None:
        return redirect('/')

    return render_template('pageDetail.html', image=img)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    return render_template('profile.html', user=user)