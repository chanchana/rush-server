from pathlib import Path

def get_filename(path):
    print(path)
    return Path(path).name

def get_file(path):
    print(get_filename(path))
    # return open(str(get_filename(path)), 'r')