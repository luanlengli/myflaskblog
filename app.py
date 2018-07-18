#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask

from routes.route_index import main as index_route


def register_routes(app):
    # 注册路由
    app.register_blueprint(index_route)
    return app

def configured_app():
    # 初始化app
    app = Flask(__name__)
    app = register_routes(app)
    return app




if __name__ == '__main__':
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=80,
    )
    app.run(**config)