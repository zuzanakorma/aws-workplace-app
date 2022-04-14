from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, EqualTo, NoneOf, Length, Email, ValidationError
from flaskr.models import User



class RegistrationForm(FlaskForm):
    firstname = StringField(render_kw={"placeholder": "First Name"}, validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField(render_kw={"placeholder": "Last Name"}, validators=[DataRequired(), Length(min=2, max=20)])
    email= StringField(render_kw={"placeholder": "Email"}, validators=[DataRequired(), Email()])
    # Getting choices from database instead of WTF
    # department = SelectField("Department", choices=[('HR','Human Resources'), ('PD','Product Development'), ('QA', 'Quality Assurance')], 
    department = SelectField(label="Department", choices=["Department"], validators=[DataRequired(), NoneOf(values=["Department"], message="Please, Select Department!")])
    password = PasswordField(render_kw={"placeholder": "Password"}, validators=[DataRequired()])
    confirm_password = PasswordField(render_kw={"placeholder": "Confirm Password"}, validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

     # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField(render_kw={"placeholder": "Email"},
                        validators=[DataRequired(), Email()])
    password = PasswordField(render_kw={"placeholder": "Password"}, validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') 

    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         user = User.query.filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError('That email is taken. Please choose a different one.')               


class RequestResetForm(FlaskForm):
    email = StringField(render_kw={"placeholder": "Email"},
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(render_kw={"placeholder": "Password"}, validators=[DataRequired()])
    confirm_password = PasswordField(render_kw={"placeholder": 'Confirm Password'},
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')