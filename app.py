#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask

from routes.route_index import main as index_route
from routes.route_blog import main as blog_route
from routes.route_weibo import main as weibo_route
from routes.route_webchat import main as webchat_route
from routes.route_webchat import socketio
from secret import Config
from models.base_model import db


def register_routes(app):
    # 注册路由
    app.register_blueprint(index_route)
    app.register_blueprint(blog_route)
    app.register_blueprint(weibo_route)
    app.register_blueprint(webchat_route)

    socketio.init_app(app)
    return app


def configured_app():
    # 初始化app
    app = Flask(__name__)
    app.secret_key = Config.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.db_uri
    app.debug = True
    db.init_app(app)
    app = register_routes(app)
    return app


if __name__ == '__main__':
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=80,
    )
    socketio.run(app, host='0.0.0.0', port=80)
