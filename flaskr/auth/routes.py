from flask import render_template, url_for, request, redirect, flash
from flaskr.extensions import db
from flask_security import login_user, login_required, current_user, logout_user, utils
from .forms import LoginForm, RegistrationForm
from flask import Blueprint
from flaskr.models import User, Department, user_datastore


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    form.department.choices = form.department.choices + [dep.name for dep in db.session.query(Department.name)]
    if form.validate_on_submit():
        hashed_password =utils.encrypt_password(password=form.password.data)
        # hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode('utf-8')
        department_id = Department.query.filter(Department.name == form.department.data).first()
        user = User(firstname=form.firstname.data, lastname=form.lastname.data,
        member=department_id, email=form.email.data, password=hashed_password, active=True)
        user_datastore.add_role_to_user(user, 'end-user')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form, logged_in=current_user.is_authenticated)



@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and utils.verify_password(form.password.data, user.password):
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are logged in!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form, logged_in=current_user.is_authenticated)

    
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))