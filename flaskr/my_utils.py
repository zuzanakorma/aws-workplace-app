import boto3
import logging
import requests
import os
from flask import url_for
from botocore.exceptions import ClientError
from botocore.config import Config
from flask_mail import Message, Mail
from dotenv import load_dotenv

mail = Mail()
# take environment variables from .env
load_dotenv()

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

my_config = Config(
    region_name = os.environ.get("AWS_REGION") or 'eu-central-1',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

aws_client_creds = {
    "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY")
}

try:
    sts_client = boto3.client("sts", config=my_config, **aws_client_creds)
                            
    assumed_role_object=sts_client.assume_role(
        RoleArn=os.environ.get("AWS_ASSUMED_ROLE_ARN"),
        RoleSessionName="AssumeRoleSession1"
    )
    credentials=assumed_role_object['Credentials']
    aws_client_creds["aws_access_key_id"] = credentials['AccessKeyId']
    aws_client_creds["aws_secret_access_key"] = credentials['SecretAccessKey']
    aws_client_creds["aws_session_token"]=credentials['SessionToken']

except:
    pass
    

s3_client = boto3.client("s3",**aws_client_creds)
    

# ============== Files =========================
def upload_new_file(file_data, bucket_name):
    try:
        upload_file_bucket = bucket_name
        upload_file_key = str(file_data.filename)
        s3_client.put_object(Bucket=upload_file_bucket, Body=file_data.read(),Key=upload_file_key)
        logger.info(f'File {file_data} uploaded')
    except ClientError as e:
        logging.error(e)
        return False
    return True
    

def delete_my_file(file_name, bucket_name):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=file_name)
        logger.info(f'File {file_name} deleted')
    except ClientError as e:
        logger.info(f'File {file_name} does not exist!')
        logging.error(e)
        return False
    return True

# check if bucket is empty before list objects, to avoid error. 
def is_bucket_empty(bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if response['KeyCount']== 0:
        return True
    else:
        return response
        
        
def list_files_in_bucket(bucket_name):
    response = is_bucket_empty(bucket_name)
    if response is not True:
        file_list = []
        for file in response["Contents"]:
            file_list.append(file["Key"])
        return file_list
    else:
        logger.info(f'Project folder {bucket_name} is empty!')
        return False

            

# ============== Buckets =========================

def create_new_bucket(bucket_name, region):
    try:
        s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration={
                                        'LocationConstraint': region})
        logger.info(f'Bucket {bucket_name} created')
             
    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_my_buckets():
    response = s3_client.list_buckets()
    bucket_list = []
    for bucket in response['Buckets']:
        bucket_list.append(bucket["Name"])

    return bucket_list


def delete_my_bucket(bucket_name):
    try:
        response = s3_client.delete_bucket(Bucket=bucket_name)
        logger.info(f'Bucket {bucket_name} deleted')
    except:
        all_files = list_files_in_bucket(bucket_name)
        list_keys = []
        for i in all_files:
            list_keys.append({"Key": i})
        response = s3_client.delete_objects(Bucket=bucket_name,
            Delete={
                'Objects': list_keys
            })
        response = s3_client.delete_bucket(Bucket=bucket_name)
        logger.info(f'Bucket {bucket_name} deleted')
        


# ============== SSM Parameter store =========================
ssm_client = boto3.client('ssm',config=my_config, **aws_client_creds)

def get_secrets(parameter_name, parameter_decryption=True):
    response = ssm_client.get_parameter(
        Name=parameter_name, 
        WithDecryption=parameter_decryption
        )
    return response['Parameter']['Value']

# ============== Get News APIs =========================
def get_news(query, language, category, country, sort_by):
    OWM_Endpoint = "https://newsapi.org/v2/top-headlines?"
    api_key=os.environ.get("api_key")
    params = {
        'q':query,
        'domains':'bbc.co.uk,techcrunch.com',
        'language':language,
        'country': country,
        'category': category,
        'sort_by':sort_by,
        'page':1
        }
    headers = {'X-Api-Key': api_key}

    response = requests.get(url=OWM_Endpoint, params=params, headers=headers)
    result = response.json()
    return result

# ============== Send email to reset password =========================
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender="noreply@demo.com",
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('auth.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
    return 'Sent'