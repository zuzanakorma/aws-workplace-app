from flask import render_template, url_for, request, redirect, flash
from flaskr.extensions import db
from flask_security import login_user, login_required, current_user, logout_user, utils
from .forms import LoginForm, RegistrationForm, ResetPasswordForm, RequestResetForm
from flask import Blueprint
from flaskr.models import User, Department, user_datastore
from flaskr.my_utils import send_reset_email


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



@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)



@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data).first()
        hashed_password =utils.encrypt_password(password=form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)