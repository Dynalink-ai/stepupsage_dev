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


def self_managed():
    print("Executing self_managed strategy...")

def process_file(file_path, save_dir):
    with open(file_path, 'r') as file:
        data = json.load(file)
        deploy_strategy = data.get('deploy_strategy', '').lower()
        
        if deploy_strategy in ['cloud-managed', 'cloud', 'cloud']:
            cloud_managed()
        elif deploy_strategy in ['self', 'self-managed', 'self']:
            self_managed()
        else:
            print("Unknown deploy strategy found.")

    # Wait for 10 seconds
    time.sleep(10)

    # Move the JSON file to deploy_confirm_save directory
    shutil.move(file_path, os.path.join(save_dir, os.path.basename(file_path)))
    print(f"Moved {file_path} to {save_dir}")

def main():
    source_dir = 'deploy_confirm'
    save_dir = 'deploy_confirm_save'

    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Created directory {save_dir}")

    # Process each JSON file in the source directory
    for file_name in os.listdir(source_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(source_dir, file_name)
            print(f"Processing {file_path}...")
            process_file(file_path, save_dir)
            break  # End the program after processing a single file

if __name__ == "__main__":
    main()
