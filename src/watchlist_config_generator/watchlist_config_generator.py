import re
from typing import List


def get_source_from_file_name(file_name: str) -> str:
    name_components = file_name.split('_')
    return name_components[1]


def create_instrument_specific_regex(instrument_name: str) -> str:
    return rf"{instrument_name}\\[A-Z][0-9][0-9]"


def create_list_of_instrument_regexes(instrument_names: List) -> List:
    return [create_instrument_specific_regex(name) for name in instrument_names]
