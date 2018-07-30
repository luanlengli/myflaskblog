#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    UnicodeText,
)
import time
from models.base_model import (
    BaseModel,
    db
)
from models.user import User
from models.blog_comment import BlogComment


class Blog(BaseModel, db.Model):
    __tablename__ = 'Blog'
    title = Column(
        String(50),
        nullable=False,
    )
    content = Column(
        UnicodeText,
        nullable=False,
    )
    user_id = Column(
        Integer,
        nullable=False,
    )
    views = Column(
        Integer,
        nullable=False,
        default=0,
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
    def view(cls, id):
        m = cls.find_one(id=id)
        m.views += 1
        m.save()
        return m

    @classmethod
    def update(cls, _id, **kwargs):
        super().update(
            id=_id,
            title=kwargs['title'],
            content=kwargs['content'],
            updated_time=int(time.time()),
        )
        m = Blog.find_one(id=_id)
        return m

    def comments(self):
        cs = BlogComment.find_all(blog_id=self.id)
        return cs

    def comment_count(self):
        count = len(self.comments())
        return count

    # 删blog的时候，同时删除blog下的所有评论
    def delete(self):
        bcs = BlogComment.find_all(blog_id=self.id)
        for bc in bcs:
            bc.delete_one(id=bc.id)
        self.delete_one(id=self.id)
        return 'Delete Success!'
