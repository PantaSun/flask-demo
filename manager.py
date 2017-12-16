#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 15:24
# @Author  : Panta Sun
# @Site    : -i https://linux.xidian.edu.cn/mirrors/pypi/web/simple/
# @File    : manager.py
# @Software: PyCharm
from flask_script import Manager
from application import app, db
from application.models import User, Image, Comment
from random import randint
manager = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(randint(0, 1000)) + 'm.png'


@manager.command
def hello(name):
    print "hello", name


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in xrange(100):
        db.session.add(User('User'+str(i+1), 'password'+str(i)))
        for j in xrange(10):
            db.session.add(Image(get_image_url(), i+1))
            for k in xrange(3):
                db.session.add(Comment("This is a comment"+str(k+1), 1+10*i+j, i+1))
    db.session.commit()

    image = Image.query.get(3)
    print image.user

if __name__ == "__main__":
    manager.run()