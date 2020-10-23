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


def discover_reference_data_files(path_to_data_folder: str) -> List[pathlib.Path]:
    """Returns a list containing the paths to the reference data files.

    The function searches COREREF files in the directory tree underlying the root of the
    data folder and collects the paths of the discovered files in a list.

    Parameters
    ----------
    path_to_data_folder: str
        The path to the root of the data folder.

    Returns
    -------
    List[pathlib.Path]
        A list of pathlib.Path objects, pointing to the location of the COREREF files.
    """
    data_folder = pathlib.Path(path_to_data_folder)
    return list(data_folder.glob("**/COREREF*.txt.bz2"))


def get_source_from_file_name(file_name: str) -> str:
    name_components = file_name.split('_')
    return name_components[1]


def create_instrument_specific_regex(instrument_name: str) -> str:
    return rf"{instrument_name}\\[A-Z][0-9][0-9]"


def create_list_of_instrument_regexes(instrument_names: List[str]) -> List[str]:
    return [create_instrument_specific_regex(name) for name in instrument_names]
