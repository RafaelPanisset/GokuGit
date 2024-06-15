from difflib import unified_diff
import zlib
from commands.status import status

import os


def diff():
    """
    Prints the diff of modified files compared to their index version.
    """
    # Get the status of the repository
    untracked_files, added_files, modified_files = status()

    # Read the index file
    index_path = os.path.join('.goku', 'index')
    index_files = {}
    if os.path.exists(index_path):
        with open(index_path, 'r') as index_file:
            index_entries = [line.split() for line in index_file.readlines()]
            index_files = {entry[1]: entry[0] for entry in index_entries}

    # For each modified file, print the diff
    for file in modified_files:
        file_name = file.strip('./')
        if file_name in index_files:
            index_hash = index_files[file_name]
            object_path = os.path.join('.goku', 'objects', index_hash[:2], index_hash[2:])
            with open(object_path, 'rb') as obj_file:
                compressed_content = obj_file.read()
                index_content = zlib.decompress(compressed_content).decode()

            with open(file, 'r') as f:
                working_content = f.read()

            # Compute the diff and print it
            diff = unified_diff(index_content.splitlines(), working_content.splitlines(),
                                fromfile=f'a/{file_name}', tofile=f'b/{file_name}', lineterm='')
            for line in diff:
                print(line)
