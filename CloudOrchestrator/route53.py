from .config import get_route53_client

def list_records(profile_name, hosted_zone_id):
    client = get_route53_client(profile_name)
    response = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    for record_set in response['ResourceRecordSets']:
        print(record_set)

def create_record(profile_name, hosted_zone_id, name, record_type, ttl, values):
    client = get_route53_client(profile_name)
    change_batch = {
        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': name,
                    'Type': record_type,
                    'TTL': ttl,
                    'ResourceRecords': [{'Value': value} for value in values]
                }
            }
        ]
    }
    response = client.change_resource_record_sets(HostedZoneId=hosted_zone_id, ChangeBatch=change_batch)
    print(response)

def delete_record(profile_name, hosted_zone_id, name, record_type, values):
    client = get_route53_client(profile_name)
    change_batch = {
        'Changes': [
            {
                'Action': 'DELETE',
                'ResourceRecordSet': {
                    'Name': name,
                    'Type': record_type,
                    'ResourceRecords': [{'Value': value} for value in values]
                }
            }
        ]
    }
    response = client.change_resource_record_sets(HostedZoneId=hosted_zone_id, ChangeBatch=change_batch)
    print(response)
