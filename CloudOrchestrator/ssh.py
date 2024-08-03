import paramiko
import boto3
from .config import load_config, get_ssh_key_path, save_config

def ssh_ec2_instance(profile_name, instance_name, command):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']
    instance_id = None
    # Find instance ID by name
    for instance in config['accounts'][profile_name]['instances']:
        if instance['Name'] == instance_name:
            instance_id = instance['InstanceId']
            break
    if not instance_id:
        print(f"Instance '{instance_name}' not found in profile '{profile_name}'")
        return
    # Retrieve SSH key path
    ssh_key_path = get_ssh_key_path(profile_name)
    if not ssh_key_path:
        ssh_key_path = input(f"Enter path to PEM file for profile '{profile_name}': ")
        config['accounts'][profile_name]['ssh_key_path'] = ssh_key_path
        save_config(config)
    # Connect to EC2 instance via SSH
    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    if 'Reservations' in response and len(response['Reservations']) > 0:
        instance_info = response['Reservations'][0]['Instances'][0]
        public_dns_name = instance_info.get('PublicDnsName', None)
        if not public_dns_name:
            print(f"Public DNS not found for instance '{instance_name}'")
            return
        try:
            # Establish SSH connection
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(public_dns_name, username='ec2-user', key_filename=ssh_key_path)
            # Execute command
            stdin, stdout, stderr = ssh_client.exec_command(command)
            print(stdout.read().decode('utf-8'))
        except paramiko.AuthenticationException:
            print("Authentication failed. Check your SSH key permissions and profile settings.")
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            ssh_client.close()
    else:
        print(f"Instance '{instance_name}' not found or has no public DNS in profile '{profile_name}'")