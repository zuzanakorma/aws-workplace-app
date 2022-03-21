from flask import Flask, url_for
from flaskr.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from flaskr.extensions import db, login_manager, mail, admin
    db.init_app(app)
    # bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
     
    from .main.routes import main
    from flaskr.errors.handlers import errors
    from flaskr.auth.routes import auth
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(auth)


    from flask_security import utils, Security, SQLAlchemyUserDatastore, roles_required
    from flaskr.models import User, Department, Role, Uploads, user_datastore
    from flask_admin import helpers as admin_helpers
    from flaskr.admin.routes import UserView, ModelView, DepartmentView, MyModelView

    admin.add_view(UserView(User, db.session))
    admin.add_view(ModelView(Uploads, db.session))
    admin.add_view(DepartmentView(Department, db.session))
    admin.add_view(MyModelView(Role, db.session))
   

    
    security = Security(app, user_datastore)
    
 
    @app.before_first_request
    def restrict_admin_url():
        endpoint = 'admin.index'
        url = url_for(endpoint)
        admin_index = app.view_functions.pop(endpoint)

        @app.route(url, endpoint=endpoint)
        @roles_required('admin')
        def secure_admin_index():
            return admin_index()

   


#   define a context processor for merging flask-admin's template context into the
#     flask-security views.    
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
    )
   

    @app.before_first_request
    def before_first_request():

        db.create_all()
        departments = ['Human Resources', 'Product Development', 'Quality Assurance']

        for department in departments:
            try:
                dep = Department(name=department)
                db.session.add(dep)
                db.session.commit()
            except:
                pass
            finally:
                db.session.close()

        users = [
        {
            "firstname": "Jane",
            "lastname": "Doe",
            "email": "admin@example.com",
            "password": "password",
            "member": "Human Resources",
            "active": 1
        },
        {    
            "firstname": "John",
            "lastname": "Goe",
            "email": "user@example.com",
            "password": "1234",
            "member": "Human Resources",
            "active": 1
        },
        ]

        for user in users:
            try:
                u = User(firstname=user["firstname"],
                        lastname=user["lastname"],
                        member=Department.query.filter(Department.name == user["member"]).first(),
                        email=user["email"],
                        active=user["active"],
                        password=utils.encrypt_password(password=user["password"]))
                        
                db.session.add(u)
                db.session.commit()
            except:
                pass
            finally:
                db.session.close()

        user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_datastore.find_or_create_role(name='end-user', description='End user')
       
        # if not user_datastore.get_user('user@example.com'):
        #     user_datastore.create_user(email='johngoe@example.com', password=utils.encrypt_password('1234'))
        # if not user_datastore.get_user('admin@example.com'):
        #     user_datastore.create_user(email='admin@example.com', password=utils.encrypt_password('password'))
        # db.session.commit()

        user_datastore.add_role_to_user('user@example.com', 'end-user')
        user_datastore.add_role_to_user('admin@example.com', 'admin')
        db.session.commit()

    return app











