from flaskr.extensions import db
from flask import redirect, render_template, flash, url_for, request, send_file
from flask_security import current_user, login_required, roles_required 
from .forms import CreateProjectFolderForm, UploadFileForm, DeleteProjectFolderForm, \
                    DeleteFileForm, FileReportForm, SelectFolderForm
from flaskr.my_utils import create_new_bucket, delete_my_file, upload_new_file, \
                    list_my_buckets, delete_my_bucket, list_files_in_bucket
from flaskr.models import Projects, Uploads, User, Department
from flask import  Blueprint


 
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@main.route('/workplace')
@login_required
def workplace():
    return render_template("workplace.html", logged_in=current_user.is_authenticated)


# compare projects in aws and db and get matches
def get_department_buckets():
    department_projects = Projects.query.filter_by(department_id = current_user.department_id)
    project_names = [i.name for i in department_projects]
    aws_bucket_names = list_my_buckets()
    project_matches=list(set(project_names).intersection(aws_bucket_names))
    if len(project_matches) == 0:
        flash(f"No projects for your department! To continue, please, create project folder first.", "warning")
        # return None
    else:
        return project_matches
    

# CREATE
@main.route('/workplace/create_project', methods=["GET", "POST"])
# @login_required
@roles_required('admin') 
def create_project():
    form = CreateProjectFolderForm()
    if form.validate_on_submit():
        bucket = form.project_folder_name.data
        create_new_bucket(bucket, region="eu-west-2")
        department_id = Department.query.get(current_user.department_id)
        project=Projects(name=bucket, folder=department_id)
        db.session.add(project)
        db.session.commit()
        flash(f"Project {bucket} has been created.", "success")
        return redirect(url_for('main.workplace'))
    return render_template("create_folder.html", form=form, logged_in=current_user.is_authenticated)


@main.route('/workplace/upload_file', methods=["GET", "POST"])
@login_required
def upload_file():
    form = UploadFileForm()
    form.project_folder_name.choices = get_department_buckets()
    # if request.method == "POST":
    if form.validate_on_submit():
        bucket = form.project_folder_name.data
        
        # if users write file name
        if form.file_name.data:
            file_data = form.file_to_upload.data
            print(file_data)
            file_data.filename = form.file_name.data
            upload_new_file(file_data=file_data, 
                bucket_name=bucket)
            # fix this, user_id not in db
            
            # department_id = User.query.filter(Department.name == form.department.data).first()
            department_id = Department.query.get(current_user.department_id)
            user_id = User.query.get(current_user.id)
            project_id = Projects.query.filter(Projects.name == form.project_folder_name.data).first()
            print(user_id.department_id)
            upload = Uploads(folder=project_id,
                            file_name=form.file_name.data,
                            owner=user_id,
                            department=department_id
                                )
            db.session.add(upload)
            db.session.commit()
            flash(f"File {form.file_name.data} in project {bucket} has been uploaded.", "success")
        # else used uploaded file as default
        else:
            file_data = form.file_to_upload.data
            upload_new_file(file_data=file_data, bucket_name=bucket)
            flash(f"File {file_data.filename} in project {bucket} has been uploaded.", "success")
        return redirect(url_for('main.workplace'))
    return render_template("upload_file.html", form=form, logged_in=current_user.is_authenticated)

# DELETE
@main.route('/workplace/delete_project', methods=["GET", "POST"])
# @login_required
@roles_required('admin') 
def delete_project():
    form = DeleteProjectFolderForm()
    form.project_folder_name.choices = get_department_buckets()
    if form.validate_on_submit():
        bucket = form.project_folder_name.data
        delete_my_bucket(bucket)
        flash(f"Project {bucket} has been deleted.", "success")
        return redirect(url_for('main.workplace'))
    return render_template("delete_folder.html", form=form, logged_in=current_user.is_authenticated)



@main.route('/workplace/delete_file', methods=["GET", "POST"])
@login_required
def select_folder():
    form = SelectFolderForm()
    form.project_folder_name.choices = get_department_buckets()
    if request.method == 'POST':
        bucket = form.project_folder_name.data
        return redirect(url_for('main.delete_file', bucket=bucket))
    return render_template("select_folder.html", form=form, logged_in=current_user.is_authenticated)

@main.route('/workplace/delete_file/<bucket>', methods=["GET", "POST"])
@login_required
def delete_file(bucket):
    form = DeleteFileForm()
    form.project_folder_name.choices = [bucket]
    form.file_to_delete.choices = list_files_in_bucket(bucket)
    

    if form.validate_on_submit(): 
        bucket = form.project_folder_name.data
        
        file_to_delete = form.file_to_delete.data
        delete_my_file(file_to_delete, bucket)
        flash(f"File {file_to_delete} from Project {bucket} has been deleted.", "success")
        
        return redirect(url_for('main.workplace'))   

    return render_template("delete_file.html", form=form, logged_in=current_user.is_authenticated)


# REPORT
@main.route('/folders_report', methods=["GET", "POST"])
@login_required
def folders_report():
    buckets = get_department_buckets()
    return render_template("folders_report.html", buckets=buckets, logged_in=current_user.is_authenticated)


@main.route('/download/<bucket>')
@login_required
def download(bucket):
    with open("flaskr/download.csv","w") as f:
        for file in list_files_in_bucket(bucket):
            f.writelines(file)
            f.write("\n")
        # flash(f"File \'download.csv' has been downloaded", "success")
    return send_file('download.csv')

    # return redirect(url_for('workplace'))
   
@main.route('/report', methods=["GET", "POST"])
@login_required
def report():
    form = FileReportForm()
    form.project_folder_name.choices = get_department_buckets()
    if form.validate_on_submit(): 
        bucket = form.project_folder_name.data
        return download(bucket)
        # return redirect(url_for('download', bucket=bucket))
    
    return render_template("report.html", form=form, logged_in=current_user.is_authenticated)