import pytest


@pytest.fixture
def get_source_symbols_dict():
    return {
        "207": [
            "F:FBTP", "F:FBTS", "F:FDAX", "F:FESX", "F:FGBL",
            "F:FGBM", "F:FGBS", "F:FGBX", "F:FOAT", "F:FSMI"
        ],
        "367": [
            "F2:TN", "F2:UB", "F2:ZB", "F2:ZF", "F2:ZN", "F2:ZT"
        ],
        "611": ["F:FCE"],
        "612": ["F:FCE"],
        "652": ["F:FIB"],
        "673": ["F2:ES", "F2:NQ"],
        "676": ["F2:ED", "F2:RTY"],
        "680": ["F2:ED", "F2:RTY"],
        "684": ["F2:ES", "F2:NQ"],
        "688": ["F2:YM"],
        "693": [
            "F2:TN", "F2:UB", "F2:ZB", "F2:ZF", "F2:ZN", "F2:ZT"
        ],
        "748": [
            "F:FBTP", "F:FBTS", "F:FDAX", "F:FESX", "F:FGBL",
            "F:FGBM", "F:FGBS", "F:FGBX", "F:FOAT", "F:FSMI"
        ],
        "890": ["F:Z"],
        "903": ["F:FIB"],
        "905": ["F:Z"],
        "945": ["F2:YM"],
    }
