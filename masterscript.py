import subprocess

# List of Python scripts you want to run
scripts = [
    
    'python backend/backend2/config_runner.py',
    'python backend/backend2/curl_test.py',
    'python backend/backend1/json_process.py',
    'python backend/backend1/json_deploy_approve.py',
    'python backend/backend1/self_managed_check.py',
    'python frontend/userpage/main.py',
    'python frontend/userpage/json_extract.py']

for script in scripts:
    print(f"Running {script}...")
    subprocess.run(["python", script])

    # If you need to pass command-line arguments to your scripts, add them to the list like so:
    # subprocess.run(["python", script, "arg1", "arg2"])

print("All scripts executed successfully.")


# os.system("python backend/backend2/config_runner.py")
# os.system("python backend/backend2/curl_test.py")
# os.system("python backend/backend1/json_process.py")
# os.system("python backend/backend1/json_deploy_approve.py")
# os.system("python backend/backend1/self_managed_check.py")
# os.system("python frontend/userpage/main.py")
# os.system("python frontend/userpage/json_extract.py")