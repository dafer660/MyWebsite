import math
import os
import random
from datetime import datetime, timedelta

from uuid import uuid4

from flask import render_template, redirect, url_for, g, abort, request, flash
from flask_security import current_user, login_required, anonymous_user_required, logout_user
from flask_security.recoverable import generate_reset_password_token

from app.main import bp
from app.models.user import User
from app.models.posts import Post

from app.main.forms import EditProfileForm

from app import login_manager, Config, db


@login_manager.user_loader
def load_user(_id):
    return User.query.get(int(_id))


@bp.before_request
def get_current_user():
    g.user = current_user


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    post_uuid = uuid4().hex
    recent_posts = Post.query_posts_by_date().all()
    try:
        posts_count = len(recent_posts)
    except Exception as e:
        posts_count = int(recent_posts.count())

    if posts_count >= Config.INDEX_POST_LIMIT:
        recent_posts = recent_posts[-6:]

    _loops = math.ceil(round((posts_count/3), 0))

    # user = User.get_user_by_email(email=current_user.email)
    # user.has_role('admin')

    return render_template('index.html',
                           current_user=current_user,
                           post_uuid=post_uuid,
                           recent_posts=recent_posts,
                           posts_count=posts_count,
                           _loops=_loops,
                           current_date=datetime.utcnow())


@bp.route('/login-success')
@login_required
def login_success():
    msg, cat = ('Welcome to {}, {}. Enjoy your stay...!'.format(Config.SITE_NAME, current_user.email), 'success')
    flash(msg, cat)
    return render_template('auth/login-success.html', message=msg)


@bp.route('/register-success')
def register_success():
    msg, cat = ("Thank you for registering.\nYou will receive an email to confirm your account...", 'success')
    flash(msg, cat)
    return render_template('auth/register-success.html', message=msg)


@bp.route('/reset-success')
@anonymous_user_required
def reset_success():
    msg, cat = ("Your account's password has been successfully reset...!".format(current_user.email), 'success')
    return render_template('auth/reset-success.html', message=msg)


@bp.route('/confirmed-success')
@login_required
def confirmed_success():
    msg, cat = ("Your account '{}' has been confirmed...!".format(current_user.email), 'success')
    flash(msg, cat)
    return render_template('auth/confirmed-success.html', message=msg)


@bp.route('/account-updated')
@login_required
def account_updated():
    msg, cat = Config.SECURITY_MSG_PASSWORD_CHANGE
    flash(msg, cat)

    return render_template('auth/account-updated.html', message=msg)


@bp.route('/profile/<email>', methods=['GET', 'POST'])
@login_required
def user(email):
    user = User.get_user_by_email(email=email)
    posts_count = Post.count_posts_by_user(user.id)
    post_uuid = uuid4().hex

    if user is None:
        abort(404)

    return render_template('profile/profile.html', user=user, post_uuid=post_uuid, post_count=posts_count)


@bp.route('/profile/<email>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(email):
    user = User.get_user_by_email(email=email)
    post_uuid = uuid4().hex
    form = EditProfileForm()

    if user is None:
        abort(404)

    if form.change_pwd.data:
        return redirect(url_for('auth.change_password'))

    if request.method == 'POST':
        if form.submit_edit.data and form.submit_edit.validate(form=form.about_me):
            user.about_me = form.about_me.data
            db.session.commit()

            flash('Account details updated')
            return redirect(url_for('main.user', email=current_user.email))

    if request.method == 'GET':
        form.email.data = user.email
        form.about_me.data = user.about_me

    return render_template('profile/edit_profile.html', post_uuid=post_uuid, user=user, form=form)


@bp.route('/generate_pdf/<endpoint>')
@login_required
def generate_pdfs(endpoint):
    # create_pdf(endpoint=endpoint)
    # TODO
    pass


# @bp.route('/request/mdm_types')
# @login_required
# def mdm_types():
#     groups = AccessRequest.get_mdm_types()
#     return jsonify({'groups': groups})
