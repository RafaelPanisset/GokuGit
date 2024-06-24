import os
from utils.file_operations import calculate_file_hash

def status():
    """
    Display the status of the Goku repository.
    
    This function checks the current state of files in the working directory
    against the index, categorizing them as untracked, added, or modified.
    """
    
    untracked_files = []
    added_files = []
    modified_files = []

    # Read the index
    index_path = os.path.join('.goku', 'index')
    index_files = {}
    if os.path.exists(index_path):
        with open(index_path, 'r') as index_file:
            index_entries = [line.strip().split(maxsplit=1) for line in index_file]
            index_files = {entry[1]: entry[0] for entry in index_entries}

    # Walk through the directory
    for root, dirs, files in os.walk('.'):
        if '.goku' in dirs:
            dirs.remove('.goku')
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file))
            if rel_path.startswith('.goku'):
                continue

            if rel_path in index_files:
                with open(rel_path, 'rb') as f:
                    content = f.read()
                file_hash = calculate_file_hash(content)
                if file_hash != index_files[rel_path]:
                    modified_files.append(rel_path)
                else:
                    added_files.append(rel_path)
            else:
                untracked_files.append(rel_path)

    # Print status
    print("Untracked files:")
    for file in untracked_files:
        print(file)
    print("\nAdded files:")
    for file in added_files:
        print(file)
    print("\nModified files:")
    for file in modified_files:
        print(file)

    return untracked_files, added_files, modified_files