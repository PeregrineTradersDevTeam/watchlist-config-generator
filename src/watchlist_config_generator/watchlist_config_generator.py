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
    """Extrapolates the source code from the file name.

    To retrieve the source code from the file name, the function uses the fact that the
    ICE uses a consistent naming convention consisting of the file type accompanied by
    the source code and the date the data in the file was generated.
    (e.g. COREREF_207_20201023.txt.bz2).

    Parameters
    ----------
    file_name: str
        The name of a file following the ICE naming convention.

    Returns
    -------
    str
        The source-code.

    """
    name_components = file_name.split('_')
    return name_components[1]


def retrieve_instruments(
    source_instruments_view: Dict[str, List[str]],
    source_code: str
) -> List[str]:
    """Retrieves the list of instruments of interest for a specific source-code.

    Parameters
    ----------
    source_instruments_view: Dict[str, List[str]]
        A dictionary containing pairs of source-code and list of instruments of interest
        for the specific source.
    source_code: str
        An ICE source-code corresponding to a specific market.

    Returns
    -------
    List[str]
        A list of instrument's symbols as strings.

    """
    return source_instruments_view.get(source_code)


def create_instrument_specific_regex(instrument_symbol: str) -> str:
    """Creates a regular expression specific to a futures instrument symbol.

    The function uses the facts that futures contracts have a naming convention that
    follows the structure "<instrument_symbol>\\\\<month_code><expiration_year>" (e.g. for
    the EURO STOXX 50 future, with delivery March 2021, the contract name is F:FESX\\\\H21
    ), to create symbol-specific regular expressions.

    Parameters
    ----------
    instrument_symbol: str
        The stable part of the instrument symbol as defined by ICE (e.g. F:FESX for the
        EURO STOXX 50 Future, or F2:ES for the E-mini S&P 500 Index Futures).

    Returns
    -------
    str
        The regular expression with embedded the stable part of the instrument symbol.

    """
    return rf"{instrument_symbol}\\[A-Z][0-9][0-9]"


def create_list_of_instrument_regexes(instrument_names: List[str]) -> List[str]:
    return [create_instrument_specific_regex(name) for name in instrument_names]
