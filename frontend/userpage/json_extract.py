import os
import json
import time
import shutil
import sys  # Import sys for exiting the script

def find_json_string(content):
    try:
        start_index = content.index('{')
        end_index = content.rindex('}') + 1
        return content[start_index:end_index]
    except ValueError:
        return None

def process_file(file_path, destination_dir):
    with open(file_path, 'r') as file:
        content = file.read()
        json_string = find_json_string(content)
        if json_string:
            try:
                json_object = json.loads(json_string)
                new_file_path = file_path.replace('.txt', '.json')
                with open(new_file_path, 'w') as json_file:
                    json.dump(json_object, json_file, indent=4)
                print(f'JSON extracted and saved to {new_file_path}')
                
                # Move the .json file to the destination directory
                shutil.move(new_file_path, os.path.join(destination_dir, os.path.basename(new_file_path)))
                print(f'Moved {new_file_path} to {destination_dir}')
                return True  # Return True to indicate the file has been processed and moved
                
            except json.JSONDecodeError as e:
                print(f'Error decoding JSON from file {file_path}: {e}')
            except Exception as e:
                print(f'An error occurred: {e}')
    return False  # Return False if no JSON file was processed

def main():
    path = '.'  # Current directory
    destination_dir = '../../backend/backend1/json_dumps'  # Destination directory for json
    
    # Ensure the destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f'Created directory {destination_dir}')
    
    while True:
        for file_name in os.listdir(path):
            if file_name.endswith('.txt'):
                full_file_path = os.path.join(path, file_name)
                if process_file(full_file_path, destination_dir):
                    print("Exiting the script after processing a file.")
                    sys.exit()  # Exit the script after a file has been processed and moved
        
        # Wait for 15 seconds before the next scan
        time.sleep(15)

if __name__ == "__main__":
    main()
