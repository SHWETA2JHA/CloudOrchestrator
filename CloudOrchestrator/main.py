import sys
from CloudOrchestrator.config import initialize_config, add_aws_account, list_instances, list_s3_buckets
from CloudOrchestrator.ec2 import start_ec2_instance, stop_ec2_instance
from CloudOrchestrator.ecr import list_ecr_repositories, create_ecr_repository, delete_ecr_repository, describe_ecr_repository, get_ecr_repository_uri
from CloudOrchestrator.s3 import list_s3_buckets, create_s3_bucket, delete_s3_bucket
from CloudOrchestrator.ssh import ssh_ec2_instance
from CloudOrchestrator.rds import start_rds_instance, stop_rds_instance, list_rds_instances
from CloudOrchestrator.tags import list_resources_by_tag
from CloudOrchestrator.deploy import deploy_existing, deploy_new, deploy_cli  
from CloudOrchestrator.docker import docker_ls, docker_ps, docker_stop, docker_sh, docker_run
from CloudOrchestrator.config import load_config, save_config 
from CloudOrchestrator.deploy import get_aws_clients
from CloudOrchestrator.route53 import list_records, create_record, delete_record
from CloudOrchestrator.sns import list_topics, create_topic, delete_topic
from CloudOrchestrator.iam import list_users, create_user, delete_user
from CloudOrchestrator.cloudwatch import list_metrics, put_metric_data
from CloudOrchestrator.dynamodb import list_tables, create_table, delete_table
from CloudOrchestrator.ssm import list_parameters, get_parameter, put_parameter
from CloudOrchestrator.elb import list_load_balancers, create_load_balancer, delete_load_balancer

def main():
    if len(sys.argv) < 2:
        print("Usage: CloudOrchestrator <command> [options]")
        return
    command = sys.argv[1]
    if command == 'initialize':
        initialize_config()
    elif command == 'add-account':
        add_account_cli()
    elif command == 'list-instances':
        list_instances_cli()
    elif command == 'ec2':
        ec2_cli()
    elif command == 'ecr-ls':
        list_ecr_cli()
    elif command == 'ecr-create':
        create_ecr_cli()
    elif command == 'ecr-delete':
        delete_ecr_cli()
    elif command == 'ecr-describe':
        describe_ecr_cli()
    elif command == 'ecr-uri':
        ecr_uri_cli()
    elif command == 's3-ls':
        list_s3_cli()
    elif command == 's3-create':
        create_s3_cli()
    elif command == 's3-delete':
        delete_s3_cli()
    elif command == 'ec2-ssh':
        ec2_ssh_cli()
    elif command == 'rds':
        rds_cli()
    elif command == 'rds-ls':
        list_rds_cli()
    elif command == 'deploy':
        deploy_lambda_cli() 
    elif command == 'docker':
        docker_cli()
    elif command == 'sns':
        sns_cli()
    elif command == 'iam':
        iam_cli()
    elif command == 'cloudwatch':
        cloudwatch_cli()
    elif command == 'dynamodb':
        dynamodb_cli()
    elif command == 'ssm':
        ssm_cli()
    elif command == 'elb':
        elb_cli()
    else:
        tag_cli(command)

def add_account_cli():
    profile_name = input("Enter profile name: ")
    access_key = input("Enter AWS Access Key: ")
    secret_key = input("Enter AWS Secret Key: ")
    region = input("Enter AWS Region: ")
    add_aws_account(profile_name, access_key, secret_key, region)

def list_instances_cli():
    profile_name = input("Enter profile name: ")
    list_instances(profile_name)

def ec2_cli():
    if len(sys.argv) < 4:
        print("Usage: CloudOrchestrator ec2 <start/stop/ssh> <instance_name> [command]")
        return
    subcommand = sys.argv[2]
    instance_name = sys.argv[3]
    profile_name = input("Enter profile name: ")  # Prompt for profile name
    if subcommand == 'start':
        start_ec2_instance(profile_name, instance_name)
    elif subcommand == 'stop':
        stop_ec2_instance(profile_name, instance_name)
    elif subcommand == 'ssh':
        if len(sys.argv) < 5:
            print("Usage: CloudOrchestrator ec2 ssh <instance_name> <command>")
            return
        ssh_command = sys.argv[4]
        ssh_ec2_instance(profile_name, instance_name, ssh_command)
    else:
        print(f"Unknown subcommand: {subcommand}")

def list_ecr_cli():
    profile_name = input("Enter profile name: ")
    repositories = list_ecr_repositories(profile_name)
    if repositories:
        print("ECR Repositories:")
        for repo in repositories:
            print(repo['RepositoryName'])
    else:
        print("No ECR repositories found.")

def create_ecr_cli():
    profile_name = input("Enter profile name: ")
    repository_name = input("Enter ECR repository name: ")
    create_ecr_repository(profile_name, repository_name)

def delete_ecr_cli():
    profile_name = input("Enter profile name: ")
    repository_name = input("Enter ECR repository name: ")
    delete_ecr_repository(profile_name, repository_name)

def describe_ecr_cli():
    profile_name = input("Enter profile name: ")
    repository_name = input("Enter ECR repository name: ")
    describe_ecr_repository(profile_name, repository_name)

def ecr_uri_cli():
    profile_name = input("Enter profile name: ")
    repository_name = input("Enter ECR repository name: ")
    uri = get_ecr_repository_uri(profile_name, repository_name)
    print(f"ECR Repository URI for '{repository_name}': {uri}")

def list_s3_cli():
    profile_name = input("Enter profile name: ")
    buckets = list_s3_buckets(profile_name)
    if buckets:
        print(f"S3 Buckets in profile '{profile_name}':")
        for bucket in buckets:
            print(bucket)
    else:
        print(f"No S3 buckets found in profile '{profile_name}'.")

def create_s3_cli():
    profile_name = input("Enter profile name: ")
    bucket_name = input("Enter S3 bucket name: ")
    create_s3_bucket(bucket_name)

def delete_s3_cli():
    profile_name = input("Enter profile name: ")
    bucket_name = input("Enter S3 bucket name: ")
    delete_s3_bucket(bucket_name)

def ec2_ssh_cli():
    if len(sys.argv) < 4:
        print("Usage: CloudOrchestrator ec2-ssh <instance_name> <command>")
        return
    instance_name = sys.argv[2]
    ssh_command = sys.argv[3]
    profile_name = input("Enter profile name: ")
    ssh_ec2_instance(profile_name, instance_name, ssh_command)

def rds_cli():
    if len(sys.argv) < 4:
        print("Usage: CloudOrchestrator rds <start/stop> <db_instance_identifier>")
        return
    subcommand = sys.argv[2]
    db_instance_identifier = sys.argv[3]
    profile_name = input("Enter profile name: ")
    if subcommand == 'start':
        start_rds_instance(profile_name, db_instance_identifier)
    elif subcommand == 'stop':
        stop_rds_instance(profile_name, db_instance_identifier)
    else:
        print(f"Unknown RDS subcommand: {subcommand}")

def list_rds_cli():
    profile_name = input("Enter profile name: ")
    list_rds_instances(profile_name)

def tag_cli(tag_keyword):
    if len(sys.argv) < 2:
        print("Usage: CloudOrchestrator <tag_keyword> ls")
        return
    profile_name = input("Enter profile name: ")
    list_resources_by_tag(profile_name, tag_keyword)

def deploy_lambda_cli():
    profile_name = sys.argv[2]
    resource_name = sys.argv[3]
    folder_path = sys.argv[4]
    deploy_cli(profile_name,resource_name,folder_path)

def docker_cli():
    if len(sys.argv) < 3:
        print("Usage: CloudOrchestrator docker <command> [options]")
        return
    subcommand = sys.argv[2]

    if subcommand == 'ls':
        docker_ls()
    elif subcommand == 'ps':
        docker_ps()
    elif subcommand == 'stop':
        if len(sys.argv) < 4:
            print("Usage: CloudOrchestrator docker stop <container_id>")
            return
        container_id = sys.argv[3]
        docker_stop(container_id)
    elif subcommand == 'sh':
        if len(sys.argv) < 4:
            print("Usage: CloudOrchestrator docker sh <container_id>")
            return
        container_id = sys.argv[3]
        docker_sh(container_id)
    elif subcommand == 'run':
        if len(sys.argv) < 6:
            print("Usage: CloudOrchestrator docker run <port1> <port2> <image_name>")
            return
        port1 = sys.argv[3]
        port2 = sys.argv[4]
        image_name = sys.argv[5]
        docker_run(port1, port2, image_name)
    else:
        print(f"Unknown Docker subcommand: {subcommand}")

def sns_cli():
    if len(sys.argv) < 3:
        print("Usage: CloudOrchestrator sns <list/create/delete> [options]")
        return
    subcommand = sys.argv[2]

    profile_name = input("Enter profile name: ")

    if subcommand == 'list':
        topics = list_topics(profile_name)
        if topics:
            print("SNS Topics:")
            for topic in topics:
                print(topic['TopicArn'])
        else:
            print("No SNS topics found.")
    elif subcommand == 'create':
        topic_name = input("Enter topic name: ")
        topic_arn = create_topic(profile_name, topic_name)
        print(f"Created topic with ARN: {topic_arn}")
    elif subcommand == 'delete':
        topic_arn = input("Enter topic ARN: ")
        delete_topic(profile_name, topic_arn)
        print(f"Deleted topic with ARN: {topic_arn}")
    else:
        print(f"Unknown SNS subcommand: {subcommand}")

def iam_cli():
    if len(sys.argv) < 3:
        print("Usage: CloudOrchestrator iam <list/create/delete> [options]")
        return
    subcommand = sys.argv[2]

    profile_name = input("Enter profile name: ")

    if subcommand == 'list':
        users = list_users(profile_name)
        if users:
            print("IAM Users:")
            for user in users:
                print(user['UserName'])
        else:
            print("No IAM users found.")
    elif subcommand == 'create':
        user_name = input("Enter user name: ")
        user = create_user(profile_name, user_name)
        print(f"Created user: {user['UserName']}")
    elif subcommand == 'delete':
        user_name = input("Enter user name: ")
        delete_user(profile_name, user_name)
        print(f"Deleted user: {user_name}")
    else:
        print(f"Unknown IAM subcommand: {subcommand}")

def cloudwatch_cli():
    if len(sys.argv) < 3:
        print("Usage: CloudOrchestrator cloudwatch <list/put> [options]")
        return
    subcommand = sys.argv[2]

    profile_name = input("Enter profile name: ")

    if subcommand == 'list':
        metrics = list_metrics(profile_name)
        if metrics:
            print("CloudWatch Metrics:")
            for metric in metrics:
                print(metric)
        else:
            print("No CloudWatch metrics found.")
    elif subcommand == 'put':
        namespace = input("Enter namespace: ")
        metric_name = input("Enter metric name: ")
        value = float(input("Enter value: "))
        put_metric_data(profile_name, namespace, metric_name, value)
        print(f"Put metric data: {metric_name} with value {value} in namespace {namespace}")
    else:
        print(f"Unknown CloudWatch subcommand: {subcommand}")

def dynamodb_cli():
    if len(sys.argv) < 3:
        print("Usage: CloudOrchestrator dynamodb <list/create/delete> [options]")
        return
    subcommand = sys.argv[2]

    profile_name = input("Enter profile name: ")

    if subcommand == 'list':
        tables = list_tables(profile_name)
        if tables:
            print("DynamoDB Tables:")
            for table in tables:
                print(table)
        else:
            print("No DynamoDB tables found.")
    elif subcommand == 'create':
        table_name = input("Enter table name: ")
        key_schema = eval(input("Enter key schema as list of dicts: "))
        attribute_definitions = eval(input("Enter attribute definitions as list of dicts: "))
        provisioned_throughput = eval(input("Enter provisioned throughput as dict: "))
        table = create_table(profile_name, table_name, key_schema, attribute_definitions, provisioned_throughput)
        print(f"Created table: {table['TableName']}")
    elif subcommand == 'delete':
        table_name = input("Enter table name: ")
        delete_table(profile_name, table_name)
        print(f"Deleted table: {table_name}")
    else:
        print(f"Unknown DynamoDB subcommand: {subcommand}")

def ssm_cli():
    if len(sys.argv) < 3:
        print("Usage: CloudOrchestrator ssm <list/get/put> [options]")
        return
    subcommand = sys.argv[2]

    profile_name = input("Enter profile name: ")

    if subcommand == 'list':
        parameters = list_parameters(profile_name)
        if parameters:
            print("SSM Parameters:")
            for param in parameters:
                print(param['Name'])
        else:
            print("No SSM parameters found.")
    elif subcommand == 'get':
        name = input("Enter parameter name: ")
        parameter = get_parameter(profile_name, name)
        print(f"Parameter: {parameter['Name']}, Value: {parameter['Value']}")
    elif subcommand == 'put':
        name = input("Enter parameter name: ")
        value = input("Enter parameter value: ")
        type = input("Enter parameter type (String, StringList, SecureString): ")
        put_parameter(profile_name, name, value, type)
        print(f"Put parameter: {name}")
    else:
        print(f"Unknown SSM subcommand: {subcommand}")

def elb_cli():
    if len(sys.argv) < 3:
        print("Usage: CloudOrchestrator elb <list/create/delete> [options]")
        return
    subcommand = sys.argv[2]

    profile_name = input("Enter profile name: ")

    if subcommand == 'list':
        load_balancers = list_load_balancers(profile_name)
        if load_balancers:
            print("Elastic Load Balancers:")
            for lb in load_balancers:
                print(lb['LoadBalancerName'])
        else:
            print("No Elastic Load Balancers found.")
    elif subcommand == 'create':
        load_balancer_name = input("Enter load balancer name: ")
        listeners = eval(input("Enter listeners as list of dicts: "))
        availability_zones = eval(input("Enter availability zones as list: "))
        load_balancer = create_load_balancer(profile_name, load_balancer_name, listeners, availability_zones)
        print(f"Created load balancer: {load_balancer_name}")
    elif subcommand == 'delete':
        load_balancer_name = input("Enter load balancer name: ")
        delete_load_balancer(profile_name, load_balancer_name)
        print(f"Deleted load balancer: {load_balancer_name}")
    else:
        print(f"Unknown ELB subcommand: {subcommand}")

if __name__ == "__main__":
    main()
