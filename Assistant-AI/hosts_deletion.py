import boto3
import configparser

# Initialize boto3 client for EC2
ec2 = boto3.client('ec2', region_name='your-region', aws_access_key_id='your-access-key', aws_secret_access_key='your-secret-key')

# Get the status of the instance
response = ec2.describe_instance_status(InstanceIds=['your-instance-id'])

# Read the hosts.ini file
config = configparser.ConfigParser()
config.read('hosts.ini')

# Check if the instance is running
if response['InstanceStatuses'] and response['InstanceStatuses'][0]['InstanceState']['Name'] != 'running':
    # If the instance is not running, delete it from the hosts.ini file
    # Check if the 'webserver' section exists
    if 'webserver' in config.sections():
        # Check if the host exists in the 'webserver' section
        if 'your-host-name' in config['webserver']:
            # Delete the host
            config.remove_option('webserver', 'your-host-name')
            # Write the updated configuration back to the hosts.ini file
            with open('hosts.ini', 'w') as configfile:
                config.write(configfile)