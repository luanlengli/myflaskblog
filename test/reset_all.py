#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from secret import Config
from app import configured_app
from models.base_model import db
from models.user import User
from models.blog import Blog
from models.blog_comment import BlogComment

def reset_database():
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
    user_form = dict(
        username='admin',
        password='abc@123',
        email='admin@example.com',
    )
    with open('markdown_demo.md', encoding='utf8') as f:
        md_content = f.read()
    blog_form1 = dict(
        title='New Blog',
        content='Hello World!',
    )
    markdown_blog_form = dict(
        title = 'Markdown样例',
        content = md_content,
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
    u = User.register(user_form)
    print('u=<{}>'.format(u))
    b = Blog.new(form=blog_form1, user_id=1)
    print('b=<{}>'.format(b))
    bc1 = BlogComment.new(form=blog_comment_form1, user_id=1)
    print('bc1=<{}>'.format(bc1))
    bc2 = BlogComment.new(form=blog_comment_form2, user_id=1)
    print('bc2=<{}>'.format(bc2))
    mb = Blog.new(form=markdown_blog_form, user_id=1)
    print('mb=<{}>'.format(mb))

if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_data()
