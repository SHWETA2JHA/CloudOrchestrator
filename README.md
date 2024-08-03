# CloudOrchestrator

**CloudOrchestrator** is an all-in-one command-line interface (CLI) tool designed to streamline the management of various AWS resources and Docker operations. Built with simplicity and efficiency in mind, CloudOrchestrator empowers developers, system administrators, and DevOps professionals to perform complex cloud operations seamlessly from their terminal.

### Key Features

1. **EC2 Management**: Start, stop, and execute commands on EC2 instances effortlessly. Manage instance states and access instances through SSH with ease.

2. **RDS Management**: Start and stop RDS instances and list all your database instances to ensure optimal database operations.

3. **Route53 Management**: Handle DNS records within your Route53 hosted zones, enabling smooth domain management and traffic routing.

4. **Lambda Management**: Deploy and manage AWS Lambda functions to run code in response to events without provisioning or managing servers.

5. **ECR Management**: List, create, delete, and describe Elastic Container Registry repositories, and retrieve repository URIs for Docker image storage and deployment.

6. **S3 Management**: Create, list, and delete S3 buckets and objects to manage your cloud storage needs effectively.

7. **Docker Management**: Run, stop, list, and manage Docker containers locally or on remote hosts, facilitating containerized application deployment and maintenance.

8. **SNS Management**: Create and delete SNS topics, and list existing topics to manage your message notification system.

9. **IAM Management**: Create and delete IAM users, and list all users to manage access to your AWS resources securely.

10. **CloudWatch Management**: List CloudWatch metrics and put custom metrics for monitoring and observability of your AWS resources.

11. **DynamoDB Management**: Create, list, and delete DynamoDB tables to handle your NoSQL database requirements.

12. **SSM Management**: Manage AWS Systems Manager parameters, including listing, getting, and putting parameters for configuration management.

13. **ELB Management**: Create, list, and delete Elastic Load Balancers to distribute incoming traffic across multiple targets.

### Why CloudOrchestrator?

- **Unified Interface**: Manage a broad range of AWS services and Docker from a single tool, reducing the need to switch between different interfaces.
- **Ease of Use**: Simple commands and clear syntax make it accessible for both beginners and experienced professionals.
- **Automation Ready**: Ideal for scripting and automation, allowing you to incorporate cloud management tasks into your CI/CD pipelines.
- **Flexibility**: Supports multiple AWS accounts and provides an easy way to add and manage them.
- **Security**: Prompts for the PEM file path for SSH operations, ensuring secure access to your EC2 instances.

CloudOrchestrator is designed to be your go-to tool for cloud and container management, making your operations smoother, more efficient, and less time-consuming. Whether you're deploying new applications, scaling existing ones, or maintaining your infrastructure, CloudOrchestrator provides the tools you need to succeed.


## Installation

```bash
pip install boto3
pip install paramiko
pip install .
```

## Usage

### Initialize the Config
```bash
cloudorchestrator initialize
```

### Add AWS Account
```bash
cloudorchestrator add-account
```

### EC2
```bash
cloudorchestrator ec2 start <instance_name>
cloudorchestrator ec2 stop <instance_name>
cloudorchestrator ec2 ssh <instance_name> <command>
```

### ECR
```bash
cloudorchestrator ecr-ls
cloudorchestrator ecr-create <repository_name>
cloudorchestrator ecr-delete <repository_name>
cloudorchestrator ecr-describe <repository_name>
cloudorchestrator ecr-uri <repository_name>
```

### S3
```bash
cloudorchestrator s3-ls
cloudorchestrator s3-create <bucket_name>
cloudorchestrator s3-delete <bucket_name>
```

### RDS
```bash
cloudorchestrator rds start <db_instance_identifier>
cloudorchestrator rds stop <db_instance_identifier>
cloudorchestrator rds-ls
```

### Docker
```bash
cloudorchestrator docker ls
cloudorchestrator docker ps
cloudorchestrator docker stop <container_id>
cloudorchestrator docker sh <container_id>
cloudorchestrator docker run <port1> <port2> <image_name>
```

### SNS
```bash
cloudorchestrator sns list
cloudorchestrator sns create <topic_name>
cloudorchestrator sns delete <topic_arn>
```

### IAM
```bash
cloudorchestrator iam list
cloudorchestrator iam create <user_name>
cloudorchestrator iam delete <user_name>
```

### CloudWatch
```bash
cloudorchestrator cloudwatch list
cloudorchestrator cloudwatch put <namespace> <metric_name> <value>
```

### DynamoDB
```bash
cloudorchestrator dynamodb list
cloudorchestrator dynamodb create <table_name> <key_schema> <attribute_definitions> <provisioned_throughput>
cloudorchestrator dynamodb delete <table_name>
```

### SSM
```bash
cloudorchestrator ssm list
cloudorchestrator ssm get <name>
cloudorchestrator ssm put <name> <value> <type>
```

### ELB
```bash
cloudorchestrator elb list
cloudorchestrator elb create <load_balancer_name> <listeners> <availability_zones>
cloudorchestrator elb delete <load_balancer_name>
```

### Deploy
```bash
cloudorchestrator deploy <profile_name> <resource_name> <folder_path>
```

### Tag
```bash
cloudorchestrator <tag_keyword> ls
```

