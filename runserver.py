#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 16:11
# @Author  : Panta Sun
# @Site    : -i https://linux.xidian.edu.cn/mirrors/pypi/web/simple/
# @File    : runserver.py
# @Software: PyCharm

from application import app



if __name__ == '__main__':
    app.run(debug=True)