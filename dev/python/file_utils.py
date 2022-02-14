import os

def get_file_vars(_file: str):
    return os.path.splitext(_file)

def get_file_name(_file: str):
    return get_file_vars(_file)[0]

def get_ext(_file: str):
    return get_file_vars(_file)[1]
