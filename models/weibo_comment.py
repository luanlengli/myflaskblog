#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sqlalchemy import (
    Column,
    Integer,
    UnicodeText,
)
from models.base_model import (
    BaseModel,
    db
)
from models.user import User


class WeiboComment(BaseModel, db.Model):
    __tablename__ = 'WeiboComment'
    content = Column(
        UnicodeText,
        nullable=False,
    )
    user_id = Column(
        Integer,
        nullable=False,
    )
    weibo_id = Column(
        Integer,
        nullable=False
    )

    def ownner(self):
        u = User.find_one(id=self.user_id)
        return u

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        m = super().add(form)
        return m

    # 将对象转换成字典形式
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'weibo_id': self.weibo_id,
        }

    # 获取所有Weibo Comment json格式数据并拼接成列表返回
    @classmethod
    def all_json(cls, weibo_id):
        print('weibo comment all json weibo = <{}>'.format(weibo_id))
        ms = cls.find_all(weibo_id=weibo_id)
        js = [m.to_json() for m in ms]
        return js

    def get_username(self):
        u = User.find_one(id=self.user_id)
        return u.username