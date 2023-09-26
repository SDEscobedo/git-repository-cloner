import json
import subprocess
import os

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

CONFIG_FILE = "config.json"

def is_repo_cloned(repo_path, expected_remote_url):
    # Check if the directory exists
    if not os.path.exists(repo_path):
        return False
    
    # Check if it's a Git repository
    try:
        # Use git remote to get the repository's remote URL
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            remote_url = result.stdout.strip()
            return remote_url == expected_remote_url
    except subprocess.CalledProcessError:
        pass  # Ignore Git errors

    return False

def colored_print(message, color=RESET):
    print(f"{color}{message}{RESET}")

def update_config(output_folder=None, input_json_file=None):
    # Load the existing configuration
    try:
        with open(CONFIG_FILE, 'r') as cf:
            config = json.load(cf)
    except FileNotFoundError:
        config = {}

    # Update the configuration based on user input
    if output_folder is not None:
        config["output_folder"] = output_folder
    if input_json_file is not None:
        config["input_json_file"] = input_json_file

    # Save the updated configuration
    with open(CONFIG_FILE, 'w') as cf:
        json.dump(config, cf, indent=4)

    colored_print("Configuration updated.", GREEN)

def check_cloned_repositories():
    # Load the config file to get the output folder and input JSON file path
    with open(CONFIG_FILE, 'r') as cf:
        config = json.load(cf)
        output_folder = config.get('output_folder')
        input_json_file = config.get('input_json_file')

    if not output_folder:
        colored_print("Error: 'output_folder' not found in the config file.", RED)
        return
    if not input_json_file:
        colored_print("Error: 'input_json_file' not found in the config file.", RED)
        return

    # Load the JSON file containing repository information
    with open(input_json_file, 'r') as f:
        repos = json.load(f)

    colored_print("Checking cloned repositories:")
    for repo in repos:
        repo_name = repo.get('name')
        repo_url = repo.get('url')
        if repo_name and repo_url:
            repo_path = os.path.join(output_folder, repo_name)

            if is_repo_cloned(repo_path, repo_url):
                colored_print(f"Repository {repo_name} is already cloned with matching remote URL.", GREEN)
            else:
                colored_print(f"Repository {repo_name} is not cloned.", YELLOW)

def clone_repositories():
    # Load the config file to get the output folder and input JSON file path
    with open(CONFIG_FILE, 'r') as cf:
        config = json.load(cf)
        output_folder = config.get('output_folder')
        input_json_file = config.get('input_json_file')

    if not output_folder:
        colored_print("Error: 'output_folder' not found in the config file.", RED)
        return
    if not input_json_file:
        colored_print("Error: 'input_json_file' not found in the config file.", RED)
        return

    # Load the JSON file containing repository information
    with open(input_json_file, 'r') as f:
        repos = json.load(f)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    colored_print("Cloning repositories:")
    for repo in repos:
        repo_name = repo.get('name')
        repo_url = repo.get('url')
        if repo_name and repo_url:
            repo_path = os.path.join(output_folder, repo_name)

            if is_repo_cloned(repo_path, repo_url):
                colored_print(f"Repository {repo_name} is already cloned with matching remote URL. Skipping.", YELLOW)
            else:
                # Clone the repository using the git command
                try:
                    subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
                    colored_print(f"Cloned {repo_name} successfully.", GREEN)
                except subprocess.CalledProcessError:
                    colored_print(f"Failed to clone {repo_name}.", RED)

def extract_repositories(output_folder, output_json_file):
    output_data = []
    
    # Get the absolute path of the output_folder
    output_folder = os.path.abspath(output_folder)

    for root, dirs, files in os.walk(output_folder):
        if ".git" in dirs:
            # This directory contains a .git subdirectory, indicating it's a Git repository
            repo_name = os.path.relpath(root, output_folder)
            repo_path = os.path.join(root, ".git")

            try:
                result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:
                    remote_url = result.stdout.strip()
                    repo_info = {"name": repo_name, "url": remote_url}
                    output_data.append(repo_info)
            except subprocess.CalledProcessError:
                pass  # Ignore Git errors

    with open(output_json_file, 'w') as f:
        json.dump(output_data, f, indent=4)

    colored_print(f"Repositories extracted and saved to {output_json_file}.", GREEN)

def check_repo_status():
    # Load the config file to get the input JSON file path
    with open(CONFIG_FILE, 'r') as cf:
        config = json.load(cf)
        input_json_file = config.get('input_json_file')

    if not input_json_file:
        colored_print("Error: 'input_json_file' not found in the config file.", RED)
        return

    # Load the JSON file containing repository information
    with open(input_json_file, 'r') as f:
        repos = json.load(f)

    colored_print("Checking Git repository status:")
    for repo in repos:
        repo_name = repo.get('name')
        repo_path = os.path.join(config.get('output_folder', ''), repo_name)

        if repo_name:
            try:
                result = subprocess.run(['git', 'status'], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                status_message = result.stdout.strip()
                
                # Check for common status keywords or phrases
                if any(keyword in status_message.lower() for keyword in ["nothing to commit", "nada para hacer commit"]):
                    colored_print(f"Repository {repo_name}: {status_message}", GREEN)
                elif "Changes not staged for commit" in status_message:
                    colored_print(f"Repository {repo_name}: {status_message}", YELLOW)
                else:
                    colored_print(f"Repository {repo_name}: {status_message}", RED)
            except subprocess.CalledProcessError:
                colored_print(f"Failed to check status for repository {repo_name}.", RED)

if __name__ == "__main__":
    while True:
        action = input("Select an action (clone/set-output/set-input/check-cloned/extract/check-status/quit): ")
        if action == "clone":
            clone_repositories()
        elif action == "set-output":
            new_output_folder = input("Enter the new output folder path: ")
            update_config(output_folder=new_output_folder)
        elif action == "set-input":
            new_input_file = input("Enter the new input JSON file path: ")
            update_config(input_json_file=new_input_file)
        elif action == "check-cloned":
            check_cloned_repositories()
        elif action == "extract":
            output_folder = input("Enter the output folder path containing Git repositories: ")
            output_json_file = input("Enter the output JSON file path for extracted repositories: ")
            extract_repositories(output_folder, output_json_file)
        elif action == "check-status":
            check_repo_status()
        elif action == "quit":
            break
        else:
            colored_print("Invalid action. Please choose 'clone', 'set-output', 'set-input', 'check-cloned', 'extract', 'check-status', or 'quit'.", RED)