
# Git Repository Cloner

Git Repository Cloner is a Python script that allows you to manage and clone remote Git repositories listed in a JSON file. You can configure the output directory and the JSON input file in a `config.json` file and perform various actions, including cloning repositories, updating the output directory, updating the input JSON file, and checking cloned repositories.

## Features

- Clone multiple Git repositories from a JSON input file.
- Specify the output directory for cloned repositories.
- Update the output directory and input JSON file path through a user-friendly interface.
- Check which repositories are already cloned without cloning them again.
- Generate JSON input file from the directory you have your repos.

## Getting Started

### Prerequisites

- Python 3.x
- Git command-line tool installed and available in your system's PATH

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/SDEscobedo/git-repository-cloner.git
   ```

2. Change to the project directory:

   ```bash
   cd git-repository-cloner
   ```

3. Create a `config.json` file with the following structure:

   ```json
   {
       "output_folder": "/path/to/your/output/folder",
       "input_json_file": "/path/to/your/input/repos.json"
   }
   ```

   Replace `/path/to/your/output/folder` with the desired output directory path and `/path/to/your/input/repos.json` with the path to your JSON input file containing the list of repositories to clone.

### Usage

Run the script using the following command:

```bash
python git_repository_cloner.py
```

You will be presented with a menu of actions to choose from:

- `clone`: Clone the repositories specified in the JSON file.
- `set-output`: Update the output directory path in the `config.json` file.
- `set-input`: Update the input JSON file path in the `config.json` file.
- `check-cloned`: Check which repositories are already cloned without cloning them again.
- `extract`: Generate a JSON file with a list of repos from a specified directory.
- `quit`: Exit the script.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

