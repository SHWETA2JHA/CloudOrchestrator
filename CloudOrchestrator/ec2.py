import boto3
from .config import load_config, save_config

def start_ec2_instance(profile_name, instance_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    # Find instance ID by name
    instance_id = None
    for instance in config['accounts'][profile_name]['instances']:
        if instance['Name'] == instance_name:
            instance_id = instance['InstanceId']
            break

    if instance_id:
        ec2_client.start_instances(InstanceIds=[instance_id])
        print(f"Started EC2 instance '{instance_name}' (Instance ID: {instance_id})")
    else:
        print(f"Instance '{instance_name}' not found in profile '{profile_name}'")

    # Update config with updated instances list
    config['accounts'][profile_name]['instances'] = get_instances_list(profile_name)
    save_config(config)

def stop_ec2_instance(profile_name, instance_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    # Find instance ID by name
    instance_id = None
    for instance in config['accounts'][profile_name]['instances']:
        if instance['Name'] == instance_name:
            instance_id = instance['InstanceId']
            break

    if instance_id:
        ec2_client.stop_instances(InstanceIds=[instance_id])
        print(f"Stopped EC2 instance '{instance_name}' (Instance ID: {instance_id})")
    else:
        print(f"Instance '{instance_name}' not found in profile '{profile_name}'")

    # Update config with updated instances list
    config['accounts'][profile_name]['instances'] = get_instances_list(profile_name)
    save_config(config)

def get_instances_list(profile_name):
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

    return instances

def execute_ssh_command(profile_name, instance_name, pem_file_path, command):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']
    instance_id = None

    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    for instance in config['accounts'][profile_name]['instances']:
        if instance['Name'] == instance_name:
            instance_id = instance['InstanceId']
            break

    if not instance_id:
        print(f"Instance '{instance_name}' not found in profile '{profile_name}'")
        return

    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    if not response['Reservations']:
        print(f"Instance '{instance_name}' not found in profile '{profile_name}'")
        return

    instance_info = response['Reservations'][0]['Instances'][0]
    if instance_info['State']['Name'] != 'running':
        print(f"Instance '{instance_name}' is not running.")
        return

    instance_ip = instance_info['PublicIpAddress']
    ssh_command = f"ssh -i {pem_file_path} ec2-user@{instance_ip} '{command}'"

    import subprocess
    try:
        subprocess.run(ssh_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing SSH command: {e}")