import json
import boto3 
CONFIG_FILE_PATH = 'config.json'

def initialize_config():
    config = {
        'accounts': {},
        'deploy': {}
    }
    save_config(config)

def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        initialize_config()
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config = json.load(config_file)
    return config

def save_config(config):
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        json.dump(config, config_file, indent=4)

def add_aws_account(profile_name, access_key, secret_key, region):
    config = load_config()
    config['accounts'][profile_name] = {
        'access_key': access_key,
        'secret_key': secret_key,
        'region': region,
        'instances': []
    }
    save_config(config)
    print(f"AWS account '{profile_name}' added successfully.")

def get_ssh_key_path(profile_name):
    config = load_config()
    return config['accounts'][profile_name].get('ssh_key_path', None)

def list_instances(profile_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    response = ec2_client.describe_instances()

    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_name = ''
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
                    break
            instances.append({'InstanceId': instance_id, 'Name': instance_name})

    config['accounts'][profile_name]['instances'] = instances
    save_config(config)

    if instances:
        print(f"Instances in profile '{profile_name}':")
        for instance in instances:
            print(f"Instance ID: {instance['InstanceId']}, Name: {instance['Name']}")
    else:
        print(f"No instances found in profile '{profile_name}'.")

    print(f"Instances in profile '{profile_name}' have been updated in config file.")

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

    config['accounts'][profile_name]['s3_buckets'] = buckets
    save_config(config)

    if buckets:
        print(f"S3 buckets in profile '{profile_name}':")
        for bucket in buckets:
            print(bucket)
    else:
        print(f"No S3 buckets found in profile '{profile_name}'.")

    print(f"S3 buckets in profile '{profile_name}' have been updated in config file.")

def update_deploy_config(profile_name, resource_name, algorithm, version, path):
    config = load_config()
    if profile_name not in config['deploy']:
        config['deploy'][profile_name] = {}
    if resource_name not in config['deploy'][profile_name]:
        config['deploy'][profile_name][resource_name] = {}
    if algorithm not in config['deploy'][profile_name][resource_name]:
        config['deploy'][profile_name][resource_name][algorithm] = {}
    config['deploy'][profile_name][resource_name][algorithm]['name'] = f"{resource_name}_{algorithm}_algorithm"
    config['deploy'][profile_name][resource_name][algorithm]['path'] = path
    config['deploy'][profile_name][resource_name][algorithm]['tag'] = version
    save_config(config)
    print(f"Deployment configuration for '{resource_name}' updated successfully.")

def get_route53_client(profile_name=None):
    if not profile_name:
        profile_name = input("Enter AWS profile name: ")

    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']
    
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )
    
    return session.client('route53')