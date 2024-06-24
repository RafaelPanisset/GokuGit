import hashlib


def create_file(path, content):
    with open(path, 'w') as file:
        file.write(path)


def calculate_file_hash(content):
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
