import csv
import datetime
import bz2
import json
import pathlib
import re
from typing import Dict, List, Optional, Pattern, Tuple


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


def get_source_from_file_path(file_path: pathlib.Path) -> str:
    """Extrapolates the source code from the file path.

    To retrieve the source id from the file name, the function uses the fact that the
    ICE uses a consistent naming convention consisting of the file type accompanied by
    the source id and the date the data in the file was generated.
    (e.g. COREREF_207_20201023.txt.bz2).

    Parameters
    ----------
    file_path: str
        The path to the file for which the source id has to be extrapolated.

    Returns
    -------
    str
        The source id.
    """
    file_name = file_path.name.split(".")[0]
    name_components = file_name.split('_')
    return name_components[1]


def retrieve_instruments(
    source_id: str,
    source_instruments_view: Dict[str, List[str]],
) -> List[str]:
    """Retrieves the list of instruments of interest for a specific source id.

    Parameters
    ----------
    source_id: str
        An ICE source id corresponding to a specific market.
    source_instruments_view: Dict[str, List[str]]
        A dictionary containing pairs of source-code and list of instruments of interest
        for the specific source.

    Returns
    -------
    List[str]
        A list of instrument's symbols as strings.
    """
    return source_instruments_view.get(source_id)


def create_specific_instrument_regex(instrument_symbol: str) -> str:
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
    return rf"{instrument_symbol}\\[A-Z][0-9]{{2}}"


def create_instrument_level_pattern(instrument_symbols: List[str]) -> str:
    """Creates a regular expression pattern to target all the instrument names relevant to a source.

    The function creates a regular expression pattern to target, within a specific DC
    message, the portion of the message containing the complete instrument symbol, for
    each instrument symbol included in the list passed as an input of the function.

    Parameters
    ----------
    instrument_symbols: List[str]
        A list of the stable components of the futures instrument symbols.

    Returns
    -------
    str
        A regular expression pattern.
    """
    specific_instrument_regexes = [
        create_specific_instrument_regex(name)
        for name in instrument_symbols
    ]
    return rf"({'|'.join(specific_instrument_regexes)})"


def create_message_level_pattern(source_id: str, instrument_symbols: List[str]) -> str:
    """Creates a regular expression pattern to target DC message types.

    The function creates a list of regular expressions to target the DC messages
    containing the information of all the instruments of interest for the specific
    source id.

    Parameters
    ----------
    source_id: str
        An ICE source id.
    instrument_symbols: List[str]
        A list of the stable portion of futures contracts symbols.

    Returns
    -------
    str
        A regular expression pattern.
    """
    return rf"^DC\|{source_id}\|{create_instrument_level_pattern(instrument_symbols)}"


def combine_multiple_regexes(regexes: List[str]) -> Pattern[str]:
    """Combine multiple regular expressions in a single pattern.

    Parameters
    ----------
    regexes: List[str]
        A list of regular expressions.

    Returns
    -------
    Pattern[str]
        A Pattern object containing the pattern that combines all the passed regular
        expressions.
    """
    return re.compile("|".join(regexes))


def retrieve_source_name_pairs(
    path_to_reference_data_file: pathlib.Path,
    message_level_pattern: str,
    instrument_level_pattern: str
) -> List[Tuple[str, str]]:
    source_name_pairs = []
    with bz2.open(path_to_reference_data_file, 'rb') as infile:
        for line in infile:
            if re.search(message_level_pattern, line.decode("utf8")):
                source_name_pairs.append(
                    (
                     get_source_from_file_path(path_to_reference_data_file),
                     re.search(instrument_level_pattern, line.decode('utf8'))[0]
                     ),
                )
    return source_name_pairs

