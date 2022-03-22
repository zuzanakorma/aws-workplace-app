import boto3
import logging
# import os
from botocore.exceptions import ClientError
from flaskr.config import Config
# from dotenv import load_dotenv

# # take environment variables from .env
# load_dotenv()

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


s3_client = boto3.client('s3', aws_access_key_id=Config.AWS_ACCESS_KEY_ID, 
                            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                            region_name=Config.AWS_REGION)

# ============== Files =========================
def upload_new_file(file_data, bucket_name):
    try:
        upload_file_bucket = bucket_name
        upload_file_key = str(file_data.filename)
        # upload_file_key = bucket_name + "/" + str(file_data.filename)
        s3_client.put_object(Bucket=upload_file_bucket, Body=file_data.read(),Key=upload_file_key)

        # problem: filename needs to be str, upload_file doesnt support bytes
        # s3_client.upload_file(file_name.read(), upload_file_bucket, upload_file_key)
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


def list_files_in_bucket(bucket_name):
    s3 = boto3.resource('s3')
    response = s3.Bucket(bucket_name)
    file_list = []
    for file in response.objects.all():
        file_list.append(file.key)
    return file_list

# ============== Buckets =========================

def create_new_bucket(bucket_name, region):
    try:
        s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration={
                                        'LocationConstraint': region})
        logger.info(f'Bucket {bucket_name} created')
             
    except ClientError as e:
        # The exceptions are related to issues with client-side behaviors, 
        # configurations, or validations.
        logging.error(e)
        return False
    return True


def list_my_buckets():
    response = s3_client.list_buckets()
    bucket_list = []
    for bucket in response['Buckets']:
        bucket_list.append(bucket["Name"])

        # print(f'{bucket["Name"]}')
    return bucket_list


def delete_my_bucket(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    try:
        bucket.delete()
        logger.info(f'Bucket {bucket_name} deleted')
    except:
        all_files = list_files_in_bucket(bucket_name)
        list_keys = []
        for i in all_files:
            list_keys.append({"Key": i})
        response = bucket.delete_objects(
            Delete={
                'Objects': list_keys
            })
        bucket.delete()
        logger.info(f'Bucket {bucket_name} deleted')
        





