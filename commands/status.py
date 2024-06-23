import os
import hashlib

def status():
    untracked_files = []
    added_files = []
    modified_files = []

    if os.path.exists(os.path.join('.goku', 'index')):
        with open(os.path.join('.goku', 'index'), 'r') as index_file:
            index_entries = [line.strip().split(maxsplit=1) for line in index_file.readlines()]
    else:
        index_entries = []

    index_files = {entry[1]: entry[0] for entry in index_entries}

    for root, dirs, files in os.walk('.'):
        if '.goku' in dirs:
            dirs.remove('.goku')
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file))
            if rel_path.startswith('.goku'):
                continue

            if rel_path in index_files:
                with open(rel_path, 'rb') as f:
                    file_hash = hashlib.sha1(f.read()).hexdigest()
                if file_hash != index_files[rel_path]:
                    modified_files.append(rel_path)
            else:
                untracked_files.append(rel_path)

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