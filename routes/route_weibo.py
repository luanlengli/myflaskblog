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
    jsonify,
)

from routes.route_index import current_user, login_required
from models.weibo import Weibo
from models.weibo_comment import WeiboComment
from models.user import User

main = Blueprint('weibo', __name__)


def weibo_ownner_required(func):
    '''
    判断Weibo属主
    :param func:
    :return:
    '''

    @functools.wraps(func)
    def f(*args, **kwargs):
        print('weibo ownner required')
        print('args = <{}>'.format(args))
        print('kwargs = <{}>'.format(kwargs))
        u = current_user()
        if request.method == 'GET':
            weibo_id = request.args.get('id')
        else:
            print('request form = <{}>'.format(request.get_json()))
            weibo_id = request.get_json()['id']
        weibo = Weibo.find_one(id=weibo_id)
        print('weibo = <{}>'.format(weibo))
        if weibo.user_id == u.id:
            return func(*args, **kwargs)
        else:
            return redirect('/weibo/index')

    return f


def weibo_comment_ownner_required(func):
    '''
    判断WeiboComment属主
    :param func:
    :return:
    '''

    @functools.wraps(func)
    def f(*args, **kwargs):
        print('weibo comment ownner required')
        print('args = <{}>'.format(args))
        print('kwargs = <{}>'.format(kwargs))
        u = current_user()
        if request.method == 'GET':
            wc_id = request.args.get('id')
        else:
            wc_id = request.get_json()['id']
        wc = WeiboComment.find_one(id=wc_id)
        print('weibo comment = <{}>'.format(wc))
        if wc.user_id == u.id:
            return func(*args, **kwargs)
        else:
            return redirect('/weibo/index')

    return f


@main.route('/weibo', methods=['GET'])
@main.route('/weibo/index', methods=['GET'])
def weibo_index():
    return render_template('weibo/weibo_index.html')


@main.route('/api/weibo/all')
def weibo_all():
    weibos = Weibo.all_json()
    print('weibo all json = <{}>'.format(weibos))
    for w in weibos:
        print('w=<{}>'.format(w))
        u = User.find_one(id=w['user_id'])
        w['username'] = u.username
    print('weibo all json add username = <{}>'.format(weibos))
    return jsonify(weibos)


@main.route('/api/weibo/add', methods=['POST'])
@login_required
def weibo_add():
    form = request.get_json()
    u = current_user()
    print('/api/weibo/add form = <{}>'.format(form))
    w = Weibo.new(form=form, user_id=u.id)
    w_json = w.to_json()
    print('weibo add w_json = <{}>'.format(w_json))
    w_json['username'] = w.get_username()
    return jsonify(w_json)


@main.route('/api/weibo/update', methods=['POST'])
@login_required
@weibo_ownner_required
def weibo_update():
    form = request.get_json()
    print('/api/weibo/update form = <{}>'.format(form))
    w = Weibo.update(**form)
    return jsonify(w.to_json())


@main.route('/api/weibo/delete', methods=['GET'])
@login_required
@weibo_ownner_required
def weibo_delete():
    weibo_id = int(request.args.get('id', -1))
    weibo = Weibo.find_one(id=weibo_id)
    weibo.delete()
    d = dict(
        message="成功删除Weibo和关联的WeiboComment！",
    )
    return jsonify(d)


@main.route('/api/weibo_comment/all', methods=['POST'])
def weibo_comment_all():
    form = request.get_json()
    print('/api/weibo_comment/all form = <{}>'.format(form))
    wcs = WeiboComment.all_json(weibo_id=int(form['weibo_id']))
    print('weibo comment all json = <{}>'.format(wcs))
    for wc in wcs:
        print('wc=<{}>'.format(wc))
        u = User.find_one(id=wc['user_id'])
        wc['username'] = u.username
    print('weibo comment all json add username = <{}>'.format(wcs))
    return jsonify(wcs)


@main.route('/api/weibo_comment/add', methods=['POST'])
@login_required
def weibo_comment_add():
    form = request.get_json()
    u = current_user()
    print('/api/weibo_comment/add form = <{}>'.format(form))
    wc = WeiboComment.new(form=form, user_id=u.id)
    wc_json = wc.to_json()
    print('weibo comment add w_json = <{}>'.format(wc_json))
    wc_json['username'] = wc.get_username()
    return jsonify(wc_json)


@main.route('/api/weibo_comment/update', methods=['POST'])
@login_required
@weibo_comment_ownner_required
def weibo_comment_update():
    form = request.get_json()
    print('/api/weibo_comment/update form = <{}>'.format(form))
    wc = WeiboComment.update(**form)
    return jsonify(wc.to_json())


@main.route('/api/weibo_comment/delete', methods=['GET'])
@login_required
@weibo_comment_ownner_required
def weibo_comment_delete():
    wc_id = int(request.args.get('id', -1))
    wc = Weibo.find_one(id=wc_id)
    wc.delete()
    d = dict(
        message="成功删除WeiboComment！",
    )
    return jsonify(d)
