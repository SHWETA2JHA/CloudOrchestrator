import os
import subprocess
import boto3
from .config import load_config, save_config

def create_ecr_repository(ecr_client, repository_name):
    try:
        ecr_client.create_repository(repositoryName=repository_name)
        print(f'Successfully created {repository_name}:latest')
    except ecr_client.exceptions.RepositoryAlreadyExistsException:
        print(f'Repository {repository_name} already exists.')

def build_and_push_docker_image(repository_name, folder_name, aws_region, aws_account_id):
    os.chdir(folder_name)
    command = f'aws ecr get-login-password --region {aws_region} | sudo docker login --username AWS --password-stdin {aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com'
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")
    subprocess.run(['sudo', 'docker', 'build', '-t', repository_name, '.'])
    subprocess.run(['sudo', 'docker', 'tag', f'{repository_name}:latest', f'{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com/{repository_name}:latest'])
    push_process = subprocess.Popen(['sudo', 'docker', 'push', f'{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com/{repository_name}:latest'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    push_process.wait()
    if push_process.returncode == 0:
        print(f'Successfully pushed {repository_name}:latest')
    else:
        print(f'Error pushing {repository_name}:latest')
        print(push_process.stderr.read().decode())
        raise Exception(f'Error pushing {repository_name}:latest')

def create_lambda_function(lambda_client, function_name, repository_name, aws_account_id, aws_region):
    ecr_image_uri = f'{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com/{repository_name}:latest'
    lambda_client.create_function(
        FunctionName=function_name,
        Code={'ImageUri': ecr_image_uri},
        PackageType='Image',
        ImageConfig={'Command': ['app.handler'], 'WorkingDirectory': ''},
        Role=f'arn:aws:iam::{aws_account_id}:role/LambdaRole',
        MemorySize=8192,
        Timeout=180
    )
    print(f'Successfully created Lambda function {function_name}')

def create_and_deploy_algorithm(profile, resource_name, folder_name):
    config = load_config()
    aws_region = config['accounts'][profile]['region']
    aws_account_id = config['accounts'][profile]['account_id']
    ecr_client = boto3.client('ecr', aws_access_key_id=config['accounts'][profile]['access_key'], aws_secret_access_key=config['accounts'][profile]['secret_key'], region_name=aws_region)
    lambda_client = boto3.client('lambda', aws_access_key_id=config['accounts'][profile]['access_key'], aws_secret_access_key=config['accounts'][profile]['secret_key'], region_name=aws_region)
    create_ecr_repository(ecr_client, resource_name)
    build_and_push_docker_image(resource_name, folder_name, aws_region, aws_account_id)
    create_lambda_function(lambda_client, resource_name, resource_name, aws_account_id, aws_region)
    print(f'Successfully created and deployed {resource_name}')
    # Update config file with new tag
    current_tag = config['deploy']['kaiznn']['algorithm']['1d']['tag']
    major, minor = map(int, current_tag[1:].split('.'))
    new_tag = f'v{major}.{minor + 1}'
    config['deploy']['kaiznn']['algorithm']['1d']['tag'] = new_tag
    save_config(config)
