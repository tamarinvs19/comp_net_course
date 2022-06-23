import os, sys
import datetime as dt
from typing import Optional, Final


FILE_DIRECTORY: Final = 'files'


def read_file(path: str):
    file_path = FILE_DIRECTORY + path
    try:
        with open(file_path, 'rb') as fin:
            data = fin.readlines()
            return b''.join(data), dt.datetime.fromtimestamp(os.path.getmtime(file_path))
    except FileNotFoundError:
        return None, None

