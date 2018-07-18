#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import (
    Blueprint,
    render_template,
)

main = Blueprint('index', __name__)


@main.route('/')
@main.route('/index')
@main.route('/index.html')
def index():
    return render_template('index.html')