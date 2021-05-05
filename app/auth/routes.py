from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, g, jsonify, abort
from flask_security import SQLAlchemyUserDatastore, login_required, \
    login_user, logout_user, current_user, anonymous_user_required
from flask_security.confirmable import send_confirmation_instructions, \
    confirm_user
from flask_security.utils import verify_password, hash_password, \
    get_token_status


from werkzeug.urls import url_parse

from app.auth import bp
from app.models.roles import UserRoles, Role
from app.models.user import User
from app.auth.forms import LoginForm, RegistrationForm

from app import login_manager, db, basic_auth, security
from config import Config

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#
#
# @login_manager.user_loader
# def load_user(_id):
#     return User.query.get(int(_id))
#
#
# @bp.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_login = datetime.utcnow()
#
#         if not current_user.confirmed and request.endpoint[:5] != 'auth':
#             return redirect(url_for('auth.login'))
#
#         if not request.endpoint[:5] != 'auth':
#             return redirect(url_for('auth.login'))
#
#         db.session.commit()
#
#
# @bp.route('/login', methods=['GET', 'POST'])
# def login():
#     # if user is already authenticated, we prevent the user to login again
#     if current_user.is_authenticated:
#         flash('User {} is already authenticated'.format(current_user.username))
#         return redirect(url_for('main.index'))
#
#     # create the LoginForm and check if form is submitted correctly
#     form = LoginForm()
#
#     if request.method == 'POST' and form.validate_on_submit() and \
#             form.password.data != '':
#         user = User.get_user_by_email(email=form.email.data)
#
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('auth.login'))
#
#         if user.confirmed_at is None:
#             flash('You need to confirm your account in order to login')
#             return redirect(url_for('auth.login'))
#
#         login_user(user, remember=form.remember_me.data)
#         db.session.commit()
#         flash('You have been successfully logged in "{}"'.format(form.email.data))
#
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             return redirect(url_for('main.index'))
#         else:
#             return redirect(next_page)
#
#     print(request.values)
#
#     return render_template('auth/login.html', title="Login Page", form=form)

#
# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     form = RegistrationForm()
#
#     if request.method == 'POST' and form.validate_on_submit():
#         user = User.get_user_by_email(form.email.data)
#         if user is None:
#             new_user = user_datastore.create_user(email=form.email.data, password_hash=hash_password(form.password.data))
#             send_confirmation_instructions(new_user)
#         db.session.commit()
#         flash('Thank you for registering "{}"! Check your email and confirm your account to login'.format(form.email.data))
#
#         # login_user(user)
#         # this will logout the user so that it will not auto login after
#         # with this, it will enforce the user to login again after registration
#         # and be redirected properly to the login page
#         return redirect(url_for('auth.login'))
#
#     return render_template('auth/register.html', title="Register Page", form=form)

#
# @bp.route('/confirm/<token>')
# @login_required
# def confirm(token):
#     print(current_user)
#     print(current_user.is_anonymous)
#     print(token)
#     if current_user.confirmed_at is not None:
#         flash("'{}' you already confirmed your account.")
#         return redirect(url_for('main.index'))
#
#     exp, inv, data = get_token_status(
#         token=token,
#         serializer='confirm',
#         max_age="CONFIRM_EMAIL")
#
#     if inv:
#         flash('Token is invalid.')
#         return redirect(url_for('main.index'))
#
#     if exp:
#         flash('Sending out a new email confirmation.')
#         send_confirmation_instructions(current_user)
#         return redirect(url_for('auth.login'))
#
#     if data:
#         print(data)
#         confirm_user(current_user)
#         db.session.commit()
#         flash("Thank you for confirming your account '{}'".format(current_user.email))
#         return redirect(url_for('main.index'))
#
#     return render_template('index.html')
#
#
# @bp.route('/confirm-error')
# def confirm_error():
#     pass
#
#
# @bp.route('/confirmed')
# def confirmed():
#     token = g.user.generate_auth_token()
#     db.session.commit()
#     return jsonify({'token': token})
#
#
# @basic_auth.error_handler
# def basic_auth_error():
#     abort(404)
#
#
# @bp.route('/logout')
# @login_required
# def logout():
#     # logout the user and redirect to index page
#     logout_user()
#     flash('Logged out')
#
#     return redirect(url_for('main.index'))
