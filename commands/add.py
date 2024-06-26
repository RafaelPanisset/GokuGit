
import os 
import zlib 
from utils.file_operations import calculate_file_hash

def add(file_name):
    """
    Add a file to the Goku repository's staging area.
    
    This function reads the file, calculates its hash, stores it as an object,
    and updates the index with the new file information.
    """
    file_path = os.path.relpath(file_name)
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist")
        return

    with open(file_path, 'rb') as f:
        content = f.read()
    
    file_hash = calculate_file_hash(content)
    
    # Store the file content as an object
    object_path = os.path.join('.goku', 'objects', file_hash[:2], file_hash[2:])
    os.makedirs(os.path.dirname(object_path), exist_ok=True)
    with open(object_path, 'wb') as f:
        f.write(zlib.compress(content))

    # Update the index
    index_path = os.path.join('.goku', 'index')
    updated_index = []
    file_updated = False

    if os.path.exists(index_path):
        with open(index_path, 'r') as index_file:
            for line in index_file:
                entry_hash, entry_name = line.strip().split(maxsplit=1)
                if entry_name == file_path:
                    updated_index.append(f"{file_hash} {file_path}")
                    file_updated = True
                else:
                    updated_index.append(line.strip())

    if not file_updated:
        updated_index.append(f"{file_hash} {file_path}")

    with open(index_path, 'w') as index_file:
        index_file.write('\n'.join(updated_index) + '\n')

    return file_hash