import pathlib
import pytest

from watchlist_config_generator import watchlist_config_generator as wcg


class TestExtrapolateSourceInstrumentsView:
    def test_extrapolation_of_source_instrument_view(self, get_source_symbols_dict):
        # Setup
        path_to_instruments_file = (
            pathlib.Path(__file__).resolve().parent / 'static_data' / 'instruments.json'
        )
        # Exercise
        extrapolated_source_instrument_view = wcg.extrapolate_source_instruments_view(
            path_to_instruments_file
        )
        # Verify
        expected_source_instrument_view = get_source_symbols_dict
        assert extrapolated_source_instrument_view == expected_source_instrument_view
        # Cleanup - none


class TestDiscoverReferenceDataFiles:
    def test_discovery_of_reference_data_files(self, tmp_path):
        # Setup
        data_dir = pathlib.Path(__file__).resolve().parent / 'static_data' / 'mock_data_dir'
        # Exercise
        discovered_reference_data_files = wcg.discover_reference_data_files(data_dir)
        # Verify
        expected_files = [
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '23',
                '207',
                'CORE',
                'COREREF_207_20201023.txt.bz2',
            ),
            pathlib.Path(__file__).parent.joinpath(
                'static_data',
                'mock_data_dir',
                '2020',
                '10',
                '23',
                '367',
                'CORE',
                'COREREF_367_20201023.txt.bz2',
            ),
        ]
        assert discovered_reference_data_files == expected_files
        # Cleanup - none


class TestGetFileNameFromPath:
    def test_retrieval_of_file_name(self):
        # Setup
        path_to_file = pathlib.Path("C:/Users/SomeUser/Data/COREREF_612_20201023.txt.bz2")
        # Exercise
        retrieved_file_name = wcg.get_file_name_from_path(path_to_file)
        # Verify
        expected_file_name = "COREREF_612_20201023"
        assert retrieved_file_name == expected_file_name
        # Cleanup - none


class TestGetSourceFromFileName:
    @pytest.mark.parametrize(
        'file_name, source', [
            ('COREREF_207_20201016.txt.bz2', '207'),
            ('COREREF_945_20200815.txt.bz2', '945')
        ]
    )
    def test_retrieval_of_source_code(self, file_name, source):
        # Setup
        # Exercise
        retrieved_source_code = wcg.get_source_from_file_name(file_name)
        # Verify
        assert retrieved_source_code == source
        # Cleanup - none


class TestRetrieveInstruments:
    @pytest.mark.parametrize(
        'source, expected_list_of_instruments', [
            (
                "207",
                ["F:FDAX", "F:FSMI", "F:FESX", "F:FGBS", "F:FGBM", "F:FGBL", "F:FGBX", "F:FBTS",
                 "F:FBTP", "F:FOAT"]
             ),
            (
                "367", ["F2:ZF", "F2:ZN", "F2:ZT", "F2:UB", "F2:ZB", "F2:TN"]
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
        retrieved_instruments = wcg.retrieve_instruments(source_instruments_view, source)
        # Verify
        assert retrieved_instruments == expected_list_of_instruments
        # Cleanup - none


class TestCreateMessageRegex:
    def test_creation_of_message_regex(self):
        # Setup
        source_code = '207'
        instrument_symbol = 'F:FESX'
        # Exercise
        generated_regex = wcg.create_message_regex(source_code, instrument_symbol)
        # Verify
        expected_regex = r"^DC\|207\|F:FESX\\\\[A-Z][0-9][0-9]"
        assert generated_regex == expected_regex
        # Cleanup - none


class TestCreateMessageLevelRegexes:
    def test_creation_of_message_level_regexes(self):
        # Setup
        instrument_symbols = ["F2:ES", "F2:NQ"]
        source_code = '684'
        # Exercise
        generated_message_level_regexes = wcg.create_message_level_regexes(
            source_code,
            instrument_symbols,
        )
        # Verify
        expected_message_level_regexes = [
            r"^DC\|684\|F2:ES\\\\[A-Z][0-9][0-9]",
            r"^DC\|684\|F2:NQ\\\\[A-Z][0-9][0-9]"
        ]
        assert generated_message_level_regexes == expected_message_level_regexes
        # Cleanup - none


class TestCreateInstrumentSpecificRegex:
    def test_creation_of_instrument_specific_regex(self):
        # Setup
        instrument_name = "F:FBTP"
        # Exercise
        generated_regexes = wcg.create_instrument_specific_regex(instrument_name)
        # Verify
        correct_regex = "F:FBTP\\\\[A-Z][0-9][0-9]"
        assert generated_regexes == correct_regex
        # Cleanup - none


class TestCreateInstrumentLevelRegexes:
    def test_creation_of_list_of_instrument_regexes(self):
        # Setup
        instrument_names = ['F:FBTP', 'F:FDAX', 'F:FESX']
        # Exercise
        generated_instrument_regexes = wcg.create_instrument_level_regexes(instrument_names)
        # Verify
        expected_instrument_regexes = [
            'F:FBTP\\\\[A-Z][0-9][0-9]', 'F:FDAX\\\\[A-Z][0-9][0-9]', 'F:FESX\\\\[A-Z][0-9][0-9]'
        ]
        assert generated_instrument_regexes == expected_instrument_regexes
        # Cleanup - none


class TestCombineMultipleRegexes:
    def test_combination_of_regexes(self):
        # Setup
        regexes = ['F2:ES\\\\[A-Z][0-9][0-9]', 'F2:NQ\\\\[A-Z][0-9][0-9]']
        # Exercise
        generated_combination_of_regexes = wcg.combine_multiple_regexes(regexes)
        # Verify
        expected_combination_of_regexes = "F2:ES\\\\[A-Z][0-9][0-9]|F2:NQ\\\\[A-Z][0-9][0-9]"
        assert generated_combination_of_regexes.pattern == expected_combination_of_regexes
        # Cleanup - none
