import re
from typing import List


def get_source_from_file_name(file_name: str) -> str:
    name_components = file_name.split('_')
    source = name_components[1]
    return source
