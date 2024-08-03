import boto3
import json
from .config import load_config, save_config

CONFIG_FILE_PATH = 'config.json'

def list_s3_buckets(profile_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    response = s3_client.list_buckets()

    buckets = []
    for bucket in response['Buckets']:
        buckets.append(bucket['Name'])

    # Update config with fetched buckets
    config['accounts'][profile_name]['s3_buckets'] = buckets
    save_config(config)

    return buckets

def create_s3_bucket(profile_name, bucket_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    response = s3_client.create_bucket(Bucket=bucket_name)

    print(f"S3 bucket '{bucket_name}' created successfully.")

def delete_s3_bucket(profile_name, bucket_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    s3_client.delete_bucket(Bucket=bucket_name)

    print(f"S3 bucket '{bucket_name}' deleted successfully.")
