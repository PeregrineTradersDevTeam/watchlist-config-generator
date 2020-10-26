import pathlib
import pytest

from watchlist_config_generator import watchlist_config_generator as wcg


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


class TestGetSourceFromFilePath:
    @pytest.mark.parametrize(
        'file_path, source', [
            (pathlib.Path("C:/Users/SomeUser/Data/COREREF_612_20201023.txt.bz2"), '612'),
            (pathlib.Path("C:/Users/SomeUser/Data/COREREF_945_20200815.txt.bz2"), '945'),
        ]
    )
    def test_retrieval_of_source_code(self, file_path, source):
        # Setup
        # Exercise
        retrieved_source_code = wcg.get_source_from_file_path(file_path)
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


class TestCreateMessageLevelPattern:
    def test_creation_of_message_level_pattern(self):
        # Setup
        instrument_symbols = ["F2:ES", "F2:NQ"]
        source_code = '684'
        # Exercise
        generated_message_level_regexes = wcg.create_message_level_pattern(
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


class TestRetrieveSourceNamePairs:
    def test_retrieval_of_source_name_pairs(self):
        # Setup
        path_to_reference_data_file = (
            pathlib.Path(__file__).resolve().parent / "static_data" / "COREREF_207_20201026.txt.bz2"
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
        retrieved_source_name_pairs = wcg.retrieve_source_name_pairs(
            path_to_reference_data_file, message_level_regex, instrument_level_regex
        )
        # Verify
        expected_source_name_pairs = [
            '207,F:FBTP\\H21', '207,F:FBTP\\M21', '207,F:FBTP\\Z20', '207,F:FBTS\\H21',
            '207,F:FBTS\\M21', '207,F:FBTS\\Z20', '207,F:FDAX\\H21', '207,F:FDAX\\M21',
            '207,F:FDAX\\Z20', '207,F:FESX\\H21', '207,F:FESX\\H22', '207,F:FESX\\M21',
            '207,F:FESX\\M22', '207,F:FESX\\U21', '207,F:FESX\\U22', '207,F:FESX\\Z20',
            '207,F:FESX\\Z21'
        ]
        assert retrieved_source_name_pairs == expected_source_name_pairs
        # Cleanup - none


class TestPrepareConfigFileBody:
    def test_preparation_of_config_file_body(self):
        # Setup
        source_name_pairs = [
            '207,F:FBTP\\H21', '207,F:FBTP\\M21', '207,F:FBTP\\Z20',
            '207,F:FBTS\\H21', '207,F:FBTS\\M21', '207,F:FBTS\\Z20'
        ]
        # Exercise
        generated_config_file_body = wcg.prepare_config_file_body(source_name_pairs)
        # Verify
        expected_config_file_body = (
            "sourceId, RTSsymbol\n"
            "207,F:FBTP\\H21\n"
            "207,F:FBTP\\M21\n"
            "207,F:FBTP\\Z20\n"
            "207,F:FBTS\\H21\n"
            "207,F:FBTS\\M21\n"
            "207,F:FBTS\\Z20"
        )
        assert generated_config_file_body == expected_config_file_body
        # Cleanup - none
