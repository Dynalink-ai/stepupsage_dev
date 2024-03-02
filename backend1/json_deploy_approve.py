import os
import time
import json
import shutil
import sys  # Import sys module to use sys.exit()

def check_and_move_file(file_path, deploy_confirm_dir, deploy_save_dir):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if data.get("deploy", "").lower() == "yes":
                shutil.move(file_path, os.path.join(deploy_confirm_dir, os.path.basename(file_path)))
                print(f"Moved to {deploy_confirm_dir}: {file_path}")
                return True  # Indicate that a file has been moved
            else:
                shutil.move(file_path, os.path.join(deploy_save_dir, os.path.basename(file_path)))
                print(f"Moved to {deploy_save_dir}: {file_path}")
                return True  # Indicate that a file has been moved
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return False  # Indicate that no file has been moved

def main():
    json_dumps_dir = "json_dumps/"
    deploy_confirm_dir = "deploy_confirm/"
    deploy_save_dir = "deploy_save/"

    while True:
        moved = False  # Initialize the flag as False
        for file_name in os.listdir(json_dumps_dir):
            if file_name.endswith('.json'):
                file_path = os.path.join(json_dumps_dir, file_name)
                # If a file is moved, stop the loop and exit
                if check_and_move_file(file_path, deploy_confirm_dir, deploy_save_dir):
                    moved = True
                    break  # Exit the for loop
        
        if moved:
            print("Exiting the script.")
            sys.exit()  # Exit the script
        
        # Wait for 15 seconds before the next scan
        time.sleep(15)

if __name__ == "__main__":
    main()
