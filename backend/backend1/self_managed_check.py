import boto3
import time

ec2 = boto3.client('ec2', region_name='ap-southeast-1')

def fetch_instance_details():
    response = ec2.describe_instances(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        },
    ])
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            public_ip_address = instance.get('PublicIpAddress')
            image_id = instance['ImageId']
            
            # Fetch the OS type based on the Image ID (This is a simplification. You might need a better logic here)
            image_details = ec2.describe_images(ImageIds=[image_id])
            platform_details = image_details['Images'][0].get('PlatformDetails', '')
            if 'Windows' in platform_details:
                ansible_user = 'Administrator'
            elif 'Ubuntu' or 'ubuntu' or 'Ubuntu (Inferred)' in platform_details:
                ansible_user = 'ubuntu'
            else:
                ansible_user = 'ec2-user'  # Default to ec2-user for Amazon Linux, RHEL, etc.
            
            return f'{public_ip_address} ansible_user="{ansible_user}" ansible_ssh_private_key_file="/home/infeon/Projects/stepupsage_dev/backend/backend2/ansible_scripts/keypairs/deploy.pem"'

    return None

def main():
    while True:
        details = fetch_instance_details()
        if details:
            with open('../../backend/backend2/ansible_scripts/hosts.ini', 'a') as file:
                file.write(f'\n{details}')
            print("Instance details appended to hosts.ini.")
            break
        else:
            print("No running instance found. Retrying in 60 seconds...")
            time.sleep(15)

if __name__ == "__main__":
    main()
