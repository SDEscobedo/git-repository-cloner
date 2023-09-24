import json
import subprocess
import os

def clone_repositories(json_file, output_folder):

    # Load the JSON file containing repository information
    with open(json_file, 'r') as f:
        repos = json.load(f)
        
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    # Loop through each repository and clone it
    for repo in repos:
        repo_name = repo.get('name')
        repo_url = repo.get('url')
        if repo_name and repo_url:
            repo_path = os.path.join(output_folder, repo_name)

            print('repo path:', repo_path)

            # Clone the repository using the git command
            try:
                subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
                print(f"Cloned {repo_name} successfully.")
            except subprocess.CalledProcessError:
                print(f"Failed to clone {repo_name}.")

if __name__ == "__main__":
    json_file = input("repos json file:")
    print('repos to load: ', json_file)
    output_folder = input("output folder:")
    print('output folder: ', output_folder)

    clone_repositories(json_file, output_folder)