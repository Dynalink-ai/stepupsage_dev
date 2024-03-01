import boto3
import time
import os

time.sleep(15)
def find_instance_by_name(ec2, instance_name):
    instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Name', 'Values': [instance_name]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            return instance
    return None

def write_instance_details_to_file(instance, file_path):
    with open(file_path, 'w') as f:
        f.write(f"Instance ID: {instance['InstanceId']}\n")
        f.write(f"IP Address: {instance['PublicIpAddress']}\n")
    print(f"Details written to {file_path}")

def main():
    region = 'ap-southeast-1'
    instance_name = 'simpleflask_instance'
    destination_dir = '../backend2/be_dumps'
    file_name = 'instance_details.txt'
    file_path = os.path.join(destination_dir, file_name)

    ec2 = boto3.client('ec2', region_name=region)

    while True:
        instance = find_instance_by_name(ec2, instance_name)
        if instance:
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            write_instance_details_to_file(instance, file_path)
            break
        else:
            print(f"Instance '{instance_name}' not available. Retrying in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    main()
