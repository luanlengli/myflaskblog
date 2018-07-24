#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from wtforms import (
    TextField,
    StringField,
    PasswordField,
    Form,
    TextAreaField,
    validators,
    BooleanField,
)


class RegistrationForm(Form):
    username = StringField('用户名', [validators.Length(min=4, max=25)])
    email = StringField('电子邮箱', [validators.Length(min=6, max=50)])
    password = PasswordField('密码', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='密码不匹配')
    ])
    confirm = PasswordField('请再次输入密码')

    def __repr__(self):
        form = dict(
            username=self.username.data,
            email=self.email.data,
            password=self.password.data,
        )
        s = ''
        for k, v in form.items():
            s += '{} = {} \n'.format(k, v)
        return s
