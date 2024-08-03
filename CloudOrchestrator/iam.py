import boto3

def list_users(profile_name):
    session = boto3.Session(profile_name=profile_name)
    iam = session.client('iam')
    response = iam.list_users()
    return response.get('Users', [])

def create_user(profile_name, user_name):
    session = boto3.Session(profile_name=profile_name)
    iam = session.client('iam')
    response = iam.create_user(UserName=user_name)
    return response['User']

def delete_user(profile_name, user_name):
    session = boto3.Session(profile_name=profile_name)
    iam = session.client('iam')
    iam.delete_user(UserName=user_name)
