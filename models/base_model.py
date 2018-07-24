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
import uuid

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

    @classmethod
    def add(cls, form):
        m = cls()
        for k, v in form.items():
            setattr(m, k, v)
        db.session.add(m)
        db.session.commit()
        return m

    @classmethod
    def find_one(cls, **kwargs):
        m = cls.query.filter_by(**kwargs).first()
        return m

    @classmethod
    def find_all(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    @classmethod
    def delete_one(cls, id):
        m = cls.query.filter_by(id=id).delete()
        return m

    @classmethod
    def update(cls, id, **kwargs):
        m = cls.query.filter_by(id=id).first()
        for k, v in kwargs.items():
            setattr(m, k, v)
        db.session.add(m)
        db.session.commit()

    @classmethod
    def columns(cls):
        return cls.__mapper__.c.items()

    def __repr__(self):
        name = self.__class__.__name__
        s = ''
        for k, v in self.columns():
            if hasattr(self, k):
                v = getattr(self, k)
                s += '{}: ({})\n'.format(k, v)
        return '{}: ({})\n'.format(k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()
