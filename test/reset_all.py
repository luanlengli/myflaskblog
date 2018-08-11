#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from secret import Config
from app import configured_app
from models.base_model import db
from models.user import User
from models.blog import Blog
from models.blog_comment import BlogComment
from models.weibo import Weibo
from models.weibo_comment import WeiboComment


def reset_database():
    # 导入models目录的类
    # 重建数据库和相应的表
    e = create_engine(Config.db_uri, echo=True)
    with e.connect() as c:
        c.execute("DROP DATABASE IF EXISTS {}".format(Config.db_name))
        c.execute('CREATE DATABASE {} CHARACTER SET {} COLLATE utf8mb4_unicode_ci'.format(
            Config.db_name,
            Config.db_charset,
        ))
        c.execute('USE {}'.format(Config.db_name))

    db.metadata.create_all(bind=e)


def generate_fake_data():
    # 生成示例表单
    # 调用类方法将数据插入数据库
    user_form1 = dict(
        username='admin',
        password='abc@123',
        email='admin@example.com',
    )
    user_form2 = dict(
        username='guest',
        password='abc@123',
        email='guest@example.com',
    )
    with open('markdown_demo.md', encoding='utf8') as f:
        md_content = f.read()
    blog_form1 = dict(
        title='New Blog',
        content='Hello World!',
    )
    markdown_blog_form = dict(
        title='Markdown样例',
        content=md_content,
    )
    blog_comment_form1 = dict(
        content='commment 1',
        user_id=1,
        blog_id=1,
    )
    blog_comment_form2 = dict(
        content=md_content,
        user_id=1,
        blog_id=1,
    )
    weibo_form1 = dict(
        content='微博1测试1',
    )
    weibo_form2 = dict(
        content='weibo test 2',
    )
    weibo_comment_form1 = dict(
        content='weibo 1 comment 1',
        weibo_id=1,
    )
    weibo_comment_form2 = dict(
        content='微博1测试2',
        weibo_id=1,
    )
    weibo_comment_form3 = dict(
        content='guest评论',
        weibo_id=2,
    )
    u1 = User.register(user_form1)
    print('u1=<{}>'.format(u1))
    u2 = User.register(user_form2)
    print('u2=<{}>'.format(u2))
    b = Blog.new(form=blog_form1, user_id=1)
    print('b=<{}>'.format(b))
    bc1 = BlogComment.new(form=blog_comment_form1, user_id=1)
    print('bc1=<{}>'.format(bc1))
    bc2 = BlogComment.new(form=blog_comment_form2, user_id=1)
    print('bc2=<{}>'.format(bc2))
    mb = Blog.new(form=markdown_blog_form, user_id=1)
    print('mb=<{}>'.format(mb))
    w1 = Weibo.new(form=weibo_form1, user_id=1)
    print('w1=<{}>'.format(w1))
    w2 = Weibo.new(form=weibo_form2, user_id=1)
    print('w1=<{}>'.format(w2))
    wc1 = WeiboComment.new(form=weibo_comment_form1, user_id=1)
    print('wc1=<{}>'.format(wc1))
    wc2 = WeiboComment.new(form=weibo_comment_form2, user_id=1)
    print('wc1=<{}>'.format(wc2))
    wc3 = WeiboComment.new(form=weibo_comment_form3, user_id=2)
    print('wc1=<{}>'.format(wc3))


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_data()
