#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import functools

from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
)

from routes.route_index import current_user, login_required
from models.blog import Blog
from models.blog_comment import BlogComment

main = Blueprint('blog', __name__)


def blog_ownner_required(func):
    '''
    判断blog属主
    :param func:
    :return:
    '''

    @functools.wraps(func)
    def f(*args, **kwargs):
        print('blog ownner required')
        print('args = <{}>'.format(args))
        print('kwargs = <{}>'.format(kwargs))
        u = current_user()
        if request.method == 'GET':
            blog_id = request.args.get('id')
        else:
            blog_id = request.form['id']
        blog = Blog.find_one(id=blog_id)
        print('blog = <{}>'.format(blog))
        if blog.user_id == u.id:
            return func(*args, **kwargs)
        else:
            return redirect('/blog/index')

    return f


def blog_comment_ownner_required(func):
    '''
    判断blog_comment属主
    :param func:
    :return:
    '''

    @functools.wraps(func)
    def f(*args, **kwargs):
        print('blog comment ownner required')
        print('args = <{}>'.format(args))
        print('kwargs = <{}>'.format(kwargs))
        u = current_user()
        if request.method == 'GET':
            bc_id = request.args.get('id')
        else:
            bc_id = request.form['id']
        bc = BlogComment.find_one(id=bc_id)
        print('blog comment = <{}>'.format(bc))
        if bc.user_id == u.id:
            return func(*args, **kwargs)
        else:
            return redirect('/blog/index')

    return f


@main.route('/blog')
@main.route('/blog/index')
def blog_index():
    blogs = Blog.find_all()
    return render_template('blog/blog_index.html', blogs=blogs)


@main.route('/blog/detail/<int:id>')
def blog_detail(id):
    blog = Blog.view(id=id)
    blog_comments = blog.comments()
    return render_template('blog/blog_detail.html', blog=blog, blog_comments=blog_comments)


@main.route('/blog/add', methods=['GET', 'POST'])
@login_required
def blog_add():
    form = request.form.to_dict()
    if request.method == 'POST':
        u = current_user()
        print('blog_add form = <{}>'.format(form))
        b = Blog.new(form=form, user_id=u.id)
        return redirect(url_for('.blog_index'))
    return render_template('blog/blog_add.html', form=form)


@main.route('/blog/edit')
@login_required
@blog_ownner_required
def blog_edit():
    blog_id = request.args.get('id')
    blog = Blog.find_one(id=int(blog_id))
    return render_template('blog/blog_edit.html', blog=blog)


@main.route('/blog/update', methods=['POST'])
@login_required
@blog_ownner_required
def blog_update():
    form = request.form.to_dict()
    blog_id = int(form['id'])
    print('blog_update form = <{}>'.format(form))
    blog = Blog.update(_id=blog_id, **form)
    return redirect('/blog/detail/{}'.format(blog_id))


@main.route('/blog/delete', methods=['GET'])
@login_required
@blog_ownner_required
def blog_delete():
    blog_id = request.args.get('id')
    blog = Blog.find_one(id=blog_id)
    blog.delete()
    return redirect('/blog/index')


@main.route('/blog_comment/add', methods=['POST'])
@login_required
def blog_comment_add():
    form = request.form.to_dict()
    u = current_user()
    print('blog_add form = <{}>'.format(form))
    bc = BlogComment.new(form=form, user_id=u.id)
    return redirect('/blog/detail/{}'.format(form['blog_id']))


@main.route('/blog_comment/edit', methods=['GET'])
@login_required
@blog_comment_ownner_required
def blog_comment_edit():
    bc_id = request.args.get('id')
    bc = BlogComment.find_one(id=bc_id)
    return render_template('blog/blog_comment_edit.html', bc=bc)


@main.route('/blog_comment/update', methods=['POST'])
@login_required
@blog_comment_ownner_required
def blog_comment_update():
    form = request.form.to_dict()
    bc_id = int(form['id'])
    print('blog_comment_update form = <{}>'.format(form))
    bc = BlogComment.update(_id=bc_id, **form)
    return redirect('/blog/detail/{}'.format(form['blog_id']))


@main.route('/blog_comment/delete', methods=['GET'])
@login_required
@blog_comment_ownner_required
def blog_comment_get():
    bc_id = int(request.args.get('id'))
    bc = BlogComment.find_one(id=bc_id)
    blog_id = bc.blog_id
    BlogComment.delete_one(id=bc.id)
    return redirect('/blog/detail/{}'.format(blog_id))
