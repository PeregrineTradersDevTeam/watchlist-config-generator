import pytest

from watchlist_config_generator import watchlist_config_generator as wcg


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
