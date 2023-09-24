import json
import subprocess
import os

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
def update_output_directory():
    new_output_folder = input("Enter the new output folder path: ")
    if not os.path.exists(new_output_folder):
        print(f"Error: The specified directory '{new_output_folder}' does not exist.")
        return

    config = {"output_folder": new_output_folder}
    with open(CONFIG_FILE, 'w') as cf:
        json.dump(config, cf, indent=4)

    print(f"Output directory updated to: {new_output_folder}")

def clone_repositories():
    # Load the config file to get the output folder and input JSON file path
    with open(CONFIG_FILE, 'r') as cf:
        config = json.load(cf)
        output_folder = config.get('output_folder')
        input_json_file = config.get('input_json_file')

    if not output_folder:
        print("Error: 'output_folder' not found in the config file.")
        return
    if not input_json_file:
        print("Error: 'input_json_file' not found in the config file.")
        return

    # Load the JSON file containing repository information
    with open(input_json_file, 'r') as f:
        repos = json.load(f)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each repository and clone it if not already cloned
    for repo in repos:
        repo_name = repo.get('name')
        repo_url = repo.get('url')
        if repo_name and repo_url:
            repo_path = os.path.join(output_folder, repo_name)

            if is_repo_cloned(repo_path, repo_url):
                print(f"Repository {repo_name} is already cloned with matching remote URL. Skipping.")
            else:
                # Clone the repository using the git command
                try:
                    subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
                    print(f"Cloned {repo_name} successfully.")
                except subprocess.CalledProcessError:
                    print(f"Failed to clone {repo_name}.")

if __name__ == "__main__":
    while True:
        action = input("Select an action (clone/update_config/quit): ")
        if action == "clone":
            clone_repositories()
        elif action == "update_config":
            update_output_directory()
        elif action == "quit":
            break
        else:
            print("Invalid action. Please choose 'clone', 'update_config', or 'quit'.")