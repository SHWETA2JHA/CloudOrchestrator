import subprocess

def configure_aws(profile_name):
    subprocess.run(['aws', 'configure', 'set', 'aws_access_key_id', '--profile', profile_name], check=True)
    subprocess.run(['aws', 'configure', 'set', 'aws_secret_access_key', '--profile', profile_name], check=True)
    subprocess.run(['aws', 'configure', 'set', 'region', '--profile', profile_name], check=True)
