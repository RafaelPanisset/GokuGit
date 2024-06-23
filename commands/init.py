import os
from utils.file_operations import create_file

def initialize_goku_repository(path):
    goku_structure = {
        "HEAD": "ref: refs/heads/master",
        "config": '[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = true\n',
        "description": 'Unnamed repository; edit this file to name it for gokuweb.\n',
        "hooks": None,
        "info": None,
        "objects": None,
        "refs": None
    }

    goku_path = os.path.join(path, '.goku')
    os.makedirs(goku_path, exist_ok=True)
     
    for file_name, content in goku_structure.items():
        if file_name in ["objects", "refs", "hooks", "info"] or content is None:
            os.makedirs(os.path.join(goku_path, file_name), exist_ok=True)
        else:
            create_file(os.path.join(goku_path, file_name), content)

    # Create the refs/heads directory
    refs_heads_path = os.path.join(goku_path, 'refs', 'heads')
    os.makedirs(refs_heads_path, exist_ok=True)

    # Ensure HEAD file is created correctly
    head_path = os.path.join(goku_path, 'HEAD')
    with open(head_path, 'w') as head_file:
        head_file.write("ref: refs/heads/master\n")

    print(f"Initialized empty Goku repository in {os.path.abspath(path)}")