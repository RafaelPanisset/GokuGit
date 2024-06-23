import os
import shutil
import pytest
from commands.init import initialize_goku_repository
from commands.add import add
from commands.status import status
from commands.commit import write_tree
from commands.commit import commit
from commands.status import status
from commands.diff import diff

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup
    os.makedirs(".goku", exist_ok=True)
    yield
    # Teardown
    if os.path.exists(".goku"):
        shutil.rmtree(".goku")
    for file in ["test_file.txt", "untracked.txt", "added.txt", "modified.txt"]:
        if os.path.exists(file):
            os.remove(file)

def test_initialize_goku_repository():
    test_path = "test_repo"
    initialize_goku_repository(test_path)
    
    assert os.path.exists(os.path.join(test_path, ".goku"))
    assert os.path.exists(os.path.join(test_path, ".goku", "HEAD"))
    assert os.path.exists(os.path.join(test_path, ".goku", "config"))
    assert os.path.exists(os.path.join(test_path, ".goku", "description"))
    assert os.path.exists(os.path.join(test_path, ".goku", "hooks"))
    assert os.path.exists(os.path.join(test_path, ".goku", "info"))
    assert os.path.exists(os.path.join(test_path, ".goku", "objects"))
    assert os.path.exists(os.path.join(test_path, ".goku", "refs", "heads"))
    
    with open(os.path.join(test_path, ".goku", "HEAD"), "r") as f:
        assert f.read().strip() == "ref: refs/heads/master"
    
    shutil.rmtree(test_path)

def test_add():
    os.makedirs(".goku/objects", exist_ok=True)
    
    with open("test_file.txt", "w") as f:
        f.write("Test content")
    
    file_hash = add("test_file.txt")
    
    assert os.path.exists(f".goku/objects/{file_hash[:2]}/{file_hash[2:]}")
    
    with open(".goku/index", "r") as f:
        assert f"{file_hash} test_file.txt" in f.read()

def test_status():
    with open("untracked.txt", "w") as f:
        f.write("Untracked content")
    
    with open("added.txt", "w") as f:
        f.write("Added content")
    add("added.txt")
    
    with open("modified.txt", "w") as f:
        f.write("Original content")
    add("modified.txt")
    with open("modified.txt", "w") as f:
        f.write("Modified content")
    
    untracked, added, modified = status()
    
    assert "untracked.txt" in untracked
    assert "added.txt" in added
    assert "modified.txt" in modified

def test_write_tree():
    with open("test_file1.txt", "w") as f:
        f.write("Test content 1")
    add("test_file1.txt")
    
    with open("test_file2.txt", "w") as f:
        f.write("Test content 2")
    add("test_file2.txt")
    
    tree_hash = write_tree()
    
    assert tree_hash is not None
    assert os.path.exists(f".goku/objects/{tree_hash[:2]}/{tree_hash[2:]}")

def test_commit():
    os.makedirs(".goku/refs/heads", exist_ok=True)
    
    with open(".goku/HEAD", "w") as f:
        f.write("ref: refs/heads/master")
    
    with open("test_file.txt", "w") as f:
        f.write("Test content")
    add("test_file.txt")
    
    commit("Initial commit")
    
    with open(".goku/refs/heads/master", "r") as f:
        commit_hash = f.read().strip()
    
    assert len(commit_hash) == 40
    assert os.path.exists(f".goku/objects/{commit_hash[:2]}/{commit_hash[2:]}")

def test_diff(capsys):
    with open("test_file.txt", "w") as f:
        f.write("Original content")
    add("test_file.txt")
    
    with open("test_file.txt", "w") as f:
        f.write("Modified content")
    
    diff()
    captured = capsys.readouterr()
    
    assert "--- a/test_file.txt" in captured.out
    assert "+++ b/test_file.txt" in captured.out
    assert "-Original content" in captured.out
    assert "+Modified content" in captured.out