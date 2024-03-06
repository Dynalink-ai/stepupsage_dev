import subprocess
import threading

# Define the paths to the Python interpreters of your two virtual environments
# python_env1 = '/home/infeon/Projects/StepUpSage_FE/env/bin/python'  # Path to the Python interpreter in the first venv
python_env2 = '/home/infeon/Projects/stepupsage_dev/venv/bin/python'  # Path to the Python interpreter in the second venv

# List of script paths with their respective Python environment
scripts = [
    # (python_env1, 'main.py'),
    # (python_env1, 'json_extract.py'),
    # (python_env2, '/home/infeon/Projects/stepupsage_dev/backend1/json_deploy_approve.py'),
    # (python_env2, '/home/infeon/Projects/stepupsage_dev/backend1/json_process.py'),
    # (python_env2, '/home/infeon/Projects/stepupsage_dev/backend1/self_managed_check.py'),
    (python_env2, '/home/infeon/Projects/stepupsage_dev/backend2/config_runner.py'),
    (python_env2, '/home/infeon/Projects/stepupsage_dev/backend2/curl_test.py'),
]

def run_script(python_interpreter, script):
    """Run a script and print its output in real-time."""
    try:
        process = subprocess.Popen([python_interpreter, script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
        
        # Print stdout in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"{script} output: {output.strip()}")
                
        # Check if there's any stderr output
        stderr = process.stderr.read()
        if stderr:
            print(f"{script} error: {stderr.strip()}")
    except Exception as e:
        print(f"Failed to start {script}: {e}")

def main():
    threads = []
    for python_interpreter, script in scripts:
        thread = threading.Thread(target=run_script, args=(python_interpreter, script))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
