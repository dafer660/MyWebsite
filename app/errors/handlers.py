from flask import render_template, request, url_for
from flask_mail import Message

from app import db, mail
from app.errors import bp


def redirect_url(default='main.index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@bp.errorhandler(400)
def bad_request(error):
    previous = redirect_url()
    return render_template('errors/400.html', previous=previous), 400


@bp.errorhandler(403)
def permission_denied(error):
    previous = redirect_url()
    return render_template('errors/403.html', previous=previous), 403


@bp.errorhandler(404)
def not_found_error(error):
    previous = redirect_url()
    return render_template('errors/404.html', previous=previous), 404


@bp.errorhandler(500)
def internal_error(error):
    # this will clean the db session before the error
    db.session.rollback()
    # also, send admin an email
    message = Message()
    previous = redirect_url()
    return render_template('errors/500.html', previous=previous), 500
