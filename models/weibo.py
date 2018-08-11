#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from sqlalchemy import (
    Column,
    Integer,
    UnicodeText,
)
import time
from models.base_model import (
    BaseModel,
    db
)
from models.user import User
from models.weibo_comment import WeiboComment


class Weibo(BaseModel, db.Model):
    __tablename__ = 'Weibo'
    content = Column(
        UnicodeText,
        nullable=False,
    )
    user_id = Column(
        Integer,
        nullable=False,
    )

    def ownner(self):
        u = User.find_one(id=self.user_id)
        return u

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        m = super().add(form)
        return m

    @classmethod
    def update(cls, **kwargs):
        super().update(
            id=kwargs['id'],
            content=kwargs['content'],
            updated_time=int(time.time()),
        )
        m = Weibo.find_one(id=kwargs['id'])
        return m

    def comments(self):
        cs = WeiboComment.find_all(blog_id=self.id)
        return cs

    def comment_count(self):
        count = len(self.comments())
        return count

    # 删Weibo的时候，同时删除Weibo下的所有评论
    def delete(self):
        wcs = WeiboComment.find_all(weibo_id=self.id)
        for wc in wcs:
            wc.delete_one(id=wc.id)
        self.delete_one(id=self.id)
        return 'Delete Success!'

    # 将对象转换成字典形式
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
        }

    # 获取所有Weibo json格式数据并拼接成列表返回
    @classmethod
    def all_json(cls, **kwargs):
        ms = cls.find_all()
        js = [m.to_json() for m in ms]
        return js

    def get_username(self):
        u = User.find_one(id=self.user_id)
        return u.username