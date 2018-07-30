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


class BlogComment(BaseModel, db.Model):
    __tablename__ = 'BlogComment'
    content = Column(
        UnicodeText,
        nullable=False,
    )
    user_id = Column(
        Integer,
        nullable=False,
    )
    blog_id = Column(
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
