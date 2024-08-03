import boto3

def list_parameters(profile_name):
    session = boto3.Session(profile_name=profile_name)
    ssm = session.client('ssm')
    response = ssm.describe_parameters()
    return response.get('Parameters', [])

def get_parameter(profile_name, name):
    session = boto3.Session(profile_name=profile_name)
    ssm = session.client('ssm')
    response = ssm.get_parameter(Name=name)
    return response['Parameter']

def put_parameter(profile_name, name, value, type):
    session = boto3.Session(profile_name=profile_name)
    ssm = session.client('ssm')
    ssm.put_parameter(Name=name, Value=value, Type=type)
