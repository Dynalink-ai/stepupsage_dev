import os
import time
import json
import shutil

def check_and_move_file(file_path, deploy_confirm_dir, deploy_save_dir):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Check if the "deployment" key exists and its value
            if data.get("deployment", "").lower() == "yes":
                # Move to /deploy_confirm
                shutil.move(file_path, os.path.join(deploy_confirm_dir, os.path.basename(file_path)))
                print(f"Moved to {deploy_confirm_dir}: {file_path}")
            else:
                # Move to /deploy_save
                shutil.move(file_path, os.path.join(deploy_save_dir, os.path.basename(file_path)))
                print(f"Moved to {deploy_save_dir}: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def main():
    json_dumps_dir = "json_dumps"
    deploy_confirm_dir = "deploy_confirm"
    deploy_save_dir = "deploy_save"

    while True:
        # List all JSON files in the /jsondumps directory
        for file_name in os.listdir(json_dumps_dir):
            if file_name.endswith('.json'):
                file_path = os.path.join(json_dumps_dir, file_name)
                check_and_move_file(file_path, deploy_confirm_dir, deploy_save_dir)
        
        # Wait for 15 seconds before the next scan
        time.sleep(15)

if __name__ == "__main__":
    main()
