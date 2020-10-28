import bz2
import csv
import datetime
import json
import pathlib
import re
from typing import Dict, List, Pattern, Tuple
import multiprocessing
from itertools import repeat


def search_files(path_to_folder: str, search_pattern: str) -> List[pathlib.Path]:
    """Returns a list containing the paths of all the files matching the search pattern.

    The function searches for all the files that match the search pattern. For some
    examples on how to use the search_pattern functionality, see the Examples section
    below.

    Parameters
    ----------
    path_to_folder: str
        The path to the directory where we want to search the files.
    search_pattern: str
        A string containing the pattern that the function has to use to search for the
        files.

    Returns
    -------
    List[pathlib.Path]
        A list of pathlib.Path objects, pointing to the location of the discovered files.

    Examples
    --------
    Search for all the .py files in the current directory:
    >>> python_files = search_files('.', '*.py')

    Search for all the .py files in the direct sub-directory of the current one:
    >>> python_files = search_files('.', '*/*.py')

    Search for all the .py files in all the directories and subdirectories rescursively:
    >>> python_files = search_files('.', '**/*.py')

    Search for all the files that have a name starting with COREREF and a txt.bz2
    extension in all the subdirectories recursively:
    >>>coreref_files = search_files('.', '**/COREREF*.txt.bz2')
    """
    data_folder = pathlib.Path(path_to_folder)
    return list(data_folder.glob(search_pattern))


def find_all_coreref_files(directory: str) -> List[pathlib.Path]:
    """Searches for all the COREREF files in a directory and all its subdirectories.

    Parameters
    ----------
    directory: str
        A string containing the path to directory where we want to search the COREREF
        files.

    Returns
    -------
    List[pathlib.Path]
        A list of pathlib.Path objects, pointing to the location of all the discovered
        COREREF files.
    """
    return list(pathlib.Path(directory).glob("**/COREREF*.txt.bz2"))


def json_loader(path_to_json_file: str) -> Dict[str, List[str]]:
    """Reads a JSON file and converts its content in a dictionary.

    Parameters
    ----------
    path_to_json_file: str
        The path to the JSON file.

    Returns
    -------
    Dict[str, List[str]]
        A dictionary of source codes with the corresponding lists of instrument symbols of
        interest for each source.
    """
    with pathlib.Path(path_to_json_file).open('r') as infile:
        return json.loads(infile.read())  # type: ignore


def get_source_id_from_file_path(file_path: pathlib.Path) -> str:
    """Extrapolates the source id from the file path.

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
    source_symbols_dictionary: Dict[str, List[str]],
) -> List[str]:
    """Retrieves the list of instruments of interest for a specific source id.

    Parameters
    ----------
    source_id: str
        An ICE source id.
    source_symbols_dictionary: Dict[str, List[str]]
        A dictionary containing pairs of source-code and list of instruments of interest
        for the specific source.

    Returns
    -------
    List[str]
        A list of instrument's symbols as strings.
    """
    return source_symbols_dictionary.get(source_id)  # type: ignore


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
    """Creates a regular expression pattern to target all the instrument symbols in a list.

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


def create_dc_message_level_pattern(source_id: str, instrument_symbols: List[str]) -> str:
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


def retrieve_source_symbol_pairs(
    path_to_coreref_file: pathlib.Path,
    message_level_pattern: str,
    instrument_level_pattern: str
) -> List[Tuple[str, str]]:
    """Searches for specific instrument symbols in a COREREF reference data file.

    The function uses regular expressions to first isolate only those reference data
    messages that belong to a specific message type (DC) and refer to a specific subset of
    instrument symbols, and then to extract from the message only the contracts
    corresponding to the subset of source-specific instrument's symbols.
    Each contract discovered is included to a list together with the corresponding
    source_id.

    Parameters
    ----------
    path_to_coreref_file: pathlib.Path
        A pathlib.Path object pointing to a COREREF file containing the reference data to
        search.
    message_level_pattern: str
        A string containing the regex pattern used to filter only a specific type of
        reference data message.
    instrument_level_pattern: str
        A string containing the regex patter used to filter a specific subset of
        instrument's symbols

    Returns
    -------
    List[Tuple[str, str]]
        A list of tuples each containing the source_id and the instrument's symbol.

    """
    source_symbol_pairs = []
    with bz2.open(path_to_coreref_file, 'rb') as infile:
        for line in infile:
            if re.search(message_level_pattern, line.decode("utf8")):
                source_symbol_pairs.append(
                    (
                     get_source_id_from_file_path(path_to_coreref_file),
                     re.search(instrument_level_pattern, line.decode('utf8'))[0]  # type: ignore
                     ),
                )
    return source_symbol_pairs


def process_coreref_file(
    coreref_file_path: pathlib.Path,
    source_symbols_dictionary: Dict[str, List[str]],
) -> List[Tuple[str, str]]:
    """Searches for source-specific instrument symbols in a COREREF file.

    The function detects the source id specific to the input COREREF file, retrieves from
    the source_symbols_dictionary the list of instrument's symbols relevant for that
    source_id, and proceeds with searching for all the contracts corresponding to the
    source-specific subset of symbols.

    Parameters
    ----------
    coreref_file_path: pathlib.Path
        A pathlib.Path object pointing to the location of the COREREF file.
    source_symbols_dictionary: Dict[str, List[str]]
        A dictionary containing "source_id":["instrument_symbol"] key-value pairs,
        containing, for each source_id, the list of symbols of interest for that specific
        source.

    Returns
    -------
    List[Tuple[str, str]]
        A list of tuples, each containing the source_id, and a contract's symbol.
    """
    top_level_regex = create_dc_message_level_pattern(
            get_source_id_from_file_path(coreref_file_path),
            retrieve_instruments(
                get_source_id_from_file_path(coreref_file_path),
                source_symbols_dictionary,
            )
        )
    symbol_level_regex = create_instrument_level_pattern(
            retrieve_instruments(
                get_source_id_from_file_path(coreref_file_path),
                source_symbols_dictionary,
            )
        )
    source_specific_symbols = retrieve_source_symbol_pairs(
            coreref_file_path, top_level_regex, symbol_level_regex
        )
    return source_specific_symbols


def process_all_coreref_files(
    coreref_file_paths: List[pathlib.Path],
    source_symbols_dictionary: Dict[str, List[str]],
) -> List[Tuple[str, str]]:
    """Searches for source-specific instrument symbols in each COREREF file in the list.

    The function iterates over the list of COREREF files, detects the source id specific
    to each file, retrieves from the source_symbols_dictionary the list of instrument's
    symbols relevant for that source_id, and proceeds with searching for all the contracts
    corresponding to the source-specific subset of symbols.

    Parameters
    ----------
    coreref_file_paths: List[pathlib.Path]
        A list of pathlib.Path objects, each pointing to a different COREREF file.
    source_symbols_dictionary: Dict[str, List[str]]
        A dictionary containing "source_id":["instrument_symbol"] key-value pairs,
        containing, for each source_id, the list of symbols of interest for that specific
        source.

    Returns
    -------
    List[Tuple[str, str]]
        A list of tuples, each containing the source_id, and a contract's symbol.

    """
    discovered_symbols = []
    for file_path in coreref_file_paths:
        discovered_symbols.extend(process_coreref_file(file_path, source_symbols_dictionary))
    return discovered_symbols


def generate_config_file_path(directory_path: str) -> pathlib.Path:
    """Generates the file path of the configuration file in a given directory.

    Parameters
    ----------
    directory_path: str
        The path to the directory where the configuration file is to be placed.

    Returns
    -------
    pathlib.Path
        A Path object providing the full path to the configuration file.
    """
    return pathlib.Path(directory_path).joinpath(
        f"watchlist_config_{datetime.datetime.utcnow().strftime('%Y%m%d')}.csv"
    )


def config_file_writer(directory_path: str, source_name_pairs: List[Tuple[str, str]]) -> str:
    """Writes the source_id-symbols pairs to a csv file with a compliant header.

    Parameters
    ----------
    directory_path: str
        The path where the file should be written.
    source_name_pairs: List[Tuple[str, str]]
        A list of tuples, each containing a source_id, contract's symbol pair.

    Returns
    -------
    str
        The summary of the operation.
    """
    pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)
    file_path = generate_config_file_path(directory_path)
    with file_path.open('w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(("sourceId", "RTSsymbol"))
        for item in source_name_pairs:
            csv_writer.writerow(item)
    return (f"Configuration file successfully written.\n"
            f"{len(source_name_pairs)} symbols were added to the file.")

