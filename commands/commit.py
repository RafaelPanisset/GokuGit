from datetime import datetime
import os
import hashlib
import zlib

def write_tree():
    index_path = os.path.join('.goku', 'index')
    
    # If the index file doesn't exist, return None
    if not os.path.exists(index_path):
        return None

    tree_entries = []
    
    # Open the index file and read its contents
    with open(index_path, 'r') as index_file:
        for line in index_file:
            file_hash, file_name = line.strip().split()
            mode = '100644'  # Assuming regular files for simplicity
            # Append the mode, filename, and file hash to tree_entries
            tree_entries.append(f"{mode} {file_name}\0{bytes.fromhex(file_hash)}")

    # Join tree entries and encode them
    tree_content = '\n'.join(tree_entries).encode()
    
    # Calculate the tree hash
    tree_hash = hashlib.sha1(b'tree ' + str(len(tree_content)).encode() + b'\0' + tree_content).hexdigest()

    # Prepare the directory path for the tree object
    objects_path = os.path.join('.goku', 'objects')
    hash_dir = os.path.join(objects_path, tree_hash[:2])
    
    # Create the directory if it doesn't exist
    os.makedirs(hash_dir, exist_ok=True)

    # Prepare the file path for the tree object
    hash_file_path = os.path.join(hash_dir, tree_hash[2:])
    
    # Compress the tree content
    compressed_content = zlib.compress(tree_content)
    
    # Write the compressed tree content to the file
    with open(hash_file_path, 'wb') as hash_file:
        hash_file.write(compressed_content)

    # Return the tree hash
    return tree_hash


def commit(message):
    tree_hash = write_tree()
    if tree_hash is None:
        print("Nothing to commit")
        return

    head_file_path = os.path.join('.goku', 'HEAD')
    with open(head_file_path, 'r') as head_file:
        ref = head_file.read().strip().split()[-1]

    ref_file_path = os.path.join('.goku', ref)
    parent_hash = None
    if os.path.exists(ref_file_path):
        with open(ref_file_path, 'r') as ref_file:
            parent_hash = ref_file.read().strip()

    author = "Author Name <author@example.com>"
    timestamp = int(datetime.now().timestamp())
    
    commit_content_lines = [
        f"tree {tree_hash}",
        f"author {author} {timestamp} +0000",
        f"committer {author} {timestamp} +0000",
        "",
        message,
        ""
    ]
    
    if parent_hash:
        commit_content_lines.insert(1, f"parent {parent_hash}")

    commit_content = "\n".join(commit_content_lines)

    commit_hash = hashlib.sha1(b'commit ' + str(len(commit_content)).encode() + b'\0' + commit_content.encode()).hexdigest()

    objects_path = os.path.join('.goku', 'objects', commit_hash[:2])
    print(objects_path)
    os.makedirs(objects_path, exist_ok=True)

    hash_file_path = os.path.join(objects_path, commit_hash[2:])
    compressed_content = zlib.compress(commit_content.encode())
    with open(hash_file_path, 'wb') as hash_file:
        hash_file.write(compressed_content)
    print(ref_file_path)
    with open(ref_file_path, 'w') as ref_file:
        ref_file.write(commit_hash)

    print(f"Committed to {ref.split('/')[-1]}: {commit_hash}")