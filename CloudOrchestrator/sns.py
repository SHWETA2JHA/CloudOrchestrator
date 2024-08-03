import boto3

def list_topics(profile_name):
    session = boto3.Session(profile_name=profile_name)
    sns = session.client('sns')
    response = sns.list_topics()
    return response.get('Topics', [])

def create_topic(profile_name, name):
    session = boto3.Session(profile_name=profile_name)
    sns = session.client('sns')
    response = sns.create_topic(Name=name)
    return response['TopicArn']

def delete_topic(profile_name, topic_arn):
    session = boto3.Session(profile_name=profile_name)
    sns = session.client('sns')
    sns.delete_topic(TopicArn=topic_arn)
