# this code to append multiple ec2 instances to the hosts.ini
import boto3

region = 'ap-south-1'
ec2 = boto3.client('ec2', region_name=region)

def fetch_instance_details():
    response = ec2.describe_instances(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        },
    ])
    
    with open('../backend2/ansible_scripts/hosts.ini', 'a') as file:  # 'a' mode to append
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                public_ip_address = instance.get('PublicIpAddress', 'No IP Address')  # Default value if no IP
                image_id = instance['ImageId']
                
                # Fetch the OS type based on the Image ID
                image_details = ec2.describe_images(ImageIds=[image_id])
                platform_details = image_details['Images'][0].get('PlatformDetails', 'Linux/UNIX')  # Default to Linux/UNIX
                
                if 'Windows' in platform_details:
                    ansible_user = 'Administrator'
                elif any(substring in platform_details for substring in ['Ubuntu', 'Linux/UNIX']):
                    ansible_user = 'ubuntu'
                else:
                    ansible_user = 'ec2-user'  # Default for other types
                
                # Write details to file with a newline
                file.write(f'{public_ip_address} ansible_user="{ansible_user}" ansible_ssh_private_key_file="/home/infeon/Projects/stepupsage_dev/backend2/ansible_scripts/keypairs/deploy.pem"\n')

print("Fetching instance details...")
fetch_instance_details()
print("Instance details appended to hosts.ini.")
