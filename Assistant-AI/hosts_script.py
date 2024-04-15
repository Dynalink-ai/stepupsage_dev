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
    #instance_ips=[]
    # fe_details=[]
    #Clear the contents of the file
    open('../hosts3.ini', 'w').close()

    with open('../hosts3.ini', 'r') as file:
        existing_lines = file.readlines()

    with open('../hosts3.ini', 'a') as file:  # 'a' mode to append
        
        file.write("[web_server_fe]\n")
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                        if 'fe' in instance_name:
                            fe_public_ip_address = instance.get('PublicIpAddress', 'No IP Address')
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
                            #file.write("[web_server_fe]\n\n")
                            # Write details to file with a newline
                            # with open('../hosts3.ini', 'r') as file2:
                            #     lines = file2.readlines()
                                    
                            #     for line in lines:
                            #         if '[web_server_fe]' in line:
                                            
                            #             break
                            new_line = f'{fe_public_ip_address} ansible_user="{ansible_user}" ansible_ssh_private_key_file="/home/infeon/Projects/stepupsage_dev/backend2/ansible_scripts/keypairs/deploy.pem"\n'
                            if new_line not in existing_lines:
                                file.write(new_line)
                                ##instance_ips.append(public_ip_address)
                                print("Fetching instance details...")
                                print("Frontend Instance details appending to hosts3.ini.")
                            # file.write(f'{be_public_ip_address} ansible_user="{ansible_user}" ansible_ssh_private_key_file="/home/infeon/Projects/stepupsage_dev/backend2/ansible_scripts/keypairs/deploy.pem"\n')
                                # print("Fetching instance details...")
                                # print("Backend Instance details appending to hosts.ini.")
        file.write("\n[web_server_be]\n")
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                        if 'be' in instance_name:
                            be_public_ip_address = instance.get('PublicIpAddress', 'No IP Address')
                            be_image_id = instance['ImageId']

                            # Fetch the OS type based on the Image ID
                            be_image_details = ec2.describe_images(ImageIds=[be_image_id])
                            be_platform_details = be_image_details['Images'][0].get('PlatformDetails', 'Linux/UNIX')  # Default to Linux/UNIX
                
                            if 'Windows' in be_platform_details:
                                ansible_user = 'Administrator'
                            elif any(substring in be_platform_details for substring in ['Ubuntu', 'Linux/UNIX']):
                                ansible_user = 'ubuntu'
                            else:
                                ansible_user = 'ec2-user'  # Default for other types
                            # with open('../hosts3.ini', 'r') as file2:
                            #     lines = file2.readlines()
                                
                            #     for line in lines:
                            #         if '[web_server_be]' in line:
                                        
                            #             break
                            new_line = f'{be_public_ip_address} ansible_user="{ansible_user}" ansible_ssh_private_key_file="/home/infeon/Projects/stepupsage_dev/backend2/ansible_scripts/keypairs/deploy.pem"\n'
                            if new_line not in existing_lines:
                                file.write(new_line)
                                ##instance_ips.append(public_ip_address)
                                print("Fetching instance details...")
                                print("Backend Instance details appending to hosts3.ini.")                        
                            # file.write(f'{be_public_ip_address} ansible_user="{ansible_user}" ansible_ssh_private_key_file="/home/infeon/Projects/stepupsage_dev/backend2/ansible_scripts/keypairs/deploy.pem"\n')
                            # print("Fetching instance details...")
                            # print("Backend Instance details appending to hosts.ini.")


fetch_instance_details()
