import csv
import datetime
import pathlib
import pytest

from watchlist_config_generator import watchlist_config_generator as wcg


class TestSearchFiles:
    def test_search_of_crossref_file_in_a_directory(self):
        # Setup
        directory_to_search = (
            pathlib.Path(__file__).resolve().parent / 'static_data' / 'mock_data_dir' /
            "2020" / "10" / "16" / "S207" / "CROSS"
        )
        pattern = "CROSSREF*.txt.bz2"
        # Exercise
        discovered_reference_data_files = wcg.search_files(directory_to_search, pattern)
        # Verify
        expected_files = [
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S207',
                'CROSS',
                'CROSSREF_207_20201016.txt.bz2',
            ),
        ]
        assert discovered_reference_data_files == expected_files
        # Cleanup - none

    def test_search_of_txt_bz2_files_in_all_subdirectories(self):
        # Setup
        data_dir = pathlib.Path(__file__).resolve().parent / 'static_data' / 'mock_data_dir'
        pattern = "**/*.txt.bz2"
        # Exercise
        discovered_reference_data_files = wcg.search_files(data_dir, pattern)
        # Verify
        expected_files = [
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S207',
                'CORE',
                'COREREF_207_20201016.txt.bz2',
            ),
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S207',
                'CROSS',
                'CROSSREF_207_20201016.txt.bz2',
            ),
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S207',
                'WATCHLIST',
                'WATCHLIST_207_20201016.txt.bz2',
            ),
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S367',
                'CORE',
                'COREREF_367_20201016.txt.bz2',
            ),
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S367',
                'CROSS',
                'CROSSREF_367_20201016.txt.bz2',
            ),
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S367',
                'WATCHLIST',
                'WATCHLIST_367_20201016.txt.bz2',
            ),
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S673',
                'CORE',
                'COREREF_673_20201016.txt.bz2',
            ),
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S673',
                'CROSS',
                'CROSSREF_673_20201016.txt.bz2',
            ),
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S673',
                'WATCHLIST',
                'WATCHLIST_673_20201016.txt.bz2',
            ),
        ]
        assert discovered_reference_data_files == expected_files
        # Cleanup - none


class TestFindAllCorerefFiles:
    def test_discovery_of_coreref_files(self):
        # Setup
        data_dir = pathlib.Path(__file__).resolve().parent / 'static_data' / 'mock_data_dir'
        # Exercise
        discovered_coreref_files = wcg.find_all_coreref_files(data_dir)
        # Verify
        expected_coreref_files = [
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S207',
                'CORE',
                'COREREF_207_20201016.txt.bz2',
            ),
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S367',
                'CORE',
                'COREREF_367_20201016.txt.bz2',
            ),
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '16',
                'S673',
                'CORE',
                'COREREF_673_20201016.txt.bz2',
            ),
        ]
        assert discovered_coreref_files == expected_coreref_files
        # Cleanup - none


class TestJsonLoader:
    def test_extrapolation_of_source_instrument_view(self, get_source_symbols_dict):
        # Setup
        path_to_instruments_file = (
            pathlib.Path(__file__).resolve().parent / 'static_data' / 'instruments.json'
        )
        # Exercise
        extrapolated_source_instrument_view = wcg.json_loader(path_to_instruments_file)
        # Verify
        expected_source_instrument_view = get_source_symbols_dict
        assert extrapolated_source_instrument_view == expected_source_instrument_view
        # Cleanup - none


class TestGetSourceIdFromFilePath:
    @pytest.mark.parametrize(
        'file_path, source', [
            (pathlib.Path("C:/Users/SomeUser/Data/COREREF_612_20201023.txt.bz2"), '612'),
            (pathlib.Path("C:/Users/SomeUser/Data/COREREF_945_20200815.txt.bz2"), '945'),
        ]
    )
    def test_retrieval_of_source_code(self, file_path, source):
        # Setup
        # Exercise
        retrieved_source_code = wcg.get_source_id_from_file_path(file_path)
        # Verify
        assert retrieved_source_code == source
        # Cleanup - none


class TestRetrieveInstruments:
    @pytest.mark.parametrize(
        'source, expected_list_of_instruments', [
            (
                "207",
                ["F:FBTP", "F:FBTS", "F:FDAX", "F:FESX", "F:FGBL",
                 "F:FGBM", "F:FGBS", "F:FGBX", "F:FOAT", "F:FSMI"
                 ]
             ),
            (
                "367", ["F2:TN", "F2:UB", "F2:ZB", "F2:ZF", "F2:ZN", "F2:ZT"]
            ),
            (
                "611", ["F:FCE"]
            ),
        ]
    )
    def test_retrieval_of_instruments_per_specific_source(
        self,
        get_source_symbols_dict,
        source,
        expected_list_of_instruments

    ):
        # Setup
        source_instruments_view = get_source_symbols_dict
        # Exercise
        retrieved_instruments = wcg.retrieve_instruments(source, source_instruments_view)
        # Verify
        assert retrieved_instruments == expected_list_of_instruments
        # Cleanup - none


class TestCreateDcMessageLevelPattern:
    def test_creation_of_message_level_pattern(self):
        # Setup
        instrument_symbols = ["F2:ES", "F2:NQ"]
        source_code = '684'
        # Exercise
        generated_message_level_regexes = wcg.create_dc_message_level_pattern(
            source_code,
            instrument_symbols,
        )
        # Verify
        expected_message_level_regexes = (
            r"^DC\|684\|(F2:ES\\[A-Z][0-9]{2}|F2:NQ\\[A-Z][0-9]{2})"
        )
        assert generated_message_level_regexes == expected_message_level_regexes
        # Cleanup - none


class TestCreateSpecificInstrumentRegex:
    def test_creation_of_instrument_specific_regex(self):
        # Setup
        instrument_name = "F:FBTP"
        # Exercise
        generated_regexes = wcg.create_specific_instrument_regex(instrument_name)
        # Verify
        correct_regex = r"F:FBTP\\[A-Z][0-9]{2}"
        assert generated_regexes == correct_regex
        # Cleanup - none


class TestCreateInstrumentLevelPattern:
    def test_creation_of__instrument_level_regex(self):
        # Setup
        instrument_names = ['F:FBTP', 'F:FDAX', 'F:FESX']
        # Exercise
        generated_instrument_regexes = wcg.create_instrument_level_pattern(instrument_names)
        # Verify
        expected_instrument_regexes = (
            r'(F:FBTP\\[A-Z][0-9]{2}|F:FDAX\\[A-Z][0-9]{2}|F:FESX\\[A-Z][0-9]{2})'
        )
        assert generated_instrument_regexes == expected_instrument_regexes
        # Cleanup - none


class TestCombineMultipleRegexes:
    def test_combination_of_regexes(self):
        # Setup
        regexes = [r'F2:ES\\[A-Z][0-9]{2}', r'F2:NQ\\[A-Z][0-9]{2}']
        # Exercise
        generated_combination_of_regexes = wcg.combine_multiple_regexes(regexes)
        # Verify
        expected_combination_of_regexes = "F2:ES\\\\[A-Z][0-9]{2}|F2:NQ\\\\[A-Z][0-9]{2}"
        assert generated_combination_of_regexes.pattern == expected_combination_of_regexes
        # Cleanup - none


class TestRetrieveSourceSymbolPairs:
    def test_retrieval_of_source_name_pairs(self):
        # Setup
        path_to_reference_data_file = (
            pathlib.Path(__file__).resolve().parent / "static_data" / "mock_data_dir" /
            "2020" / "10" / "16" / "S207" / "CORE" / "COREREF_207_20201016.txt.bz2"
        )
        instrument_level_regex = (
            r"(F:FDAX\\[A-Z][0-9]{2}|F:FESX\\[A-Z][0-9]{2}|F:FBTP\\[A-Z][0-9]{2}|"
            r"F:FBTS\\[A-Z][0-9]{2})"
        )
        message_level_regex = (
            r"^DC\|207\|(F:FDAX\\[A-Z][0-9]{2}|F:FESX\\[A-Z][0-9]{2}|F:FBTP\\[A-Z][0-9]{2}|"
            r"F:FBTS\\[A-Z][0-9]{2})"
        )
        # Exercise
        retrieved_source_name_pairs = wcg.retrieve_source_symbol_pairs(
            path_to_reference_data_file, message_level_regex, instrument_level_regex
        )
        # Verify
        expected_source_name_pairs = [
            ('207', 'F:FBTP\\H21'), ('207', 'F:FBTP\\M21'), ('207', 'F:FBTP\\Z20'),
            ('207', 'F:FBTS\\H21'), ('207', 'F:FBTS\\M21'), ('207', 'F:FBTS\\Z20'),
            ('207', 'F:FDAX\\H21'), ('207', 'F:FDAX\\M21'), ('207', 'F:FDAX\\Z20'),
            ('207', 'F:FESX\\H21'), ('207', 'F:FESX\\H22'), ('207', 'F:FESX\\M21'),
            ('207', 'F:FESX\\M22'), ('207', 'F:FESX\\U21'), ('207', 'F:FESX\\U22'),
            ('207', 'F:FESX\\Z20'), ('207', 'F:FESX\\Z21')
        ]
        assert retrieved_source_name_pairs == expected_source_name_pairs
        # Cleanup - none


class TestProcessAllCorerefFiles:
    def test_discovery_of_all_symbols(self, get_source_symbols_dict):
        # Setup
        files_to_process = [
            pathlib.Path(__file__).resolve().parent.joinpath(
                'static_data', 'mock_data_dir', '2020', '10', '16', 'S367', 'CORE',
                'COREREF_367_20201016.txt.bz2'
            ),
            pathlib.Path(__file__).resolve().parent.joinpath(
                'static_data', 'mock_data_dir', '2020', '10', '16', 'S673', 'CORE',
                'COREREF_673_20201016.txt.bz2'
                ),
        ]
        dictionary_of_symbols = get_source_symbols_dict
        # Exercise
        discovered_symbols = wcg.process_all_coreref_files(
            files_to_process, dictionary_of_symbols
        )
        # Verify
        expected_symbols = [
            ('367', 'F2:TN\\H21'), ('367', 'F2:TN\\M21'), ('367', 'F2:TN\\Z20'),
            ('367', 'F2:UB\\H21'), ('367', 'F2:UB\\M21'), ('367', 'F2:UB\\Z20'),
            ('367', 'F2:ZB\\H21'), ('367', 'F2:ZB\\M21'), ('367', 'F2:ZB\\Z20'),
            ('367', 'F2:ZF\\H21'), ('367', 'F2:ZF\\M21'), ('367', 'F2:ZF\\U20'),
            ('367', 'F2:ZF\\Z20'), ('367', 'F2:ZN\\H21'), ('367', 'F2:ZN\\M21'),
            ('367', 'F2:ZN\\Z20'), ('367', 'F2:ZT\\H21'), ('367', 'F2:ZT\\M21'),
            ('367', 'F2:ZT\\U20'), ('367', 'F2:ZT\\Z20'), ('673', 'F2:ES\\H21'),
            ('673', 'F2:ES\\M21'), ('673', 'F2:ES\\U21'), ('673', 'F2:ES\\Z20'),
            ('673', 'F2:ES\\Z21'), ('673', 'F2:NQ\\H21'), ('673', 'F2:NQ\\M21'),
            ('673', 'F2:NQ\\U21'), ('673', 'F2:NQ\\Z20'), ('673', 'F2:NQ\\Z21')
        ]
        assert discovered_symbols == expected_symbols
        # Cleanup - none


class TestGenerateConfigFilePath:
    def test_generation_of_file_path(self):
        # Setup
        target_directory = "C:/Users/some_user/config_files"
        # Exercise
        generated_file_path = wcg.generate_config_file_path(target_directory)
        # Verify
        expected_file_path = pathlib.Path(target_directory).joinpath(
            f"watchlist_config_{datetime.datetime.utcnow().strftime('%Y%m%d')}.csv")
        assert generated_file_path.as_posix() == expected_file_path.as_posix()
        # Cleanup - none


class TestConfigFileWriter:
    def test_csv_file_is_created(self):
        # Setup
        target_directory = pathlib.Path(__file__).resolve().parent / "static_data"
        source_symbol_pairs = [
            ('367', 'F2:TN\\H21')
        ]
        # Exercise
        wcg.config_file_writer(target_directory.as_posix(), source_symbol_pairs)
        # Verify
        expected_file_path = (
            pathlib.Path(__file__).resolve().parent / "static_data" /
            f"watchlist_config_{datetime.datetime.utcnow().strftime('%Y%m%d')}.csv"
        )
        assert expected_file_path.is_file() is True
        # Cleanup - none
        target_directory.joinpath(expected_file_path).unlink(missing_ok=True)

    def test_written_file_has_proper_name(self):
        # Setup
        target_directory = pathlib.Path(__file__).resolve().parent / "static_data"
        source_symbol_pairs = [
            ('367', 'F2:TN\\H21'), ('367', 'F2:TN\\M21'), ('367', 'F2:TN\\Z20'),
            ('367', 'F2:UB\\H21'), ('367', 'F2:UB\\M21'), ('367', 'F2:UB\\Z20'),
            ('367', 'F2:ZB\\H21'), ('367', 'F2:ZB\\M21'), ('367', 'F2:ZB\\Z20'),
            ('367', 'F2:ZF\\H21'), ('367', 'F2:ZF\\M21'), ('367', 'F2:ZF\\U20'),
            ('367', 'F2:ZF\\Z20'), ('367', 'F2:ZN\\H21'), ('367', 'F2:ZN\\M21'),
            ('367', 'F2:ZN\\Z20'), ('367', 'F2:ZT\\H21'), ('367', 'F2:ZT\\M21'),
            ('367', 'F2:ZT\\U20'), ('367', 'F2:ZT\\Z20')
        ]
        # Exercise
        wcg.config_file_writer(target_directory.as_posix(), source_symbol_pairs)
        file_name = list(target_directory.glob("watchlist_config*.csv"))[0].name
        # Verify
        expected_file_name = f"watchlist_config_{datetime.datetime.utcnow().strftime('%Y%m%d')}.csv"
        assert file_name == expected_file_name
        # Cleanup - none
        target_directory.joinpath(expected_file_name).unlink(missing_ok=True)

    def test_file_has_proper_header(self):
        # Setup
        target_directory = pathlib.Path(__file__).resolve().parent / "static_data"
        source_symbol_pairs = []
        # Exercise
        wcg.config_file_writer(target_directory.as_posix(), source_symbol_pairs)
        # Verify
        expected_header = "sourceId,RTSsymbol"
        path_to_file = (
            pathlib.Path(__file__).resolve().parent / "static_data" /
            f"watchlist_config_{datetime.datetime.utcnow().strftime('%Y%m%d')}.csv"
        )
        with path_to_file.open('r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for index, row in enumerate(csv_reader):
                if index == 0:
                    file_header =  ','.join(row)
        assert file_header == expected_header
        # Cleanup - none
        path_to_file.unlink(missing_ok=True)

    def test_file_has_expected_content(self):
        # Setup
        target_directory = pathlib.Path(__file__).resolve().parent / "static_data"
        source_symbol_pairs = [
            ('207', 'F:FBTP\\H21'), ('207', 'F:FBTP\\M21'), ('207', 'F:FBTP\\Z20'),
            ('207', 'F:FBTS\\H21'), ('207', 'F:FBTS\\M21'), ('207', 'F:FBTS\\Z20')
        ]
        # Exercise
        wcg.config_file_writer(target_directory.as_posix(), source_symbol_pairs)
        # Verify
        path_to_file = (
            pathlib.Path(__file__).resolve().parent / "static_data" /
            f"watchlist_config_{datetime.datetime.utcnow().strftime('%Y%m%d')}.csv"
        )
        expected_file_content = (
            "sourceId,RTSsymbol\n"
            "207,F:FBTP\\H21\n"
            "207,F:FBTP\\M21\n"
            "207,F:FBTP\\Z20\n"
            "207,F:FBTS\\H21\n"
            "207,F:FBTS\\M21\n"
            "207,F:FBTS\\Z20"
        )
        with path_to_file.open('r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # file_content = ''
            # for index, row in enumerate(csv_reader):
            #     if index == 0:
            #         file_content + ','.join(row)
            #     else:
            #         file_content + '\n' + ','.join(row)
            rows = [','.join(row) for row in csv_reader]
            file_content = '\n'.join(rows)
        assert file_content == expected_file_content
        # Cleanup - none
        path_to_file.unlink(missing_ok=True)

    def test_return_the_expected_summary(self):
        # Setup
        target_directory = pathlib.Path(__file__).resolve().parent / "static_data"
        source_symbol_pairs = [
            ('673', 'F2:ES\\H21'), ('673', 'F2:ES\\M21'), ('673', 'F2:ES\\U21'),
            ('673', 'F2:ES\\Z20'), ('673', 'F2:ES\\Z21'), ('673', 'F2:NQ\\H21'),
            ('673', 'F2:NQ\\M21'), ('673', 'F2:NQ\\U21'), ('673', 'F2:NQ\\Z20'),
            ('673', 'F2:NQ\\Z21')
        ]
        # Exercise
        generated_summary = wcg.config_file_writer(target_directory.as_posix(), source_symbol_pairs)
        # Verify
        expected_summary = "Write complete. Written 10 symbols to the file."
        assert generated_summary == expected_summary
        # Cleanup
        path_to_file = (
            pathlib.Path(__file__).resolve().parent / "static_data" /
            f"watchlist_config_{datetime.datetime.utcnow().strftime('%Y%m%d')}.csv"
        )
        path_to_file.unlink(missing_ok=True)
