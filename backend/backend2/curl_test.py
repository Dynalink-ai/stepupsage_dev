import subprocess
import time
import re
import os

# Path to your hosts.ini file
hosts_ini_path = "ansible_scripts/hosts.ini"

# Function to get IP address from the last line of the hosts.ini file
def get_ip_address(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            last_line = lines[-1]
            # Extract IP address using regular expression
            ip_address_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', last_line)
            if ip_address_match:
                return ip_address_match.group(1)
            else:
                raise ValueError("IP address not found in the last line.")
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    except Exception as e:
        raise e

# Function to check connectivity using wget
def check_connectivity(ip):
    try:
        result = subprocess.run(["wget", "--spider", f"http://{ip}:5000"], capture_output=True, text=True)
        return result.returncode == 0  # returncode 0 indicates success
    except Exception as e:
        print(f"An error occurred while checking connectivity: {e}")
        return False

def main():
    ip_address = get_ip_address(hosts_ini_path)
    if ip_address:
        while True:
            if check_connectivity(ip_address):
                # If successful, write the result to result.txt and end the program
                with open("result.txt", "w") as file:
                    file.write(f"Successfully reached {ip_address}:5000")
                print(f"Successfully reached {ip_address}:5000. Exiting.")
                os.system('python send_email.py')
                break
            else:
                print(f"Unable to reach {ip_address}:5000. Retrying in 15 seconds...")
                time.sleep(15)

if __name__ == "__main__":
    main()
