import requests
import os 

replacement = input("Name of your project. (nospaces, all lowercase, no special chars): ")


'''    Name of Project: coursef    '''

# List of file URLs and corresponding filenames
file_links = {
    "https://raw.githubusercontent.com/DCRepublic/cs77-templates/refs/heads/main/.gitlab-ci.yml": ".gitlab-ci.yml",
    "https://raw.githubusercontent.com/DCRepublic/cs77-templates/refs/heads/main/docker-compose.yml": "docker-compose.yml",
    "https://raw.githubusercontent.com/DCRepublic/cs77-templates/refs/heads/main/Dockerfile": "Dockerfile",
}

# Download each file
for url, filename in file_links.items():
    try:
        print(f"Downloading {filename} from {url}...")
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status codes
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"{filename} downloaded successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename}. Error: {e}")


# Target directory and file info
directory = os.path.join(".github", "workflows")
url = "https://raw.githubusercontent.com/DCRepublic/cs77-templates/refs/heads/main/.github/workflows/mirror.yml" 
filename = "mirror.yml"
filepath = os.path.join(directory, filename)

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Download the file
try:
    print(f"Downloading {filename} to {directory}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, 'wb') as f:
        f.write(response.content)
    print(f"{filename} downloaded successfully to {filepath}.")
except requests.exceptions.RequestException as e:
    print(f"Download failed: {e}")


# Get the current script filename
current_file = os.path.basename(__file__)
print(current_file)
# Get user input for replacement

# Loop through all files in the current directory
for root, dirs, files in os.walk("."):
    for file in files:
        filepath = os.path.abspath(os.path.join(root, file))

        # Skip the current script itself
        if filepath == os.path.abspath(os.path.join(root, current_file)) :
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if "MYSERVICE" in content:
                new_content = content.replace("MYSERVICE", replacement)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
        except Exception as e:
            print(f"Skipped {filepath} (error: {e})")