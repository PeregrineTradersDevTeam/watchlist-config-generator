import pathlib
import pytest

from watchlist_config_generator import watchlist_config_generator as wcg


class TestExtrapolateSourceInstrumentsView:
    def test_extrapolation_of_source_instrument_view(self):
        # Setup
        path_to_instruments_file = (
            pathlib.Path(__file__).resolve().parent / 'static_data' / 'instruments.json'
        )
        # Exercise
        extrapolated_source_instrument_view = wcg.extrapolate_source_instruments_view(
            path_to_instruments_file
        )
        # Verify
        expected_source_instrument_view = {
            "207": [
                "F:FDAX", "F:FSMI", "F:FESX", "F:FGBS", "F:FGBM",
                "F:FGBL", "F:FGBX", "F:FBTS", "F:FBTP", "F:FOAT"
            ],
            "367": [
                "F2:ZF", "F2:ZN", "F2:ZT", "F2:UB", "F2:ZB", "F2:TN"
            ],
            "611": ["F:FCE"],
            "612": ["F:FCE"],
            "652": ["F:FIB"],
            "673": ["F2:ES", "F2:NQ"],
            "676": ["F2:RTY", "F2:ED"],
            "680": ["F2:RTY", "F2:ED"],
            "684": ["F2:ES", "F2:NQ"],
            "688": ["F2:YM"],
            "693": [
                "F2:ZF", "F2:ZN", "F2:ZT", "F2:UB", "F2:ZB", "F2:TN"
            ],
            "748": [
                "F:FDAX", "F:FSMI", "F:FESX", "F:FGBS", "F:FGBM",
                "F:FGBL", "F:FGBX", "F:FBTS", "F:FBTP", "F:FOAT"
            ],
            "890": ["F:Z"],
            "903": ["F:FIB"],
            "905": ["F:Z"],
            "945": ["F2:YM"],
        }
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
