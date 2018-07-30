#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hashlib
from sqlalchemy import (
    Column,
    String,
)
from models.base_model import (
    BaseModel,
    db
)
from secret import Config


class User(BaseModel, db.Model):
    __tablename__ = 'User'
    username = Column(
        String(25),
        nullable=False,
    )
    password = Column(
        String(128),
        nullable=False,
    )
    email = Column(
        String(50),
        nullable=False,
    )
    image = Column(
        String(200),
        nullable=False,
        default='https://www.baidu.com/favicon.ico',
    )
    signature = Column(
        String(280),
        nullable=False,
        default='这个人很懒，什么也没有留下',
    )

    @staticmethod
    def salted_password(password, salt=Config.salt):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        if (len(name) > 2) and (User.find_one(username=name) is None):
            form['password'] = User.salted_password(form['password'])
            print('User Register Form = {}'.format(form))
            u = User.add(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        return User.find_one(**query)

