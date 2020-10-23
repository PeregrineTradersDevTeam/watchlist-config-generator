import pathlib
import pytest

from watchlist_config_generator import watchlist_config_generator as wcg


class TestExtrapolateSourceInstrumentsView:
    def test_extrapolation_of_source_instrument_view(self, get_source_symbols_list):
        # Setup
        path_to_instruments_file = (
            pathlib.Path(__file__).resolve().parent / 'static_data' / 'instruments.json'
        )
        # Exercise
        extrapolated_source_instrument_view = wcg.extrapolate_source_instruments_view(
            path_to_instruments_file
        )
        # Verify
        expected_source_instrument_view = get_source_symbols_list
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
        get_source_symbols_list,
        source,
        expected_list_of_instruments

    ):
        # Setup
        source_instruments_view = get_source_symbols_list
        # Exercise
        retrieved_instruments = wcg.retrieve_instruments(source_instruments_view, source)
        # Verify
        assert retrieved_instruments == expected_list_of_instruments
        # Cleanup - none


class TestCreateMessageLevelRegex:
    def test_creation_of_message_level_regexes(self, get_source_symbols_list):
        # Setup
        source_instruments_view = get_source_symbols_list
        source_code = '684'
        # Exercise
        generated_message_level_regexes = wcg.create_message_level_regex(
            source_code,
            source_instruments_view,
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


class TestCreateListOfInstrumentRegexes:
    def test_creation_of_list_of_instrument_regexes(self):
        # Setup
        instrument_names = ['F:FBTP', 'F:FDAX', 'F:FESX']
        # Exercise
        generated_instrument_regexes = wcg.create_list_of_instrument_regexes(instrument_names)
        # Verify
        expected_instrument_regexes = [
            'F:FBTP\\\\[A-Z][0-9][0-9]', 'F:FDAX\\\\[A-Z][0-9][0-9]', 'F:FESX\\\\[A-Z][0-9][0-9]'
        ]
        assert generated_instrument_regexes == expected_instrument_regexes
        # Cleanup - none
