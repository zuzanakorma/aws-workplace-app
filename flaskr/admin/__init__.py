from flask import Blueprint

bp_admin = Blueprint('bp_admin', __name__)

from flaskr.admin import routes
