#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
)
import time
from datetime import datetime

db = SQLAlchemy()


class BaseModel(object):
    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
        nullable=False,
    )
    created_time = Column(
        Integer,
        nullable=False,
        default=int(time.time())
    )
    updated_time = Column(
        Integer,
        nullable=False,
        default=int(time.time())
    )

    # 增
    @classmethod
    def add(cls, form):
        m = cls()
        for k, v in form.items():
            setattr(m, k, v)
        db.session.add(m)
        db.session.commit()
        return m

    # 查一个
    @classmethod
    def find_one(cls, **kwargs):
        m = cls.query.filter_by(**kwargs).first()
        return m

    # 查全部
    @classmethod
    def find_all(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    # 删
    @classmethod
    def delete_one(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()
        return True

    # 改
    @classmethod
    def update(cls, id, **kwargs):
        m = cls.query.filter_by(id=id).first()
        for k, v in kwargs.items():
            setattr(m, k, v)
        db.session.add(m)
        db.session.commit()
        return m

    @classmethod
    def columns(cls):
        return cls.__mapper__.c.items()

    # 修改魔法方法，使其能将所有属性打印出来
    def __repr__(self):
        name = self.__class__.__name__
        s = ''
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                s += '{}: ({})\n'.format(attr, v)
        return '< {}\n{} >\n'.format(name, s)

    # 将自己保存到数据库
    def save(self):
        db.session.add(self)
        db.session.commit()

    # 将timestamp转换成可读的时间
    def human_read_created_time(self):
        return datetime.fromtimestamp(self.created_time)

    def human_read_updated_time(self):
        return datetime.fromtimestamp(self.updated_time)
