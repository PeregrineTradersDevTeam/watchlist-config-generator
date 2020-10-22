import re
from typing import List


def get_source_from_file_name(file_name: str) -> str:
    name_components = file_name.split('_')
    source = name_components[1]
    return source


def create_instrument_specific_regex(instrument_name: str) -> str:
    regex = rf"{instrument_name}\\[A-Z][0-9][0-9]"
    return regex
