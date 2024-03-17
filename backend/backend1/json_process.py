import os
import json
import time
import shutil

def cloud_managed():
    print("Executing cloud_managed strategy...")
    os.chdir("terraform_script/cloud_managed/")
    os.system("terraform init")
    os.system("terraform plan")
    os.system("terraform apply -auto-approve")
    print("Service creation pending... running")

def self_managed():
    print("Executing self_managed strategy...")
    os.chdir("terraform_script/self_managed/")
    os.system("terraform init")
    os.system("terraform plan")
    os.system("terraform apply -auto-approve")
    print("Instance creation pending... running")

def process_file(file_path, destination_dir):
    with open(file_path, 'r') as file:
        data = json.load(file)
        deploy_strategy = data.get("deploy_strategy", "").lower()
        
        if deploy_strategy in ['cloud-managed', 'cloud', 'cloud']:
            cloud_managed()
        elif deploy_strategy in ['self', 'self-managed', 'self']:
            self_managed()
        else:
            print(f"Unknown deploy strategy: {deploy_strategy}")

    # Move the file to deploy_confirm_save directory after processing
    shutil.move(file_path, os.path.join(destination_dir, os.path.basename(file_path)))
    print(f"Moved {file_path} to {destination_dir}")

def main():
    source_dir = 'deploy_confirm/'
    destination_dir = 'deploy_confirm_save/'
    
    # Ensure the destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"Created directory {destination_dir}")
    
    while True:
        # Look for JSON files in the deploy_confirm directory
        for file_name in os.listdir(source_dir):
            if file_name.endswith('.json'):
                full_file_path = os.path.join(source_dir, file_name)
                print(f"Processing file: {full_file_path}")
                process_file(full_file_path, destination_dir)
                break  # Exit the loop after processing a file

        # Sleep for 10 seconds after processing a file, or immediately if no file was found
        time.sleep(10)

if __name__ == "__main__":
    main()