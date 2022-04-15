import os

from python.utils.error_utils import exception


def get_file_vars(_file: str) -> tuple[str]:
    return os.path.splitext(_file)


def get_file_name(_file: str) -> str:
    return get_file_vars(_file)[0]


def get_file_ext(_file: str) -> str:
    return get_file_vars(_file)[1]


def transfer(_origin_path: str, _destination_path: str) -> bool:
    try:
        in_file = open(_origin_path, "r")
        file_content = in_file.read()
        in_file.close()

        out_file = open(_destination_path, "w")
        out_file.write(file_content)
        out_file.close()
        return True
    except:
        exception(f"Issue transferring file: {_origin_path} to: {_destination_path}")
        return False
