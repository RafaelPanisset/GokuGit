import os
import hashlib

def status():
    untracked_files = []
    added_files = []
    modified_files = []

    if os.path.exists(os.path.join('.goku', 'index')):
        with open(os.path.join('.goku', 'index'), 'r') as index_file:
            index_entries = [line.split() for line in index_file.readlines()]
    else:
        index_entries = []

    index_files = {entry[1]: entry[0] for entry in index_entries}

    for root, dirs, files in os.walk('.'):
        if '.goku' in dirs:
            dirs.remove('.goku')
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.startswith('./.goku'):
                continue

            if file in index_files:
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha1(f.read()).hexdigest()
                if file_hash != index_files[file]:
                    modified_files.append(file_path)
            else:
                untracked_files.append(file_path)

    added_files = list(index_files.keys())

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

