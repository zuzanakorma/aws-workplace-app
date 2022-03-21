from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.fields.core import DateTimeField, SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NoneOf, Regexp, Length, Email, Optional
from flask_wtf.file import FileField, FileAllowed




class CreateProjectFolderForm(FlaskForm):
    project_folder_name = StringField("Project Name", validators=[DataRequired(), 
                        Regexp('(?!^(\d{1,3}\.){3}\d{1,3}$)(^[a-z0-9]([a-z0-9-]*(\.[a-z0-9])?)*$)', message="Project names can contain lowercase letters, numbers, and hyphens."), 
                        Length(min=3, max=63,  message="Project names must be betwen 3 & 63 characters")])
    submit = SubmitField('Create')

# AWS S3 Bucket names
# Bucket names must be at least 3 and no more than 63 characters long.
# Bucket names must be a series of one or more labels.
# Bucket names can contain lowercase letters, numbers, and hyphens.
# Each label must start and end with a lowercase letter or a number.
# Adjacent labels are separated by a single period (.)
# Bucket names must not be formatted as an IP address (for example, 192.168.5.4)


class UploadFileForm(FlaskForm):
    project_folder_name = SelectField("All Projects", choices=[], validators=[DataRequired()])
    file_name = StringField("File Name", validators=[Regexp("^.*\.(jpeg|png|jpg|gif|doc|pdf|docx|xls|xlsx|csv|txt|html)$", 
                        message='File name must have an extension to be uploaded'), Length(min=3, max=63)])
    file_to_upload = FileField('Upload Project File', validators=[DataRequired(), 
                    FileAllowed(['pdf','doc','docx','xls','xlsx','csv','txt','html','jpg','jpeg','png','gif'])])
    description = TextAreaField("Description", validators=[Optional(), Length(max=200)])
    submit = SubmitField('Upload')


class SelectFolderForm(FlaskForm):
    project_folder_name = SelectField("All Projects", choices=[], validators=[DataRequired()])
    submit = SubmitField('Select')


class DeleteProjectFolderForm(FlaskForm):
    project_folder_name = SelectField("All Projects", choices=[], validators=[DataRequired()])
    project_to_delete = StringField("Confirm Project Name", validators=[DataRequired(), EqualTo("project_folder_name", message='Project name must match!')])
    submit = SubmitField('Delete')


class DeleteFileForm(FlaskForm):
    project_folder_name = SelectField("Selected Project", choices=[], validators=[DataRequired()])
    file_to_delete = SelectField("Select File to Delete", choices=[], validators=[DataRequired()])
    file_to_delete_confirm = StringField("Confirm File Name", validators=[DataRequired(), EqualTo("file_to_delete", message='File name must match!')]) 
    submit = SubmitField('Delete')


class FileReportForm(FlaskForm):
    project_folder_name = SelectField("All Projects", choices=[], validators=[DataRequired()])
    submit = SubmitField('Download Your Files Report')