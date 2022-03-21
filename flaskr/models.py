from flask_security import current_user, UserMixin, \
     RoleMixin
from datetime import datetime
from .extensions import login_manager, db
from flask_security import SQLAlchemyUserDatastore



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)   


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    active= db.Column(db.Boolean)
    uploads = db.relationship("Uploads", backref="owner", lazy="dynamic")
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )   


    def __repr__(self):
        return f"{self.firstname} {self.lastname}"
  

class Uploads(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    def __repr__(self):
        return f"Project:'{self.project_name}', File:'{self.file_name}', User:'{self.user_id}'"


class Department(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship("User", backref="member", lazy="dynamic")
    uploads = db.relationship("Uploads", backref="department", lazy="dynamic")
    projects = db.relationship("Projects", backref="folder", lazy="dynamic")

    def __repr__(self):
        return f"Department: '{self.name}'"


class Projects(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    uploads = db.relationship("Uploads", backref="folder", lazy="dynamic")


    def __repr__(self):
        return f"Project:'{self.name}'"


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
