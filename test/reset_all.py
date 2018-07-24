#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from secret import Config
from app import configured_app
from models.base_model import db
from models.user import User


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
    u = User.register(user_form)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_data()
