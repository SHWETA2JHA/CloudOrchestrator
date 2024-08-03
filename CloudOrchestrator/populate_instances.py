import boto3
from .config import load_config, save_config

def populate_instances(profile_name):
    config = load_config()
    session = boto3.Session(profile_name=profile_name)
    ec2_client = session.client('ec2')
    response = ec2_client.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                "InstanceId": instance['InstanceId'],
                "Name": instance['Tags'][0]['Value'] if 'Tags' in instance and instance['Tags'] else ''
            })
    config['accounts'][profile_name]['instances'] = instances
    save_config(config)
