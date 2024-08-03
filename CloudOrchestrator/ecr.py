import boto3
import json
from .config import load_config, save_config

CONFIG_FILE_PATH = 'config.json'

def list_ecr_repositories(profile_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    ecr_client = boto3.client('ecr', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    response = ecr_client.describe_repositories()

    repositories = []
    for repository in response['repositories']:
        repositories.append({'RepositoryName': repository['repositoryName']})

    return repositories

def create_ecr_repository(profile_name, repository_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    ecr_client = boto3.client('ecr', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    response = ecr_client.create_repository(repositoryName=repository_name)

    print(f"ECR repository '{repository_name}' created successfully.")

def delete_ecr_repository(profile_name, repository_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    ecr_client = boto3.client('ecr', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    ecr_client.delete_repository(repositoryName=repository_name, force=True)

    print(f"ECR repository '{repository_name}' deleted successfully.")

def describe_ecr_repository(profile_name, repository_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    ecr_client = boto3.client('ecr', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    response = ecr_client.describe_repositories(repositoryNames=[repository_name])

    repository_info = response['repositories'][0]

    print(f"ECR Repository Name: {repository_info['repositoryName']}")
    print(f"Registry ID: {repository_info['registryId']}")
    print(f"Repository ARN: {repository_info['repositoryArn']}")
    print(f"Repository URI: {repository_info['repositoryUri']}")
    print(f"Created At: {repository_info['createdAt']}")

def get_ecr_repository_uri(profile_name, repository_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    ecr_client = boto3.client('ecr', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    response = ecr_client.describe_repositories(repositoryNames=[repository_name])

    repository_info = response['repositories'][0]

    return repository_info['repositoryUri']
