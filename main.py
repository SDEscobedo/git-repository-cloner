import json
import subprocess
import os

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
def clone_repositories(json_file, output_folder):
    # Load the JSON file containing repository information
    with open(json_file, 'r') as f:
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
                print(f"Repository {repo_name} is already cloned. Skipping.")
            else:
                # Clone the repository using the git command
                try:
                    subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
                    print(f"Cloned {repo_name} successfully.")
                except subprocess.CalledProcessError:
                    print(f"Failed to clone {repo_name}.")

if __name__ == "__main__":
    json_file = input("Enter the JSON file path containing repository information: ")
    output_folder = input("Enter the output folder where repositories should be cloned: ")

    clone_repositories(json_file, output_folder)