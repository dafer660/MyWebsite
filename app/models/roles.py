from flask_security import RoleMixin
from flask_admin.contrib.sqla import ModelView

from app import db
from config import Config


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Role id: {self.id}, name: {self.name}, permissions: {self.permissions}>"


class UserRoles(db.Model, RoleMixin):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

    @staticmethod
    def get_all_user_roles():
        return UserRoles.query.all()

    @staticmethod
    def get_user_roles(user_id):
        user_roles = UserRoles.query.filter_by(user_id=user_id).all()

        roles = list()
        for user_role in user_roles:
            current_role = Role.get_role_by_id(role_id=user_role.id)
            roles.append(current_role.name)

        # using List Comprehension:
        # roles = [(Role.query.filter_by(id=role.id).first()).name for role in user_roles]
        return roles
