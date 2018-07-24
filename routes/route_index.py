#!/usr/bin/env python3
# -*- coding:utf-8 -*-

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
from models.form import RegistrationForm
from models.user import User

main = Blueprint('index', __name__)


def current_user():
    uid = session.get('uid', '')
    u = User.find_one(id=uid)
    print('Curren_User = <{}>'.format(u.username))
    return u


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # print('Register Form = <{}>'.format(form))
        register_form = dict(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
        )
        u = User.register(register_form)
        flash('{}，你已注册成功！'.format(u.username), 'success')
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

            flash("{}，你已成功登录！".format(u.username), 'success')
            return redirect('dashboard')
    return render_template('login.html')


@main.route('/logout')
def logout():
    session.clear()
    flash("你已经成功退出登录", "success")
    return redirect(url_for('.login'))


@main.route('/dashboard')
def dashboard():
    user = current_user()
    return render_template('dashboard.html', u=user)
