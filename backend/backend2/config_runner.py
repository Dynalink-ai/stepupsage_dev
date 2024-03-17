import time
import subprocess
import os
def get_file_line_count(filename):
    with open(filename, 'r') as file:
        return sum(1 for _ in file)

def run_ansible_playbook(playbook, inventory):
    command = ['sudo','ansible-playbook', '-i', inventory, playbook, "--ssh-extra-args='-o StrictHostKeyChecking=no'"]
    subprocess.run(command, check=True)

def monitor_file_for_changes(filename, interval=10):
    print(f"Monitoring {filename} for changes...")
    initial_line_count = get_file_line_count(filename)

    while True:
        time.sleep(interval)
        current_line_count = get_file_line_count(filename)

        if current_line_count > initial_line_count:
            print("New line detected! Running Ansible playbook...")
            run_ansible_playbook('ansible_scripts/deploy_app.yaml', 'ansible_scripts/hosts.ini')
            os.system('python curl_test.py')
            print("Ansible playbook has been executed. Exiting.")
            break

if __name__ == "__main__":
    try:
        monitor_file_for_changes('ansible_scripts/hosts.ini')
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
