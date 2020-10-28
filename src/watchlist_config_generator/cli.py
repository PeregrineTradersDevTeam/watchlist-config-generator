"""
Module containing the command line app.
"""
import pathlib

import click

from watchlist_config_generator.watchlist_config_generator import (
    config_file_writer,
    find_all_coreref_files,
    json_loader,
    process_all_coreref_files,
)


@click.command()
@click.argument('data_directory', type=click.Path(exists=True))
@click.argument('path_to_input_file', type=click.Path(exists=True))
@click.option("-w", "--write-to", type=click.Path(exists=True), default=None)
def makeconfig(data_directory, path_to_input_file, write_to):
    reference_data_files = find_all_coreref_files(data_directory)
    instruments_input_file = json_loader(path_to_input_file)
    discovered_contracts = process_all_coreref_files(reference_data_files, instruments_input_file)
    if not write_to:
        write_to = pathlib.Path.cwd()
    summary = config_file_writer(write_to, discovered_contracts)
    click.echo(summary)


if __name__ == '__main__':
    makeconfig()
