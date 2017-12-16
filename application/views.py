#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 16:13
# @Author  : Panta Sun
# @Site    : -i https://linux.xidian.edu.cn/mirrors/pypi/web/simple/
# @File    : views.py
# @Software: PyCharm
from application import app, db
from flask import render_template, redirect, request, flash, get_flashed_messages
from models import Image, User
from flask_login import login_required, login_user, logout_user, current_user
import random
import hashlib
import json


def redirect_with_msg(target, msg, category):
    if msg is not None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/')
def index():
    images = Image.query.order_by('id desc').limit(10).all()
    return render_template('index.html', images=images)


@app.route('/image/<int:image_id>/')
def image(image_id):
    img = Image.query.get(image_id)
    if img is None:
        return redirect('/')

    return render_template('pageDetail.html', image=img)


@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')

    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1, per_page=3, error_out=False)
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next)


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    maps = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        imgvo = {'id': image.id, 'url': image.url, 'comment_count': len(image.comments)}
        images.append(imgvo)
    maps['images'] = images
    return json.dumps(maps)


@app.route('/regloginpage/')
def regloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    return render_template('login.html', msg=msg, next=request.values.get('next'))


@app.route('/reg/', methods=['post'])
def reg():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage/', u'用户名或密码为空', 'reglogin')
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return redirect_with_msg('/regloginpage/', u'用户名已存在', 'reglogin')

    salt = '.'.join(random.sample('0123456789abcdeABCDE', 10))
    m = hashlib.md5()
    m.update(password+salt)
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    next_url = request.values.get('next')
    if next_url is not None and next_url.startswith('/'):
        return redirect(next_url)
    return redirect('/')


@app.route('/login/', methods=['post'])
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage/', u'用户名或密码为空', 'reglogin')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect_with_msg('/regloginpage/', u'用户名不存在', 'reglogin')

    m = hashlib.md5()
    m.update(password + user.salt)
    if user.password != m.hexdigest():
        return redirect_with_msg('/regloginpage/', u'密码错误', 'reglogin')
    login_user(user)
    next_url = request.values.get('next')
    if next_url is not None and next_url.startswith('/'):
        return redirect(next_url)
    return redirect('/')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')