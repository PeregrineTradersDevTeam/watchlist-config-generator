import json
import pathlib
import re
from typing import List, Dict


def extrapolate_source_instruments_view(path_to_json_file: str) -> Dict[str, List[str]]:
    """Reads a JSON file and converts its content in a dictionary.

    The function opens the JSON file containing the <source>: [<instruments] pairs and
    converts the file content in a python dictionary.

    Parameters
    ----------
    path_to_json_file: str
        The path to the JSON file.

    Returns
    -------
    Dict[str, List[str]]
        A dictionary of source codes with the corresponding lists of instruments of
        interest for each source.
    """
    with pathlib.Path(path_to_json_file).open('r') as infile:
        return json.loads(infile.read())


def get_source_from_file_name(file_name: str) -> str:
    name_components = file_name.split('_')
    return name_components[1]


def create_instrument_specific_regex(instrument_name: str) -> str:
    return rf"{instrument_name}\\[A-Z][0-9][0-9]"


def create_list_of_instrument_regexes(instrument_names: List[str]) -> List[str]:
    return [create_instrument_specific_regex(name) for name in instrument_names]
