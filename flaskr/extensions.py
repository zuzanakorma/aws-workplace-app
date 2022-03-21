from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
# from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin


db = SQLAlchemy()
mail = Mail()
# bcrypt = Bcrypt()
login_manager = LoginManager()
admin = Admin(name='PharmaMax', 
        template_mode='bootstrap3', 
        base_template='admin/index.html')



