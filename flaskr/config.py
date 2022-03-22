import os
import secrets
from flaskr.my_utils import get_secrets
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(16)
    # EXPLAIN_TEMPLATE_LOADING = True

    MARIADB_PASSWORD = os.environ.get("MARIADB_PASSWORD") or "securepassword"
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") or "securepassword"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_EMAIL_SENDER= 'no-reply@example.com'
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT= 465
    MAIL_USE_SSL= True

    MAIL_USERNAME = os.environ.get("EMAIL_USERNAME") or "fake@email.com"
    MAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD") or "securepassword"

    AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID") or "yourAWSaccessKey"
    AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY") or "yourAWSsecretKey"
    AWS_REGION=os.environ.get("AWS_REGION") or "eu-central-1"
    # S3_LOCATION = 'https://{}.s3.{}.amazonaws.com/'.format(os.environ.get("S3_BUCKET"), os.environ.get("REGION")) or "eu-west-2"


    SECURITY_USER_IDENTITY_ATTRIBUTES= os.environ.get("SECURITY_USER_IDENTITY_ATTRIBUTES") or 'email'
    SECURITY_PASSWORD_HASH= os.environ.get("SECURITY_PASSWORD_HASH") or 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT= os.environ.get("SECURITY_PASSWORD_SALT") or get_secrets("SECURITY_PASSWORD_SALT")  or "yourVerySecureSatlPassword"
    SECURITY_LOGIN_URL="/templates//login.html"
    SECURITY_POST_LOGIN_VIEW="/workplace"
    SECURITY_LOGIN_USER_TEMPLATE="/login.html"
    # default is none, but custom 403.html didnt work without it
    SECURITY_UNAUTHORIZED_VIEW=None



    # to get secret key in terminal
# >>> import secrets
# >>> secrets.token_hex(16)


    