#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/13 22:55
# @Author  : Panta Sun
# @Site    : -i https://linux.xidian.edu.cn/mirrors/pypi/web/simple/
# @File    : testt.py
# @Software: PyCharm

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return "hello world"


@app.route('/profile/<int:uid>', methods=['GET', 'POST'])
def profile(uid):
    return render_template('profile.html', uid=uid)


if __name__ == "__main__":
    app.run(debug=True)
