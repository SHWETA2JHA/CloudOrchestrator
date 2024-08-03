import boto3

def list_metrics(profile_name):
    session = boto3.Session(profile_name=profile_name)
    cloudwatch = session.client('cloudwatch')
    response = cloudwatch.list_metrics()
    return response.get('Metrics', [])

def put_metric_data(profile_name, namespace, metric_name, value):
    session = boto3.Session(profile_name=profile_name)
    cloudwatch = session.client('cloudwatch')
    cloudwatch.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value
            },
        ]
    )
