import sys
import json
import subprocess
import boto3
import os

CONFIG_FILE = './config.json'

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_aws_clients(profile_name):
    config = load_config()
    profile = config['accounts'].get(profile_name)
    if not profile:
        raise ValueError(f"Profile '{profile_name}' not found in config.json")

    session = boto3.Session(
        aws_access_key_id=profile['access_key'],
        aws_secret_access_key=profile['secret_key'],
        region_name=profile['region']
    )

    ecr_client = session.client('ecr')
    lambda_client = session.client('lambda')
    return ecr_client, lambda_client

def get_latest_ecr_tag(ecr_client, repository_name):
    try:
        response = ecr_client.describe_images(repositoryName=repository_name, filter={'tagStatus': 'TAGGED'})
        tags = [image_detail['imageTags'][0] for image_detail in response['imageDetails'] if 'imageTags' in image_detail]
        if tags:
            latest_tag = sorted(tags)[-1]
            return latest_tag
        return None
    except Exception as e:
        print(f'Error fetching tags: {str(e)}')
        return None

def increment_tag(tag):
    if tag and tag.startswith('v'):
        version = tag[1:]
    else:
        version = '1.0'
    print
    parts = version.split('.')
    if parts[-1].isdigit():
        parts[-1] = str(int(parts[-1]) + 1)
    else:
        parts[-1] = '1'

    new_tag = 'v' + '.'.join(parts)
    return new_tag


def create_ecr_repository(ecr_client, repository_name):
    try:
        ecr_client.create_repository(repositoryName=repository_name)
        print(f'Successfully created ECR repository {repository_name}')
    except ecr_client.exceptions.RepositoryAlreadyExistsException:
        print(f'ECR repository {repository_name} already exists')

def build_and_push_docker_image(ecr_client, repository_name, folder_path, new_tag):
    os.chdir(folder_path)
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    region = ecr_client.meta.region_name
    command = f'aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {account_id}.dkr.ecr.{region}.amazonaws.com'
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")
    subprocess.run(['docker', 'build', '-t', f'{repository_name}:{new_tag}', '.'])
    subprocess.run(['docker', 'tag', f'{repository_name}:{new_tag}', f'{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{new_tag}'])
    subprocess.run(['docker', 'push', f'{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{new_tag}'])
    print(f'Successfully pushed Docker image {repository_name}:{new_tag}')

def create_lambda_function(lambda_client, function_name, repository_name, new_tag):
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    region = lambda_client.meta.region_name
    ecr_image_uri = f'{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{new_tag}'
    lambda_client.create_function(
        FunctionName=function_name,
        Code={'ImageUri': ecr_image_uri},
        PackageType='Image',
        ImageConfig={'Command': ['app.handler'], 'WorkingDirectory': ''},
        Role=f'arn:aws:iam::{account_id}:role/LambdaRole',
        MemorySize=8192,
        Timeout=180
    )
    print(f'Successfully created Lambda function {function_name}')

def update_lambda_function(lambda_client, function_name, repository_name, image_tag):
    try:
        account_id = boto3.client('sts').get_caller_identity().get('Account')
        region = lambda_client.meta.region_name
        ecr_image_uri = f'{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{image_tag}'
        lambda_client.update_function_code(
            FunctionName=function_name,
            ImageUri=ecr_image_uri
        )
        print(f'Successfully updated Lambda function {function_name} with image {repository_name}:{image_tag}')
    except Exception as e:
        print(f'Error: {str(e)}')

def deploy_existing(profile_name, resource_name, folder_path):
    ecr_client, lambda_client = get_aws_clients(profile_name)
    latest_tag = get_latest_ecr_tag(ecr_client, resource_name)
    new_tag = increment_tag(latest_tag)
    build_and_push_docker_image(ecr_client, resource_name, folder_path, new_tag)
    
    # Check if Lambda function already exists
    try:
        lambda_client.get_function(FunctionName=resource_name)
        update_lambda_function(lambda_client, resource_name, resource_name, new_tag)
    except lambda_client.exceptions.ResourceNotFoundException:
        # Lambda function doesn't exist, create it
        create_lambda_function(lambda_client, resource_name, resource_name, new_tag)
    
    return new_tag

def deploy_new(profile_name, resource_name, folder_path):
    ecr_client, lambda_client = get_aws_clients(profile_name)
    create_ecr_repository(ecr_client, resource_name)
    new_tag = 'v1.0'
    build_and_push_docker_image(ecr_client, resource_name, folder_path, new_tag)
    create_lambda_function(lambda_client, resource_name, resource_name, new_tag)
    return new_tag

def deploy_cli(profile_name,resource_name,folder_path):
    print('Choose deployment option:')
    print('1. Deploy using existing Lambda and ECR repository')
    print('2. Create ECR, build image, push to Lambda, create Lambda')
    option = input('Enter option (1 or 2): ').strip()

    if option == '1':
        new_tag = deploy_existing(profile_name, resource_name, folder_path)
    elif option == '2':
        new_tag = deploy_new(profile_name, resource_name, folder_path)
    else:
        print('Invalid option')
        sys.exit(1)

    print(f'Successfully deployed {resource_name} with tag {new_tag}')

if __name__ == '__main__':
    deploy_cli()
