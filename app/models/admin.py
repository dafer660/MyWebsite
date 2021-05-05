from flask import request, redirect, url_for, abort, flash
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from config import Config


class AdminMixin:

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin'))

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                msg, cat = Config.SECURITY_MSG_LOGIN
                flash(msg, cat)
                return redirect(url_for('auth.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class AdminUserView(AdminMixin, ModelView):
    form_columns = ['roles', 'email', 'password', 'about_me', ]


class AdminPostView(AdminMixin, ModelView):
    form_columns = ['author_id', 'tags', 'title', 'description', 'body', ]


class AdminTagView(AdminMixin, ModelView):
    form_columns = ['name', 'description', ]


class AdminRoleView(AdminMixin, ModelView):
    form_columns = ['name', 'description', ]


