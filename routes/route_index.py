#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import functools

from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    session,
)
from uuid import uuid4

from models.user import User

main = Blueprint('index', __name__)


def current_user():
    '''
    判断当前登录用户
    :return: 用户对象
    '''
    uid = session.get('uid', '')
    u = User.find_one(id=uid)
    print('Curren_User = <{}>'.format(u.username))
    return u


def login_required(func):
    '''
    判断用户登录
    :param func:
    :return:
    '''

    @functools.wraps(func)
    def f(*args, **kwargs):
        print('login required')
        login = session.get('login', False)
        if login is True:
            print('Logined!')
            return func(*args, **kwargs)
        else:
            print('No login!')
            return redirect(url_for('index.login'))

    return f


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = request.form.to_dict()
    if request.method == 'POST':
        # print('Register Form = <{}>'.format(form))
        u = User.register(form)
        # flash('{}，你已注册成功！'.format(u.username), 'success')
        return redirect(url_for('.index'))
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form.to_dict()
        # print('Route Login Form = <{}>'.format(form))
        u = User.validate_login(form)
        if u is None:
            error = "你输入的用户名和密码有误！"
            return render_template('login.html', error=error)
        else:
            session['username'] = u.username
            session['uid'] = u.id
            session['login'] = True
            # flash("{}，你已成功登录！".format(u.username), 'success')
            return redirect('dashboard')
    return render_template('login.html')


@main.route('/logout')
def logout():
    session.clear()
    flash("你已经成功退出登录", "success")
    return redirect(url_for('.login'))


@main.route('/dashboard')
@login_required
def dashboard():
    user = current_user()
    return render_template('dashboard.html', u=user)
