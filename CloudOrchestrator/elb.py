import boto3

def list_load_balancers(profile_name):
    session = boto3.Session(profile_name=profile_name)
    elb = session.client('elb')
    response = elb.describe_load_balancers()
    return response.get('LoadBalancerDescriptions', [])

def create_load_balancer(profile_name, load_balancer_name, listeners, availability_zones):
    session = boto3.Session(profile_name=profile_name)
    elb = session.client('elb')
    response = elb.create_load_balancer(
        LoadBalancerName=load_balancer_name,
        Listeners=listeners,
        AvailabilityZones=availability_zones
    )
    return response

def delete_load_balancer(profile_name, load_balancer_name):
    session = boto3.Session(profile_name=profile_name)
    elb = session.client('elb')
    elb.delete_load_balancer(LoadBalancerName=load_balancer_name)
