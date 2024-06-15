import os 
import hashlib
import zlib 

def add(file_name):
    file_path = os.path.join(os.getcwd(), file_name)

    if not os.path.exists(file_path):
        print(f"Error: {file_name} does not exist")
        return

    with open(file_path, 'rb') as file:
        file_contents = file.read()
        file_hash = hashlib.sha1(file_contents).hexdigest()

    objects_path = os.path.join('.goku', 'objects')

    hash_dir = os.path.join(objects_path, file_hash[:2])
    os.makedirs(hash_dir, exist_ok=True)

    hash_file_path = os.path.join(hash_dir, file_hash[2:])
    compressed_content = zlib.compress(file_contents)

    with open(hash_file_path, 'wb') as hash_file:
        hash_file.write(compressed_content)

    index_path = os.path.join('.goku', 'index')
    with open(index_path, 'a') as index_file:
        index_file.write(f"{file_hash} {file_name}\n")

    return file_hash

