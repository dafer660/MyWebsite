from datetime import datetime

from flask import Flask

from flask_security import Security, SQLAlchemyUserDatastore, \
    AnonymousUser
from flask_security.utils import hash_password
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_httpauth import HTTPBasicAuth
from flask_ldap3_login import LDAP3LoginManager
from flask_assets import Bundle, Environment
from flask_wtf import CSRFProtect
from flask_simplemde import SimpleMDE
from flask_dropzone import Dropzone
from flask_babel import Babel

from app.models.admin import AdminView, HomeAdminView, AdminUserView, \
    AdminPostView, AdminRoleView, AdminTagView
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
ldap3_login_manager = LDAP3LoginManager()
mail = Mail()
basic_auth = HTTPBasicAuth()
assets = Environment()
csrf = CSRFProtect()
security = Security()
simplemde = SimpleMDE()
dropzone = Dropzone()
babel = Babel()
admin = Admin(base_template="admin/base_admin.html",
              template_mode='bootstrap4')
# totp = TOTP.using(secrets_path=Config.TOTP_SECRETS, issuer=Config.TOTP_ISSUER)

login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please log in to access this page.'
login_manager.anonymous_user = AnonymousUser

js = Bundle('js/functions.js', output='gen/main.js', filters="jsmin")


def create_app(config_file=Config):
    app = Flask(__name__)

    # import the Config file here:
    from app.models.roles import Role, UserRoles
    from app.models.user import User
    from app.models.posts import Post, Tag
    app.config.from_object(config_file)

    # Register error Blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # register the error handlers here:
    from app.errors.handlers import not_found_error, permission_denied, bad_request, internal_error
    app.register_error_handler(400, bad_request)
    app.register_error_handler(403, permission_denied)
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)

    # register Blueprints here:
    # from app.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # from app.admin import bp as admin_bp
    # app.register_blueprint(admin_bp)

    from app.blog import bp as blog_bp
    app.register_blueprint(blog_bp)

    # register all the js files here:
    assets.register('main_js', js)

    # Initiate all the objects for the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    assets.init_app(app)
    csrf.init_app(app)
    simplemde.init_app(app)
    dropzone.init_app(app)
    babel.init_app(app)
    admin.init_app(app, url='/admin', index_view=HomeAdminView())

    # User Security for Roles
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    # Flask-Admin templates override
    edit_template = 'admin/models/_blog_edit.html'
    create_template = 'admin/models/_blog_create.html'
    list_template = 'admin/models/_blog_list.html'

    # Use ModelView to override
    ModelView.edit_template = edit_template
    ModelView.create_template = create_template
    ModelView.list_template = list_template

    # Flask-Admin views
    admin.add_view(AdminUserView(User, db.session, category="Users"))
    admin.add_view(AdminPostView(Post, db.session, category="Posts"))
    admin.add_view(AdminRoleView(Role, db.session, category="Users"))
    admin.add_view(AdminTagView(Tag, db.session, category="Posts"))

    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.jinja_env.add_extension('jinja2.ext.do')
    app.jinja_env.add_extension('jinja2.ext.with_')
    app.jinja_env.add_extension('jinja2.ext.autoescape')
    app.jinja_env.add_extension('jinja2.ext.i18n')

    with app.app_context():
        db.create_all()

        # Create default roles:
        for role in Config.ROLES:
            if user_datastore.find_role(role=role) is None:
                user_datastore.create_role(name=role, description='{} role'.format(role))
                user_datastore.add_permissions_to_role(role=role, permissions=Config.PERMISSIONS_ADMIN)

        # Create admin user:
        if not user_datastore.find_user(email="danielf18@hotmail.com"):
            admin_user = user_datastore.create_user(email="danielf18@hotmail.com",
                                                    password=hash_password("toor"),
                                                    confirmed_at=datetime.utcnow())
            user_datastore.add_role_to_user(admin_user, 'admin')

        # Create all Tags:
        Tag.create_tags()

        db.session.commit()

        # service_values.ServiceValue.generate_service_values()

    return app


