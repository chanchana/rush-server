from pathlib import Path

def get_filename(path):
    return Path(path).name

def get_file(path):
    return open(get_filename(path), 'r')