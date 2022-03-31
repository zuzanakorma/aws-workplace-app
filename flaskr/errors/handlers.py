from flask import Blueprint, render_template
from flask_security import current_user

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', logged_in=current_user.is_authenticated), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', logged_in=current_user.is_authenticated), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', logged_in=current_user.is_authenticated), 500