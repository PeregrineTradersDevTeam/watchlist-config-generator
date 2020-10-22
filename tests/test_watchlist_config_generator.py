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
