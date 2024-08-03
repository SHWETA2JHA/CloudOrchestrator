import boto3
from .config import load_config, save_config

def start_rds_instance(profile_name, db_instance_identifier):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    rds_client = boto3.client('rds', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    response = rds_client.start_db_instance(DBInstanceIdentifier=db_instance_identifier)
    print(f"Started RDS instance '{db_instance_identifier}'")

def stop_rds_instance(profile_name, db_instance_identifier):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    rds_client = boto3.client('rds', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    response = rds_client.stop_db_instance(DBInstanceIdentifier=db_instance_identifier)
    print(f"Stopped RDS instance '{db_instance_identifier}'")

def list_rds_instances(profile_name):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    rds_client = boto3.client('rds', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    response = rds_client.describe_db_instances()

    instances = []
    for db_instance in response['DBInstances']:
        db_instance_identifier = db_instance['DBInstanceIdentifier']
        db_instance_status = db_instance['DBInstanceStatus']
        instances.append({'DBInstanceIdentifier': db_instance_identifier, 'DBInstanceStatus': db_instance_status})

    config['accounts'][profile_name]['rds_instances'] = instances
    save_config(config)

    if instances:
        print(f"RDS Instances in profile '{profile_name}':")
        for instance in instances:
            print(f"DB Instance Identifier: {instance['DBInstanceIdentifier']}, Status: {instance['DBInstanceStatus']}")
    else:
        print(f"No RDS instances found in profile '{profile_name}'.")

    print(f"RDS instances in profile '{profile_name}' have been updated in config file.")