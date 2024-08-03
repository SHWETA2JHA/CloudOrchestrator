import boto3

def list_tables(profile_name):
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb')
    response = dynamodb.list_tables()
    return response.get('TableNames', [])

def create_table(profile_name, table_name, key_schema, attribute_definitions, provisioned_throughput):
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb')
    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput
    )
    return response['TableDescription']

def delete_table(profile_name, table_name):
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb')
    dynamodb.delete_table(TableName=table_name)
