import boto3
from .config import load_config

def list_resources_by_tag(profile_name, tag_keyword):
    config = load_config()
    aws_access_key = config['accounts'][profile_name]['access_key']
    aws_secret_key = config['accounts'][profile_name]['secret_key']
    aws_region = config['accounts'][profile_name]['region']

    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    rds_client = boto3.client('rds', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    lambda_client = boto3.client('lambda', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    ecr_client = boto3.client('ecr', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    ecs_client = boto3.client('ecs', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    # Function to check if a tag contains the keyword
    def tag_contains_keyword(tags, keyword):
        for tag in tags:
            if keyword in tag['Value']:
                return True
        return False

    # Function to check if a name contains the keyword
    def name_contains_keyword(name, keyword):
        if keyword in name:
            return True
        return False

    # List EC2 instances by tag or name
    ec2_response = ec2_client.describe_instances()
    ec2_instances = []
    for reservation in ec2_response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_name = next((tag['Value'] for tag in instance['Tags'] if tag_keyword in tag['Value']), instance.get('Tags', [{'Value': ''}])[0]['Value'])
            if tag_contains_keyword(instance['Tags'], tag_keyword) or name_contains_keyword(instance_name, tag_keyword):
                ec2_instances.append({'InstanceId': instance_id, 'Name': instance_name})

    # List RDS instances by tag or name
    rds_response = rds_client.describe_db_instances()
    rds_instances = []
    for db_instance in rds_response['DBInstances']:
        db_instance_id = db_instance['DBInstanceIdentifier']
        tags_response = rds_client.list_tags_for_resource(ResourceName=db_instance['DBInstanceArn'])
        if tag_contains_keyword(tags_response['TagList'], tag_keyword) or name_contains_keyword(db_instance_id, tag_keyword):
            rds_instances.append({'DBInstanceIdentifier': db_instance_id, 'Name': db_instance_id})

    # List Lambda functions by tag or name
    lambda_response = lambda_client.list_functions()
    lambda_functions = []
    for function in lambda_response['Functions']:
        tags_response = lambda_client.list_tags(Resource=function['FunctionArn'])
        function_name = function['FunctionName']
        if tag_contains_keyword(tags_response['Tags'], tag_keyword) or name_contains_keyword(function_name, tag_keyword):
            lambda_functions.append({'FunctionName': function_name, 'Name': function_name})

    # List ECR repositories by tag or name
    ecr_response = ecr_client.describe_repositories()
    ecr_repositories = []
    for repository in ecr_response['repositories']:
        tags_response = ecr_client.list_tags_for_resource(resourceArn=repository['repositoryArn'])
        repository_name = repository['repositoryName']
        if tag_contains_keyword(tags_response['tags'], tag_keyword) or name_contains_keyword(repository_name, tag_keyword):
            ecr_repositories.append({'RepositoryName': repository_name, 'Name': repository_name})

    # List ECS clusters by tag or name
    ecs_response = ecs_client.list_clusters()
    ecs_clusters = []
    for cluster_arn in ecs_response['clusterArns']:
        tags_response = ecs_client.list_tags_for_resource(resourceArn=cluster_arn)
        cluster_name = cluster_arn.split('/')[-1]
        if tag_contains_keyword(tags_response['tags'], tag_keyword) or name_contains_keyword(cluster_name, tag_keyword):
            ecs_clusters.append({'ClusterName': cluster_name, 'Name': cluster_name})

    # Print the results
    if ec2_instances:
        print(f"EC2 Instances with tag or name containing '{tag_keyword}':")
        for instance in ec2_instances:
            print(f"Instance ID: {instance['InstanceId']}, Name: {instance['Name']}")
    else:
        print(f"No EC2 instances found with tag or name containing '{tag_keyword}'.")

    if rds_instances:
        print(f"RDS Instances with tag or name containing '{tag_keyword}':")
        for instance in rds_instances:
            print(f"DBInstanceIdentifier: {instance['DBInstanceIdentifier']}, Name: {instance['Name']}")
    else:
        print(f"No RDS instances found with tag or name containing '{tag_keyword}'.")

    if lambda_functions:
        print(f"Lambda Functions with tag or name containing '{tag_keyword}':")
        for function in lambda_functions:
            print(f"Function Name: {function['FunctionName']}, Name: {function['Name']}")
    else:
        print(f"No Lambda functions found with tag or name containing '{tag_keyword}'.")

    if ecr_repositories:
        print(f"ECR Repositories with tag or name containing '{tag_keyword}':")
        for repository in ecr_repositories:
            print(f"Repository Name: {repository['RepositoryName']}, Name: {repository['Name']}")
    else:
        print(f"No ECR repositories found with tag or name containing '{tag_keyword}'.")

    if ecs_clusters:
        print(f"ECS Clusters with tag or name containing '{tag_keyword}':")
        for cluster in ecs_clusters:
            print(f"Cluster Name: {cluster['ClusterName']}, Name: {cluster['Name']}")
    else:
        print(f"No ECS clusters found with tag or name containing '{tag_keyword}'.")
